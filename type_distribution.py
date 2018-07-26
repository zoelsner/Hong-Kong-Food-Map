import matplotlib.pyplot as plt
import json

original_data = []
top_five_types = []
top_five_nums = []
types = set()
type_count = {}
others = 0

with open('openrice_data.json') as json_data:
    original_data = json.load(json_data)

#take out everything thats not mong kok
for obj in original_data:
    if obj['district'] is not "Mong Kok":
        original_data.remove(obj)

for obj in original_data:
    for x in obj['cuisine']:
        types.add(x)

for typ in types:
    type_count[typ] = 0

for obj in original_data:
    for x in obj['cuisine']:
        for key in type_count:
            if str(key) == str(x):
                type_count[key] += 1

x = 0;
start = 5;
end = 10;
for key in sorted(type_count, key=type_count.get, reverse = True):
    print("x: ", x)
    if (x >= start) and (x < end):
        others += type_count[key]
        print("adding", key, type_count[key])
    elif x >= end:
        break
    else:
        print("skipping", key, type_count[key])
    x += 1

x = 0;
end = 5;
for key in sorted(type_count, key=type_count.get, reverse = True):
    if x == end:
        top_five_types.append("Others")
        top_five_nums.append(others)
        break;
    top_five_types.append(key)
    top_five_nums.append(type_count[key])
    x += 1

for x in range( len(top_five_types) ):
    print(top_five_types[x])
    print(top_five_nums[x])



# Data to plot

labels = top_five_types
sizes = top_five_nums
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'purple', 'red']

# Plot
plt.pie(sizes, labels=labels, colors=colors,
        autopct='%1.1f%%')

plt.axis('equal')
plt.show()
