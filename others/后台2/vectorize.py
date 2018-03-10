#encoding=utf8
'''
    __author__ = 'Administrator'
    2016.3.3 22:30 first version
    将单词、文章、用户向量化，包括word2vec, doc2vec
'''
import logging
import re
import sys
import datetime
import gensim
from gensim.models.doc2vec import TaggedDocument
import jieba
import pandas as pd
from gensim.models import Word2Vec, Doc2Vec
from helper.textprocessing import handleContent, cut_sentence_2
reload(sys)
sys.setdefaultencoding('utf-8')

stop_dict = {}
for line in open("C:\Python27\Lib\site-packages\jieba-0.37-py2.7.egg\jieba\stop_chinese.txt"):
    stop_dict.setdefault(line.strip(), 0)
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

##Load documents
print "before load date", datetime.datetime.now()

news_dataset = pd.read_pickle("./data/news_dataset.pkl")
news_dataset_other = pd.read_pickle("./data/news_dataset_other.pkl")
all_dataset = pd.concat([news_dataset, news_dataset_other])

print "end load date", datetime.datetime.now()


print "before word2vec", datetime.datetime.now()
documents = []
sentences = []
for i in xrange(0, len(all_dataset)):
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
            #u'数正', '下险企
        #if tokens[i] in[u'融系',u'办则',u'部是', u'若仅', u'虽同', u'或苏', u'由十']:
            #print tokens[i], title, content

        new_tokens.append(tokens[i])
    # for token in new_tokens:
    #     print token,
    # print ""
    # print len(tokens),len(new_tokens)
    documents.append(new_tokens)
    # content = content.replace("#r#", "\r").replace("#n#", "\n").replace("#t#", "\t")
    # sentence_list = [title] + cut_sentence_2(content)
    # for i in xrange(len(sentence_list)):
    #     sentence_list[i] = handleContent(sentence_list[i])
    sentences.append(doc)


## train a word2vec model
num_features = 200      # Word vector dimensionality
min_word_count = 1      # Minimum word count
num_workers = 4         # Number of threads to run in parallel
context = 10            # Context window size
downsampling = 1e-5     # Downsample setting for frequent words

print "Training Word2Vec model...", datetime.datetime.now()
model = Word2Vec(documents, \
                 workers=num_workers,\
                 size=num_features,\
                 min_count=min_word_count,\
                 window=context, \
                 sample=downsampling,\
                 seed=1)

model.init_sims(replace=True)
model.save('./data/word2vec.model')
print "here"
for pp in model.most_similar(["陆金所".decode("utf8")],topn=30):
    print pp[0], pp[1], "\t",
print ""
for pp in model.most_similar(["P2P".decode("utf8")],topn=30):
    print pp[0], pp[1], "\t",
print ""
for pp in model.most_similar(["网贷".decode("utf8")],topn=30):
    print pp[0], pp[1], "\t",
print ""
for pp in model.most_similar(["e租宝".decode("utf8")],topn=30):
    print pp[0], pp[1], "\t",
print ""
print "end word2vec", datetime.datetime.now()


print "before doc2vec", datetime.datetime.now()
class DocIterator(object):
    def __init__(self, documents):
        self.documents = documents

    def __iter__(self):
        for i in xrange(len(self.documents)):
            words = self.documents[i]
            tags = [i]
            yield TaggedDocument(words, tags)

## train a doc2vec model
print "Training DocVec model..."
model = Doc2Vec(DocIterator(documents), \
                size=100, \
                window=8, \
                min_count=5,\
                workers=4)
model.init_sims(replace=True)
model.save('./data/doc2vec.model')
print "end doc2vec", datetime.datetime.now()
