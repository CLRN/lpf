from journey import Journey
from station import StationList, Station
from requests_html import HTMLSession
from datetime import datetime


class TimeResults:
    def __init__(self, pages):
        self.pages = pages

    def diff(self, dep, arr):
        return int((datetime.strptime(arr, '%H:%M') - datetime.strptime(dep, '%H:%M')).total_seconds() / 60)

    def get_best(self):
        fastest = 180
        departure_time = ''

        for page in self.pages:
            for row in page.html.find('tr'):
                data = [r.strip() for r in row.text.split('\n')]
                if len(data) < 6:
                    continue

                try:
                    diff = self.diff(data[0], data[3])
                    if diff < fastest:
                        fastest = diff
                        departure_time = data[0]
                except:
                    pass

        return fastest, departure_time


class Parser:
    def __init__(self, stations, time_range=['0730', '0745', '0800', '0815', '0830'], date='130319'):
        self.stations = stations
        self.time_range = time_range
        self.date = date
        self.url_pattern = 'http://ojp.nationalrail.co.uk/service/timesandfares/{}/{}/{}/{}/dep'
        self.session = HTMLSession()

    def make_url(self, src, dst, time_start):
        return self.url_pattern.format(src, dst, self.date, time_start)

    def run(self):
        all_stations = StationList().stations

        for dst in self.stations:
            for src in all_stations:
                urls = [self.make_url(src.code, dst.code, t) for t in self.time_range]
                pages = [self.session.get(u) for u in urls]
                results = TimeResults(pages)
                fastest, time = results.get_best()

                print("{:<30} -> {:<30}: {} at {}".format(src.name, dst.name, fastest, time))

                Journey(src=src, dst=dst, best=fastest, departure_time=time).save()


if __name__ == '__main__':
    stations = filter(lambda x: x.name in ['London Bridge',
                                           'Cannon Street',
                                           'Blackfriars',
                                           'City Thameslink'], StationList().stations)
    parser = Parser([x for x in stations])
    parser.run()


