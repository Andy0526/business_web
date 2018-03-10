#encoding=utf8
'''
    __author__ = 'Administrator'
    2016.4.3 21:60 first version
    热门话题提取 single pass + Kmeans
'''
import csv
import json
import os
import time
import re
from string import punctuation,digits,letters,whitespace
import sys
import datetime
from gensim.models.doc2vec import TaggedDocument
import jieba
import math
from helper import myio
import jieba.analyse
import pandas as pd
from sklearn.cluster import KMeans
from gensim import corpora,models
from gensim.models import Word2Vec, Doc2Vec
from helper.textprocessing import handleContent
from helper import nlp_model

reload(sys)
sys.setdefaultencoding('utf-8')
jieba.load_userdict("C:/Python27/Lib/site-packages/jieba-0.37-py2.7.egg/jieba/financedict.txt")

stop_dict = {}
for line in open("C:\Python27\Lib\site-packages\jieba-0.37-py2.7.egg\jieba\stop_chinese.txt"):
    stop_dict.setdefault(line.strip(), 0)






print "before load date", datetime.datetime.now()

news_dataset = pd.read_pickle("./data/news_dataset.pkl")
# news_dataset_other = pd.read_pickle("./data/news_dataset_other.pkl")
# all_dataset = pd.concat([news_dataset, news_dataset_other])
all_dataset = news_dataset
print "end load date", datetime.datetime.now()



class DocIterator(object):
    def __init__(self, documents):
        self.documents = documents

    def __iter__(self):
        for i in xrange(len(self.documents)):
            words = self.documents[i]
            tags = [i]
            yield TaggedDocument(words, tags)

news_list = []
news_feature = []

## 8000 articles 5mins
print "before cut segments", datetime.datetime.now()
# 分词，关键字提取
tfidf_set = []
df_dict = {}
for i in xrange(0, 20000):
    title = all_dataset.iloc[i]['title']
    content = all_dataset.iloc[i]['content']
    doc =  handleContent(title) + " " + handleContent(content)
    tokens = list(jieba.cut(doc))
    new_tokens = []

    for i in xrange( len(tokens) ):
        if tokens[i].isdigit() == True or len(tokens[i]) <= 1\
                or (tokens[i].isalnum() == True and len(tokens[i]) > 20):
             #print tokens[i],
             continue
        if tokens[i] in stop_dict:#去停用词
            continue
        new_tokens.append(tokens[i])
        df_dict[tokens[i]] = df_dict.setdefault(tokens[i], 0) + 1
    tfidf_set.append(new_tokens)
dic = corpora.Dictionary(tfidf_set)
print "the number of word in dicts is %d" %(len(dic))
stems_once = set(stem for stem in df_dict if df_dict[stem] <= 2)
texts = [[token for token in new_tokens if token not in stems_once] for new_tokens in tfidf_set]
dic = corpora.Dictionary(texts)
print "the number of word in dicts is %d" %(len(dic))
corpus = [dic.doc2bow(text) for text in tfidf_set]
tfidf = models.TfidfModel(corpus)
tfidf.save("./data/tfidf_dict.model")
corpus_tfidf = tfidf[corpus]
print "end cut segments", datetime.datetime.now()

doc2vec_model = Doc2Vec.load('./data/doc2vec.model')
for i in xrange(0, len(all_dataset)):
    title = all_dataset.iloc[i]['title']
    content = all_dataset.iloc[i]['content']
    item_pub_time = all_dataset.iloc[i]['item_pub_time']
    if item_pub_time >  '2016-01-15 00:00:00' or item_pub_time < '2015-11-01 00:00:00':
        continue
    news_list.append(all_dataset.iloc[i])
    doc =  handleContent(title) + " " + handleContent(content)
    tokens = list(jieba.cut(doc))
    new_tokens = []

    for i in xrange( len(tokens) ):
        if tokens[i].isdigit() == True or len(tokens[i]) <= 1\
                or (tokens[i].isalnum() == True and len(tokens[i]) > 20):
             #print tokens[i],
             continue
        if tokens[i] in stop_dict:#去停用词
            continue
        new_tokens.append(tokens[i])
    corp = dic.doc2bow(new_tokens)
    tfidf_inv_list = tfidf[corp]
    # print tfidf_inv_list
    tfidf_vec = []
    tfidf_dict = {}
    for pp in tfidf_inv_list:
        tfidf_dict.setdefault(pp[0], pp[1])
    for i in xrange(len(dic)):
        if i in tfidf_dict:
            tfidf_vec.append(tfidf_dict[i])
        else:
            tfidf_vec.append(0)
    vec = list(doc2vec_model.docvecs[i])
    news_feature.append(vec + tfidf_vec)
