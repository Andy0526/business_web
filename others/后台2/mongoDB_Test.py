#encoder=utf8


from pymongo import MongoClient

client=MongoClient()


db = client.holmesdb

data =  db.t_sh_industry_keywords.find()
for d in data:
    for k in d:
        if k.find("hot") != -1:
            print d["dt"], k, d[k]

