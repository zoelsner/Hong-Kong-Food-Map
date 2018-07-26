import numpy as np
import matplotlib.pyplot as plt
import json

original_data = []
prices = []
reviews = []

with open('openrice_data.json') as json_data:
    original_data = json.load(json_data)

# set the mean prices
for obj in original_data:
    temp = obj['price_range']
    if ("above" in temp):
        obj_range_u = temp.replace("$","").split(" ")
        obj_range_u[0] = obj_range_u[1]
        obj_range_u[1] = str(1000)
    elif ("below" in temp):
        obj_range_u = temp.replace("$","").split(" ")
        obj_range_u[0] = str(0)
    else:
        obj_range_u = temp.replace("$","").split("-")
    obj_range = []
    for z in range( len(obj_range_u) ) : obj_range.append(obj_range_u[z].encode('utf-8'))
    obj_mean_prix = (int(obj_range[0]) + int(obj_range[1])) / 2
    obj['mean_prix'] = obj_mean_prix

# set the num of reviews
for obj in original_data:
    num_reviews = 0
    for x in obj['reviews']:
        try:
            num_reviews += int(x)
        except:
            num_reviews += 0


    obj['num_reviews'] = num_reviews

# loop through to collect both data points
for obj in original_data:
    prices.append(obj['mean_prix'])
    reviews.append(obj['num_reviews'])


N = len(prices)
x = prices
y = reviews
colors = np.random.rand(N)

plt.scatter(x, y)
plt.xlabel('Price')
plt.ylabel('Number of Reviews')
plt.show()