print len(news_list)


cluster_cnt = 20
kmeans = KMeans(n_clusters=cluster_cnt, random_state=170, max_iter=1000)
cluster_indexs = kmeans.fit_predict(news_feature)
cluster_docs = []
for i in xrange(cluster_cnt):
    cluster_docs.append([])
for i in xrange(len(news_list)):
    cluster_docs[cluster_indexs[i]].append((news_list[i]["item_id"],news_list[i]["title"],news_list[i]["content"], news_list[i]["item_pub_time"]))


keyword_rev_dict = myio.getJsonFile_all("./data/keyword_revise_dict.json")
test_date = datetime.date(2015, 12, 31)
date_begin = datetime.date(2015, 01, 01)
test_date_end = test_date + datetime.timedelta(days=7)

all_date = int(str(test_date - date_begin).split(' ')[0])


cluster_result_f = open("./data/news/hot_topics/hot_event_cluster_result.txt", "w")
for ci in xrange(0, cluster_cnt):
    cluster_result_f.write("%d\n"%ci)
    print ci
    ci_dir_name = "./data/news/hot_topics/%d" %(ci)
    if os.path.exists(ci_dir_name) == False:
        os.mkdir(ci_dir_name)

    keyword_dict = {}
    news_dict_list = []
    new_keyword_list = []
    keyword_list = []
    for (id, title, content, item_pub_time) in cluster_docs[ci]:
        #print "\t", title
        cluster_result_f.write("\t%s\n"%title)
        news_dict_list.append({"_id": id, "title":title, "concent":content, "item_pub_time":item_pub_time})
        title = handleContent(title)
        title_keyword =  list(jieba.cut(title, cut_all=False))
        content = handleContent(content)
        cont_keyword = jieba.analyse.extract_tags(content, topK = 100)
        for kw in title_keyword:
            if  kw.isdigit() == True or len(kw) <= 1:
                continue
            keyword_dict[kw] = keyword_dict.setdefault(kw, 0) + 2
        for kw in cont_keyword:
            if  kw.isdigit() == True or len(kw) <= 1:
                continue
            keyword_dict[kw] = keyword_dict.setdefault(kw, 0) + 1
    ci_news_name = os.path.join(ci_dir_name, "news.json")
    ci_news_f = open(ci_news_name, "w")
    myio.writeJsonDict(news_dict_list, ci_news_f)
    date_dict = {}
    for data in news_dict_list:
        d = data["item_pub_time"].split(" ")[0].replace("-", ".")
        date_dict[d] = date_dict.setdefault(d, 0) + 1
    print sorted(date_dict.items(), lambda a,b: cmp(a[0], b[0]))
    ci_news_date_name = os.path.join(ci_dir_name, "news_date_analyze.json")
    myio.writeJsonDict(date_dict, open(ci_news_date_name, "w"))

    keyword_list = sorted(keyword_dict.items(), lambda a,b:-cmp(a[1], b[1]))
    new_keyword_dict = {}
    for (word, weight) in keyword_list:
        prev_cnt = 0
        if word in keyword_rev_dict:
            for (d, w) in keyword_rev_dict[word]:
                d = datetime.datetime.strptime(d, "%Y-%m-%d")
                d = datetime.date(d.year, d.month, d.day)
                if d < test_date:
                    prev_cnt += 1
                else:
                    break
        weight = weight * 1.0 / all_date * math.log(all_date * 1.0 / (1 + prev_cnt))
        new_keyword_list.append((word, weight))
    new_keyword_list =  sorted(new_keyword_list, lambda a,b: -cmp(a[1], b[1]))[:50]
    ci_keyword_name = os.path.join(ci_dir_name, "keywords.json")
    ci_keyword_f = open(ci_keyword_name, "w")
    for (word, weight) in new_keyword_list:
        new_keyword_dict.setdefault(word, weight)
    myio.writeJsonDict(new_keyword_dict, ci_keyword_f)
    for pp in new_keyword_list:
        print pp[0],pp[1]
