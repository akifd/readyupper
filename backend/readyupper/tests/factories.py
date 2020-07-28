import factory

from .. import models


class CalendarFactory(factory.SQLAlchemyModelFactory):
    class Meta:
        model = models.Calendar

    name = factory.Faker("sentence")


class ParticipantFactory(factory.SQLAlchemyModelFactory):
    class Meta:
        model = models.Participant

    calendar = factory.SubFactory(CalendarFactory)
    name = factory.Faker("name")
