from station import StationList
from zoopla import Zoopla
from zoopla.exceptions import ZooplaAPIException
import os

zoopla = Zoopla(api_key=os.environ['ZOOPLA_KEY'], verbose=True)

for station in StationList().stations:
    name = '{} Station'.format(station.name)
    latitude, longitude = station.parse_location()

    try:
        prices = zoopla.average_area_sold_price({
            'latitude': str(latitude),
            'longitude': str(longitude),
            'order': 'ascending',
            'page_number': 1,
            'page_size': 1
        })
    except ZooplaAPIException as e:
        print(e)
        continue

    print(prices)


#
# for result in search.listing:
#     print(result.price)
#     print(result.description)
#     print(result.image_url)
#
# for j in Journey.objects().order_by('best'):
#     print(j)
#
