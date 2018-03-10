#encoding=utf8
'''
    __author__ = 'Administrator'
    2016.2.27 20:30 first version
    分词、提取关键字、提取文章主题
'''


import sys
reload(sys)
sys.setdefaultencoding('utf-8')


f_out = open("data/finance_words/eco_out.txt", "w")
word_dict = {}
for line in open("data/finance_words/eco.txt", "r"):
    #print "###" ,line
    if line.find("、") != -1:
        if line[line.find("、"):line.find("（") ].find(" ") != -1:
            line = line[line.find(" ")+ 1:line.find("（") ]
        else:
            line = line[line.find("、") + len("、"):line.find("（") ]
        flag = 0
        for c in line:
            if c.isalpha() == True:
                flag = 1
        if flag == 0 and len(line) > 1 and len(line) < 30:
            word_dict.setdefault(line, 0)

for line in open("data/finance_words/p2p_sentence.txt", "r"):
    if line.find("：") != -1:
        line = line[:line.find("：")]
        while line[0] == " ": line = line[1:]
        while line[-1] == " ": line = line[:-1]
        while line[:len("　")] == "　": line = line[len("　"):]
        print line
        m = 0
        sep_list  = [".","．","、"," "]
        for sep in sep_list:
            if line.find(sep) != -1:
                m = max(m, line.find(sep) + len(sep))
        if m > 0:
            if line.find("（") == -1:
                line = line[m:]
        if line.find("（") != -1:
            line = line[:line.find("（")]
        while line[0] == " ": line = line[1:]
        while line[-1] == " ": line = line[:-1]
        while line[:len("　")] == "　": line = line[len("　"):]
        if len(line) > 1 and len(line) < 30:
            word_dict.setdefault(line, 0)

for key in word_dict:
    f_out.write( "%s 100\n" %(key))

