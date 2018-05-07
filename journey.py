from station import Station

from mongoengine import Document, ReferenceField, IntField, StringField


class Journey(Document):
    src = ReferenceField(Station, required=True)
    dst = ReferenceField(Station, required=True)
    best = IntField(required=True)
    departure_time = StringField(required=True)

    def __repr__(self):
        return "[{}] {} -> {}".format(self.best, self.src.name, self.dst.name)

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()
