import pytest
from test.main.models import Client, Parking


def test_create_client(client):
    client_data = {
    "name": "Oleg1",
    "surname": "Kaneman",
    "credit_card": "88005553535",
    "car_number": "a666ue"

    }
    resp = client.post('/clients', json=client_data)

    assert resp.status_code == 201


def test_create_parking(client):
    parking_data = {
    "address": "voronezh",
    "opened": True,
    "count_places": 5,
    "count_available_places": 2

    }
    resp = client.post('/parking', json=parking_data)

    assert resp.status_code == 201

@pytest.mark.parking_in_and_out
def test_client_parking(client, db):
    client_parking_data = {
    "client_id": 2,
    "parking_id": 1,

    }
    query = db.select(Parking).where(Parking.id == client_parking_data['parking_id'])
    parking = db.session.execute(query).scalar_one_or_none()
    assert True == parking.opened
    count_available_places = parking.count_available_places
    resp = client.post('/client_parking', json=client_parking_data)
    assert count_available_places - parking.count_available_places == 1
    assert resp.status_code == 201

@pytest.mark.parking_in_and_out
def test_client_parking_out(client, db):
    ...
    client_parking_data = {
    "client_id": 1,
    "parking_id": 1,

    }
    query = db.select(Client).where(Client.id == client_parking_data['client_id'])
    client_db = db.session.execute(query).scalar_one_or_none()
    assert True == bool(client_db.credit_card)
    resp = client.delete('/client_parking', json=client_parking_data)
    assert resp.status_code == 204
