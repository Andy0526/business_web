#encoding=utf8
'''
    __author__ = 'Administrator'
    2016.2.27 20:30 first version
    训练主题模型
'''
import csv
import json
import time
import re
from string import punctuation,digits,letters,whitespace
import sys
import datetime
import jieba
import jieba.analyse
import pandas as pd
from gensim import corpora,models
from helper.textprocessing import handleContent

reload(sys)
sys.setdefaultencoding('utf-8')
jieba.load_userdict("C:/Python27/Lib/site-packages/jieba-0.37-py2.7.egg/jieba/financedict.txt")








print "before load date", datetime.datetime.now()

news_dataset = pd.read_pickle("./data/news_dataset.pkl")
# news_dataset_other = pd.read_pickle("./data/news_dataset_other.pkl")
# all_dataset = pd.concat([news_dataset, news_dataset_other])
all_dataset = news_dataset
print "end load date", datetime.datetime.now()


text_tags = []
lda_train_set = []



## 8000 articles 5mins
print "before cut segments", datetime.datetime.now()
# 分词，关键字提取

for content in all_dataset['content']:
    content = handleContent(content)
    seg = list(jieba.cut(content))
    lda_train_set.append(seg)

print "end cut segments", datetime.datetime.now()


print "before LDA", datetime.datetime.now()
# LDA主题模型
dic = corpora.Dictionary(lda_train_set)
corpus = [dic.doc2bow(text) for text in lda_train_set]
tfidf = models.TfidfModel(corpus)
tfidf.save("./data/tfidf_dict.model")
corpus_tfidf = tfidf[corpus]

# 8000 article 2mins
lda = models.LdaModel(corpus_tfidf, id2word = dic, num_topics = 200)
lda.save("./data/lda.model")
corpus_lda = lda[corpus_tfidf]

for i in range(0, lda.num_topics):
    print i, lda.print_topic(i)

for p in corpus_lda:
    print p

print "end LDA", datetime.datetime.now()


topic_doc_dict = {}
for i in xrange(0 , len(corpus_lda)):
    cnt = 0
    for pp in sorted(corpus_lda[i], lambda a,b: -cmp(a[1], b[1])):
        cnt += 1
        if cnt >= 2: break
        topic_id, weight = pp[0], pp[1],
        topic_doc_dict[topic_id][i] = topic_doc_dict.setdefault(topic_id, {}).setdefault(i, 0) + weight

for topic_id in topic_doc_dict:
    tag_set = {}
    for doc_id in topic_doc_dict[topic_id]:
        for tag in text_tags[doc_id]:
            tag_set[tag] = tag_set.setdefault(tag, 0) + topic_doc_dict[topic_id][doc_id]
    print topic_id, len(tag_set),
    for tag in sorted(tag_set.items(), lambda a,b: -cmp(a[1], b[1])):
        print("%s %s" %(tag[0], tag[1])),
    print ""

