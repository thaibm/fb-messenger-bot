# -*- coding: utf8 -*-

import gensim, logging, os, re


def data_filter(data):
    result = re.sub('\W+', ' ', data.lower().strip())
    return result


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()



desti_file = open("data-new/data_filter.txt", "w")
with open("tiki-new.csv", "r") as f:
    for line in f:
        result = data_filter(line)
        desti_file.write(result + "\n")

# sentences = MySentences('data/')  # a memory-friendly iterator
# model = gensim.models.Word2Vec(sentences, size= 50, min_count=3)
# model.train(sentences)
# model.wv.save_word2vec_format('vector_new.txt', binary = False)