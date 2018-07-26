# -*- coding: utf-8 -*-
import json
import math
import ast
import sys

class Food_Search_Engine:
    # original data from crawled json file
    original_data = []
    # the result after filter/ranking
    query_result = []

    def __init__(self, json_file_name):
        self.load_data(json_file_name)
        self.reset()

    def load_data(self, json_file_name):
        with open(json_file_name) as json_data:
            self.original_data = json.load(json_data)
        #print(self.original_data[len(self.original_data) - 2])

    def reset(self):
        self.query_result = list(self.original_data) # need to address this!

    def clear_result(self):
        self.query_result = []

    def filter(self, filter_cond):
        self.clear_result()

        #alters the key slightly, because in the obj, we use an underscore not a hyphen
        if 'price-range' in filter_cond:
            filter_cond['price_range'] = filter_cond.pop('price-range')

        keys = filter_cond.keys()
        print("Query: ")
        print(filter_cond)
        print("searching to match the %s" % keys)
        print("\n")



        # self.original_data is a JSON LIST of DICTIONARIES
        for obj in self.original_data:
            flag = True
            for x in range( len(keys) ):

                if keys[x] is 'cuisine':
                    obj_cuisines = []
                    for z in range( len(obj[keys[x]]) ) : obj_cuisines.append(obj[keys[x]][z].encode('utf-8'))

                    # converting filter list to lower case
                    filter_cond_keys = []
                    for z in range( len(filter_cond[keys[x]]) ) :
                        filter_cond_keys.append(filter_cond[keys[x]][z].lower())

                    # if there is no intersection of the two lists
                    if set(obj_cuisines).isdisjoint(filter_cond_keys) :
                        flag = False

                elif keys[x] == 'price_range':
                    # gets an array with [lower_end, upper_end]
                    criteria = filter_cond[keys[x]].split("-")
                    criteria_lower = criteria[0]
                    criteria_upper = criteria[1]

                    if ("above" in obj[keys[x]]):
                        obj_range_u = obj[keys[x]].replace("$","").split(" ")
                        obj_range_u[0] = obj_range_u[1]
                        obj_range_u[1] = str(1000)
                    elif ("below" in obj[keys[x]]):
                        obj_range_u = obj[keys[x]].replace("$","").split(" ")
                        obj_range_u[0] = str(0)
                    else:
                        obj_range_u = obj[keys[x]].replace("$","").split("-")

                    obj_range = []
                    for z in range( len(obj_range_u) ) : obj_range.append(obj_range_u[z].encode('utf-8'))
                    ##print("restaurant price: ")
                    ##print(obj_range)
                    obj_lower = obj_range[0]
                    obj_upper = obj_range[1]
                    if not (criteria_lower <= obj_lower) :
                        flag = False
                    if not (criteria_upper >= obj_upper) :
                        flag = False

                elif (keys[x] == 'name') or (keys[x] == 'district') :
                    filter_cond_keys = []
                    for z in range ( len(filter_cond[keys[x]]) ) :
                        filter_cond_keys.append( filter_cond[keys[x]][z].lower().replace(" ","") )

                    if obj[keys[x]].lower().replace(" ","") not in filter_cond_keys:
                        flag = False

                elif keys[x] == 'name_contains':
                    filter_cond_keys = []
                    for z in range( len(filter_cond[keys[x]]) ):
                        filter_cond_keys.append( filter_cond[keys[x]][z].lower().replace(" ","") )
                    ismatch = False
                    for z in range( len(filter_cond_keys) ):
                         if filter_cond_keys[z] in obj['name'].lower().replace(" ","").encode("utf-8") :
                             ismatch = True
                    if not ismatch:
                        flag = False


                # in some cases, results have NO reviews
                elif keys[x] == 'rating':
                    try:
                        if float(obj[keys[x]]) < float(filter_cond[keys[x]]):
                            flag = False
                    except:
                        rating = 0
                        if rating < float(filter_cond[keys[x]]):
                            flag = False




            if flag is False:
                continue;
            #print("match! ")

            #print("\n")
            self.query_result.append(obj)

    # v1 = rating
    # v2 = norm_distance
    # v3 = av_price
    # v4 = ratio of bad
    def get_vector(self, obj):
        v = []
        try:
            float(obj['rating'])
            v.append(obj['rating']) #rating
        except:
            v.append(0)
        SHB_lat = 22.417875
        SHB_lng = 114.207263
        lat = obj['address'][0]
        lng = obj['address'][1]
        v.append(math.sqrt(pow((SHB_lat - lat),2) + pow((SHB_lng - lng),2))) #norm_distance
        if "above" in obj['price_range']:
            price = obj['price_range'].replace("$","").split(" ")
            price_low = int(price[1]) #price[0] = "Above" price [1] = "800"
            price_high = 1000 # set from specs
        elif "below" in obj['price_range']:
            price = obj['price_range'].replace("$","").split(" ")
            price_high = int(price[1]) #price[0] = "Below" price [1] = "50"
            price_low = int(0) # set from specs
        else:
            price_range = obj['price_range'].replace("$","").split("-")
            price_low = int(price_range[0])
            price_high = int(price_range[1])
        v.append((price_low + price_high) / 2) #average price
        try: num_good = int(obj['reviews'][0])
        except: num_good = 0.0
        try: num_ok = int(obj['reviews'][1])
        except: num_ok = 0.0
        try: num_bad = int(obj['reviews'][2])
        except: num_bad = 0.0
        if (num_good == 0) and (num_ok == 0) and (num_bad == 0):
            v.append(1.0)
        else:
            v.append(float(num_bad) / (num_bad + num_ok + num_good)) # ratio of bad
        return v

    def swap(self, A, x, y ):
      tmp = A[x]
      A[x] = A[y]
      A[y] = tmp

    def rank(self, ranking_weight):

        for obj in self.query_result:
            v = self.get_vector(obj)
            rw = []
            for x in range(len(ranking_weight)):
                rw.append(ranking_weight[x])
            try:
                obj['score'] = float(rw[0]*v[0]) + float(rw[1]*v[1]) + float(rw[2]*v[2]) + float(rw[3]*v[3])
            except:
                obj['score'] = float(rw[0]*1) + float(rw[1]*v[1]) + float(rw[2]*v[2]) + float(rw[3]*v[3])

        for i in range( len( self.query_result ) ):
            for k in range( len( self.query_result ) - 1, i, -1 ):
                if ( self.query_result[k]['score'] > self.query_result[k - 1]['score'] ):
                    self.swap( self.query_result, k, k - 1 )

    def similarity(self,a,b,sw):
        a = self.get_vector(a)
        b = self.get_vector(b)
        return sw[0]*abs(float(a[0]) - float(b[0])) + sw[1]*abs(float(a[1]) - float(b[1])) + sw[2]*abs(float(a[2]) - float(b[2])) + sw[3]*abs(float(a[3]) - float(b[3]))

    def find_similar(self, restaurant, similiarity_weight, k):

        # calculate similarity for each restaurant
        for obj in self.original_data:
            obj['s_index'] = self.similarity(obj, restaurant, similiarity_weight)

        # sort the data set in order of most similar (smallest number) to least similar (largest number)
        for i in range( len( self.original_data ) ):
            for x in range( len( self.original_data ) - 1, i, -1 ):
              if ( self.original_data[x]['s_index'] < self.original_data[x - 1]['s_index'] ):
                self.swap( self.original_data, x, x - 1 )

        result_array = []
        i = 1
        for obj in self.original_data:
            if i > k:
                break
            i += 1
            result_array.append(self.original_data[i - 1])
        return result_array

    def print_query_result(self):
        print('Overall number of query_result: %d' % len(self.query_result))
        for restaurant in self.query_result:
            v = self.get_vector(restaurant)
            print(restaurant)
            # print(restaurant['name'])
            # print(v[0])
            # print(v[3])
            print(" ")
        #print("\n")

newSearch = Food_Search_Engine('../openrice_data.json');
two = {'name_contains': ['Chan Kun', 'Pai Dong'], 'district': 'Shatin','rating': 3.0, 'cuisine': ['Guangdong', 'Indian']}

one = {'cuisine': ['Japanese', 'American', 'Italian', 'Stir-Fry'],
'price-range': '51-200', 'district': 'Sha Tin', 'name': ['M3 Italian',
'Sha Tin 18'],'name_contains': 'a', 'rating': 3.5}

three = {
'name_contains': ['Chan Kun', 'Pai Dong', 'yuet', 'dim sum'],
'district': ['sHatin','Mong Kok'],
'rating': 3.5,
'cuisine': ['Guangdong', 'Indian'],
'price-range': '$50-100'
}

four = {
'cuisine': ['Japanese'], 'district': ['Sha Tin'], 'price-range': '$50-200'
}


newSearch.filter(four)
newSearch.rank([1,0,0,0.9])
newSearch.print_query_result()
# above functions work perfectly

#print(newSearch.find_similar(newSearch.query_result[0], [0,-1,0,0],100))
