import json

new_plats = json.load(open('platform_search.json', 'r'))
# display_plat = json.load(open('display_platform.json', 'r'))
name_id = {}
for item in new_plats:
    # if item['platName'] in display_plat:
    name_id[item['platName']] = item['platId']
all_reviews = json.load(open('platform_reviews.json', 'r'))

result = {}
for name in name_id:
    result[name] = {
        'reviews': {'0': {'labels': {}, 'comments': []}, '1': {'labels': {}, 'comments': []},
                    '2': {'labels': {}, 'comments': []}}}
    try:
        for each in all_reviews[name_id[name]]['reviews']:
            if 'platReviewTagList' in each:
                if len(each['platReviewTagList']):
                    for item in each['platReviewTagList']:
                        if 'tagName' in item:
                            if 'amp' not in item['tagName']:
                                result[name]['reviews'][each['evaluation']]['labels'][item['tagName']] = \
                                    result[name]['reviews'][each['evaluation']]['labels'].get(item['tagName'], 0) + 1
            try:
                if not 'hellip' in each['reviewContent'] and not 'amp' in each['reviewContent']:
                    result[name]['reviews'][each['evaluation']]['comments'].append(
                        {'content': each['reviewContent'], 'date': each['reviewDate']})
            except:
                continue
    except:
        continue

json.dump(result, open('all_platform_reviews.json', 'w'))
