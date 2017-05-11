# -*- coding: utf8 -*-
# import modules & set up logging
import gensim, logging, os

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()


sentences = MySentences('../data-filter/result/')  # a memory-friendly iterator
model = gensim.models.Word2Vec(sentences, size= 600, min_count=2)
model.train(sentences)
model.wv.save_word2vec_format('vector.txt', binary = False)