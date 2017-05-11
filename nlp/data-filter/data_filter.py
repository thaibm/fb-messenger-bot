#!/usr/bin/python
# -*- coding: utf8 -*-

import string, re, glob, os

# --------------DEFINE FUNCTIONS----------------------
def removeStopwords(data, filename):
    # result after handle. Ex: result.txt
    output = open(filename, 'w', encoding='utf8')
    lines = data.split('\n')
    # list of stopwords. Ex: vn_stopword.txt
    fileStopword = open('stopwords', 'r', encoding='utf8')
    listStopword = fileStopword.read().split('\n')
    for line in lines:
        line = ' '.join([word for word in line.split() if word not in listStopword and len(str(word)) > 1])
        if len(line.split()) <= 0: continue

        output.write(line + '\n')

def data_filter(data):
    result = re.sub('\W+', ' ', data.lower().strip())
    return result

desti_file = open("result/data_filter_sw.txt", "w")
with open("tiki.csv", "r") as f:
    for line in f:
        result = data_filter(line)
        desti_file.write(result + "\n")