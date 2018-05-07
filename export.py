from journey import Journey
import csv
import string


def parse_location(input):
    input = ''.join(filter(lambda x: x in string.printable, input))
    input = [s.strip() for s in input.split('/')][-1]
    parts = [s.strip().strip(';') for s in input.split(' ')]
    return float(parts[0]), float(parts[1])


with open('export.csv', 'w') as csvfile:
    fieldnames = ['name', 'code', 'time', 'dst', 'depart', 'latitude', 'longitude']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for j in Journey.objects(best__lte=60, best__gt=50).order_by('best'):
        latitude, longitude = parse_location(j.src.location)

        writer.writerow({'name': '[{}] {}'.format(j.best, j.src.name),
                         'code': j.src.code,
                         'time': j.best,
                         'dst': j.dst.name,
                         'depart': j.departure_time,
                         'latitude': latitude,
                         'longitude': longitude})
