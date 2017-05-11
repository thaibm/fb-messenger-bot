#!/usr/bin/python
# -*- coding: utf8 -*-
import gensim, glob, os
from collections import Counter
import numpy as np

wv = gensim.models.KeyedVectors.load_word2vec_format("../nlp/vector.txt",
                                                     binary=False)
shape = wv.syn0.shape
if not os.path.exists("data/embed_vn.dat"):
    print("Caching word embeddings in memmapped format...")

    fp = np.memmap("data/embed_vn.dat", dtype=np.double, mode='w+', shape=shape)
    fp[:] = wv.syn0[:]
    with open("data/embed_vn.vocab", "w", encoding='utf-8') as f:
        for _, w in sorted((voc.index, word) for word, voc in wv.vocab.items()):
            print(w, file=f)
    del fp, wv

size = 600
# path = "wmd/"
path = ""
W = np.memmap(path+"data/embed_vn.dat", dtype=np.double, mode="r", shape=shape)

with open(path+"data/embed_vn.vocab", encoding='utf-8') as f:
    vocab_list = map(str.strip, f.readlines())
vocab_dict = {w: k for k, w in enumerate(vocab_list)}


def get_xd(document):
    # Matrix of document
    ds = document.split()
    list_doc = [word for word in ds if word in vocab_dict]
    vect = Counter(list_doc)

    input_vector_matrix = W[[vocab_dict[w] for w in vect.keys()]]
    # Calculate word frequency
    v = list(vect.values())
    v = np.ravel(v)
    frequency = np.divide(v, v.sum())
    # Calculate di*xi
    input_vector = []
    for i in range(0, len(input_vector_matrix)):
        input_vector.append(
            np.multiply(input_vector_matrix[i], frequency[i]))

    X = np.sum(input_vector, axis=0)
    return X

if not os.path.exists("data/Xd.dat"):
    print("Caculate Xd.dat...")

    list_docs = []
    with open("../nlp/data/data_filter.txt", "r") as filename:
        for line in filename:
            line = line.strip()
            if line != '':
                list_docs.append(line)

    X_dict = []
    for i in range(0, len(list_docs)):
        X_dict.append(get_xd(list_docs[i]))
    fp = np.memmap("data/Xd.dat", dtype=np.double, mode='w+',
                   shape=(len(list_docs), size))
    fp[:] = X_dict[:]

    with open("data/list_doc.vocab", "w", encoding='utf-8') as f:
        for doc in list_docs:
            print(doc, file=f)
    del fp
