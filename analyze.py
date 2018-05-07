from journey import Journey
from zoopla import Zoopla
import os

zoopla = Zoopla(api_key=os.environ['ZOOPLA_KEY'])

search = zoopla.property_listings({
    'maximum_beds': 2,
    'page_size': 100,
    'listing_status': 'sale',
    'area': 'Albany Park Station'
})

for result in search.listing:
    print(result.price)
    print(result.description)
    print(result.image_url)

for j in Journey.objects().order_by('best'):
    print(j)

