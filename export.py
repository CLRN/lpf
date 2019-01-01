from journey import Journey
from station import Station
import csv

dst = Station.objects(name='City Thameslink')[0]


with open('export.csv', 'w') as csvfile:
    fieldnames = ['name', 'code', 'time', 'dst', 'depart', 'latitude', 'longitude']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for j in Journey.objects(best__lte=20, best__gt=10).order_by('best'):
        latitude, longitude = j.src.parse_location()

        writer.writerow({'name': '[{}] {}'.format(j.best, j.src.name),
                         'code': j.src.code,
                         'time': j.best,
                         'dst': j.dst.name,
                         'depart': j.departure_time,
                         'latitude': latitude,
                         'longitude': longitude})
