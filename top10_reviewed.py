import matplotlib.pyplot as plt
import numpy as np
import json

# original_data is a LIST of DICTIONARIES
original_data = []
top_ten = []
top_ten_names = []
top_ten_nums = []

#swap helper function
def swap(A, x, y ):
  tmp = A[x]
  A[x] = A[y]
  A[y] = tmp

#open file and import data
with open('openrice_data.json') as json_data:
    original_data = json.load(json_data)

# get num of reviews
for obj in original_data:
    num_reviews = 0
    obj_reviews = []
    try:
        for z in range( len(obj['reviews']) ):
            obj_reviews.append(int(obj['reviews'][z].encode('utf-8')))
    except:
        obj_reviews = [0,0,0]

    for x in range( len(obj_reviews) ):
        num_reviews += obj_reviews[x]
    obj['num_reviews'] = num_reviews

# sort the data set by num of reviews, highest -> lowest
for i in range( len( original_data ) ):
    for k in range( len( original_data ) - 1, i, -1 ):
        if ( original_data[k]['num_reviews'] > original_data[k - 1]['num_reviews'] ):
            swap( original_data, k, k - 1 )

# take the top ten from the sorted data set and push them to top_ten
for x in range(0,10) :
    top_ten.append(original_data[x])

# get top ten names
for x in range( len(top_ten) ):
    top_ten_names.append(top_ten[x]['name'])
#print(top_ten_names)

# get top ten nums
for x in range( len(top_ten) ):
    top_ten_nums.append(top_ten[x]['num_reviews'])
#print(top_ten_nums)

# set up the plot
fig, ax = plt.subplots()

#set y axis interval
y_pos = np.arange(0,1000,100)

#data is top_ten_nums
x = np.array(top_ten_nums)

#display the bar graph
ax.barh(y_pos, x, 85, align='center',color='green')
ax.set_yticks(y_pos)
ax.set_yticklabels(top_ten_names)
ax.invert_yaxis()
ax.set_xlabel('Number of Reviews')
ax.set_title('Top 10 Most Reviewed Restaurants in Sha Tin')
plt.savefig('topten.png',dpi=200,pad_inches=0.5,orientation='landscape')
plt.show()
