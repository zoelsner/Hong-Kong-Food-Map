# import gmplot
#
# gmap = gmplot.GoogleMapPlotter(37.428, -122.145, 16)
#
# gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=10)
# gmap.scatter(more_lats, more_lngs, '#3B0B39', size=40, marker=False)
# gmap.scatter(marker_lats, marker_lngs, 'k', marker=True)
# gmap.heatmap(heat_lats, heat_lngs)
#
# gmap.draw("mymap.html")
#
# The above method failed to compile. We tried Python2.7 and 3 on two different machines, and tried PyCharm as well as the terminal
# we made sure to install gmplot with pip before all of this and double - triple checked that we had everything
# I suspect there is a bug, or the library is no longer supported
# Thus we decided to use a similar library below:
# source: https://github.com/tcassou/mapsplotlib

from mapsplotlib import mapsplot as mplt
import json
import pandas as pd

original_data = []
lats = []
longs = []
reviews = []
combo = []

with open('../openrice_data.json') as json_data:
    original_data = json.load(json_data)

#get coords
for obj in original_data:
    lats.append(obj['address'][0])
    longs.append(obj['address'][1])

#get num reviews
for obj in original_data:
    num_reviews = 0
    for x in obj['reviews']:
        try:
            num_reviews += int(x)
        except:
            num_reviews += 0
    reviews.append(num_reviews)

# create a combo list for later use
for x in range( len(lats) ):
    temp = (lats[x], longs[x], reviews[x])
    combo.append(temp)

# creating a dataframe, which is required by the library
labels = ['latitude', 'longitude', 'reviews']
df = pd.DataFrame.from_records(combo, columns=labels)

#google maps api key obtained
mplt.register_api_key('AIzaSyBWMZIWfp9p0bdqqDoEuJN3D4IuVKtUttU')

# show heat map of reviews
mplt.heatmap(df['latitude'], df['longitude'], df['reviews'])
