import json

result = []

data = json.load(open('raw_recent_reviews.json', 'r'))
for item in data:
    comment = {}
    labels = []
    if 'platReviewTagList' in item:
        for each in item['platReviewTagList']:
            if 'tagName' in each:
                labels.append(each['tagName'])
    comment['reviewContent'] = item['reviewContent']
    comment['platName'] = item['platName']
    comment['evaluation'] = item['evaluation']
    comment['reviewDate'] = item['reviewDate']
    comment['reviewUserName'] = item['reviewUserName']
    comment['label'] = labels
    result.append(comment)

json.dump(result, open('recent_reviews.json', 'w'))
