#!/usr/bin/python
# -*- coding: utf8 -*-

import string, re, glob, os

# --------------DEFINE FUNCTIONS----------------------
def removeStopwords(data, filename):
    # result after handle. Ex: result.txt
    output = open(filename, 'w', encoding='utf8')
    lines = data.split('\n')
    # list of stopwords. Ex: vnstopword.txt
    fileStopword = open('stopwords', 'r', encoding='utf8')
    listStopword = fileStopword.read().split('\n')
    for line in lines:
        line = ' '.join([word for word in line.split() if word not in listStopword and len(str(word)) > 1])
        if len(line.split()) <= 0: continue

        output.write(line + '\n')

def data_handle(filename):
    source = open(filename, 'r', encoding='utf-8')
    data = source.read()
    source.close()

    # lowercase all the text on the file
    dataLower = data.lower()
    # create new list punctuation
    punctuation = re.sub('_', '', string.punctuation)
    # then add some special characters in Vietnamese to this list
    punctuation += '–“”…'
    # remove all punctuation
    result = re.sub('[%s]' % punctuation, '', dataLower)
    return result

path = ''
for filename in glob.glob(os.path.join(path, '*.txt.uet')):
    result_name = re.sub(path, '', filename)
    result_name = re.sub('.uet', '', result_name)
    destination = 'data-handle.txt'
    result = data_handle(filename)
    removeStopwords(result, destination)