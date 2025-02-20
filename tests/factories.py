import factory
import random
from test.main.app import db
from test.main.models import Client, Parking


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    credit_card = factory.Maybe(
        factory.Faker("boolean", chance_of_getting_true=70),
        yes_declaration=factory.LazyFunction(
            lambda: "".join([str(random.randint(0, 9)) for _ in range(10)])
        ),
        no_declaration=None,
    )
    car_number = factory.Faker("license_plate")


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker("address")
    opened = factory.LazyFunction(lambda: random.choice([True, False]))
    count_places = factory.LazyFunction(lambda: random.randint(20, 100))

    @factory.lazy_attribute
    def count_available_places(self):
        return random.randint(0, self.count_places)
