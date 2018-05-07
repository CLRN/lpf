from station import Station

from mongoengine import Document, ReferenceField, IntField, StringField


class Journey(Document):
    src = ReferenceField(Station, required=True)
    dst = ReferenceField(Station, required=True)
    best = IntField(required=True)
    departure_time = StringField(required=True)
