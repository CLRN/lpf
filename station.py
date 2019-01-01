from requests_html import HTMLSession
from mongoengine import Document, connect, StringField

connect("lpf")


class Station(Document):
    name = StringField(required=True)
    location = StringField()
    code = StringField(required=True)

    def __repr__(self):
        return "[{}] {}".format(self.code, self.name)

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()


class StationList:
    def __init__(self):
        self.session = HTMLSession()
        self.url = 'https://en.wikipedia.org/wiki/List_of_London_railway_stations'
        self.stations = list()

        if not len(Station.objects):
            self.save()
        self.load()

    def load(self):
        self.stations = [x for x in Station.objects]

    def save(self):
        response = self.session.get(self.url)
        for row in response.html.find('tr'):
            if len(row.links) == 1:
                continue

            data = [r.strip() for r in row.text.split('\n')]
            if len(data) < 8:
                continue

            if len(data[3]) != 3:
                continue

            if data[0].endswith('London'):
                data[0] = data[0][:len(data[0]) - len('London')]
            if data[0].endswith(']'):
                end = data[0].rfind('[')
                data[0] = data[0][:end]
            Station(name=data[0], location=data[7], code=data[3]).save()


if __name__ == '__main__':
    l = StationList()
    print(l.stations)


