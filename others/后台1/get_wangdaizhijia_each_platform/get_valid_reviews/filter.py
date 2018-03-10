import json

data = json.load(open('all_platform_reviews.json', 'r'))
for each in data:
    for item in data[each]['reviews']:
        temp = sorted(data[each]['reviews'][item]['labels'].items(), key=lambda x: x[1], reverse=True)
        temp = [temp_label[0] for temp_label in temp[:5]]
        data[each]['reviews'][item]['labels'] = temp
        # print each
        # print data[each]['reviews'][item]['labels']
        data[each]['reviews'][item]['comments'] = data[each]['reviews'][item]['comments'][:90]
        print len(data[each]['reviews'][item]['comments'])
json.dump(data, open('platform_reviews_v5.json', 'w'))
