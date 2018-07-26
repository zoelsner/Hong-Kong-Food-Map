import numpy as np
import matplotlib.pyplot as plt
import json

original_data = []
reviews = []

with open('openrice_data.json') as json_data:
    original_data = json.load(json_data)

for obj in original_data:
    num_reviews = 0
    for x in obj['reviews']:
        try:
            num_reviews += int(x)
        except:
            num_reviews += 0
    reviews.append(num_reviews)

x = np.array(reviews)

# the histogram of the data
n, bins, patches = plt.hist(x, 50, facecolor='g', alpha=0.75)

plt.xlabel('# of Reviews')
plt.ylabel('# of Restaurants')
plt.title('Distr. of # of Reviews')
#plt.axis([0, 1000, 0, 10])
plt.grid(True)
plt.show()
