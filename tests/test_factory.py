from .factories import ClientFactory, ParkingFactory
from test.main.models import Client, Parking


def test_create_client(db):
    client = ClientFactory()
    db.session.commit()
    assert client.id is not None
    assert len(db.session.query(Client).all()) == 3


def test_create_parking(db):
    parking = ParkingFactory()
    db.session.commit()
    assert parking.id is not None
    assert len(db.session.query(Parking).all()) == 2
