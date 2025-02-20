from datetime import datetime
import json

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///prod.db"
    db.init_app(app)

    from .models import Client, ClientParking, Parking

    @app.before_request
    def before_request_func():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route("/clients", methods=["GET"])
    def get_clients():
        query = db.select(Client)
        clients = db.session.execute(query).scalars().all()
        clients_to_json = [client.to_json() for client in clients]

        return app.response_class(
            response=json.dumps({"clients": clients_to_json}, indent=4),
            status=200,
            mimetype="application/json",
        )

    @app.route("/clients/<int:client_id>")
    def get_client_by_id(client_id):

        query = db.select(Client).where(Client.id == client_id)
        client = db.session.execute(query).scalar_one_or_none()
        if client:
            client_to_json = client.to_json()
            return jsonify({f"client_{client_id}": client_to_json})
        return jsonify({"error": "client not found"})

    @app.route("/clients", methods=["POST"])
    def post_client():
        data = request.get_json()
        name = data.get("name")
        surname = data.get("surname")
        credit_card = data.get("credit_card")
        car_number = data.get("car_number")
        client = Client(
            name=name,
            surname=surname,
            credit_card=credit_card,
            car_number=car_number
        )
        db.session.add(client)
        db.session.commit()

        client_json = client.to_json()
        return jsonify({"new_client": client_json}), 201

    @app.route("/parking", methods=["POST"])
    def post_parking():
        data = request.get_json()
        address = data.get("address")
        opened = data.get("opened")
        count_places = data.get("count_places")
        count_available_places = data.get("count_available_places")
        parking = Parking(
            address=address,
            opened=opened,
            count_places=count_places,
            count_available_places=count_available_places,
        )
        db.session.add(parking)
        db.session.commit()

        parking_json = parking.to_json()
        return jsonify({"new_parking": parking_json}), 201

    @app.route("/client_parking", methods=["POST"])
    def post_client_parking():

        data = request.get_json()
        client_id = data.get("client_id")
        parking_id = data.get("parking_id")
        query = db.select(Parking).where(Parking.id == parking_id)
        parking = db.session.execute(query).scalar_one_or_none()
        if parking.opened and parking.count_available_places >= 1:
            parking.count_available_places -= 1
            client_parking = ClientParking(
                client_id=client_id,
                parking_id=parking_id,
                time_in=datetime.now()
            )
            db.session.add(client_parking)
            db.session.commit()
            return (
                f"клиент с id = {client_id}, "
                f"занял место на парковке {parking_id}",
                201,
            )
        else:
            return "парковка закрыта или на ней нет свободных мест"

    @app.route("/client_parking", methods=["DELETE"])
    def delete_client_parking():

        data = request.get_json()
        client_id = data.get("client_id")
        parking_id = data.get("parking_id")
        query = (db.select(ClientParking).
                 where(ClientParking.client_id == client_id))
        client_parking = db.session.execute(query).scalar_one_or_none()

        if client_parking.client.credit_card:
            db.session.delete(client_parking)
            db.session.commit()
            return (f"клиент id = {client_id} "
                    f"выехал с парковки id = {parking_id}"), 204
        else:
            return (f"не выпускаем клиента id = {client_id} "
                    f"с парковки id = {parking_id} "
                    f"так как он не оплатил парковку ")

    return app
