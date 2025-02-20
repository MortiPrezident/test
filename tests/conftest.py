import pytest
from test.main.app import create_app, db as _db
from test.main.models import Client, Parking, ClientParking
from datetime import datetime

"""
Создайте фикстуры в файле conftest.py:
app — приложение, внутри фикстуры опишите создание тестового клиента,
парковки и парковочного лога с фиксацией времени въезда и выезда.
client — клиент, для запросов к приложению.
db — для работы с БД.

"""


@pytest.fixture
def app():
    _app = create_app()
    _app.config['TESTING'] = True
    _app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"

    with _app.app_context():
        _db.create_all()
        client = Client(
            name="Oleg",
            surname="Kaneman",
            credit_card="88002553535",
            car_number="a663ue"

    )
        client_2 = Client(
            name="Oleg_2",
            surname="Kaneman_2",
            credit_card="88010553535",
            car_number="a613ue"

        )
        parking = Parking(
            address="voronezh",
            opened=True,
            count_places=5,
            count_available_places=2

        )
        client_parking = ClientParking(
            client_id=1,
            parking_id=1,
            time_in=datetime.now()

        )
        _db.session.add(client)
        _db.session.add(client_2)
        _db.session.add(parking)
        _db.session.add(client_parking)
        _db.session.commit()
        yield _app
        _db.session.close()
        _db.drop_all()

@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture()
def db(app):
    with app.app_context():
        yield _db