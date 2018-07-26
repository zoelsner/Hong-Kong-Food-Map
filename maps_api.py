import requests
from mapsplotlib import mapsplot as mplt
import numpy as np
import json
import pandas as pd

original_data = []
lats = []
longs = []
names = []
# combo = []


with open('openrice_data.json') as json_data:
    original_data = json.load(json_data)

#get coords
for obj in original_data:
    lats.append(obj['address'][0])
    longs.append(obj['address'][1])

#get names
for obj in original_data:
    names.append(obj['name'])

# for x in range( len(lats) ):
#     temp = (lats[x], longs[x], reviews[x])
#     combo.append(temp)

# labels = ['latitude', 'longitude', 'reviews']
# df = pd.DataFrame.from_records(combo, columns=labels)

mplt.register_api_key('AIzaSyBWMZIWfp9p0bdqqDoEuJN3D4IuVKtUttU')


## Getting data and filtering
## Please register your key and design the correct query
key = "AIzaSyBWMZIWfp9p0bdqqDoEuJN3D4IuVKtUttU"
query = ""

# you might want a for loop to send and receive the query
url = "https://maps.googleapis.com/maps/api/distancematrix/json?" + query
res = requests.get(url).json()
