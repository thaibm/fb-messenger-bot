#!/usr/bin/python
# -*- coding: utf8 -*-
# import gensim, glob, os
import math
import operator
import re
import string
import time
from collections import Counter

import numpy as np
from pyemd import emd
from sklearn.metrics import euclidean_distances

# wv = gensim.models.KeyedVectors.load_word2vec_format("../nlp/word2vec/vector.txt",
#                                                      binary=False)
# shape = wv.syn0.shape
# if not os.path.exists("data/embed_vn.dat"):
#     print("Caching word embeddings in memmapped format...")
#
#     fp = np.memmap("data/embed_vn.dat", dtype=np.double, mode='w+', shape=shape)
#     fp[:] = wv.syn0[:]
#     with open("data/embed_vn.vocab", "w", encoding='utf-8') as f:
#         for _, w in sorted((voc.index, word) for word, voc in wv.vocab.items()):
#             print(w, file=f)
#     del fp, wv

shape = (17900, 600)
size = 600
path = "wmd/"
# path = ""
W = np.memmap(path + "data/embed_vn.dat", dtype=np.double, mode="r",
              shape=shape)

with open(path + "data/embed_vn.vocab", encoding='utf-8') as f:
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


# if not os.path.exists("data/Xd.dat"):
#     print("Caculate Xd.dat...")
#
#     list_docs = []
#     with open("../nlp/data-filter/result/data_filter_sw.txt", "r") as filename:
#         for line in filename:
#             line = line.strip()
#             if line != '':
#                 list_docs.append(line)
#     # list_docs = sorted(list_docs)
#     # print(list_docs[10])
#     X_dict = []
#     for i in range(0, len(list_docs)):
#         X_dict.append(get_xd(list_docs[i]))
#     fp = np.memmap("data/Xd.dat", dtype=np.double, mode='w+',
#                    shape=(len(list_docs), size))
#     fp[:] = X_dict[:]
#
#     with open("data/list_doc.vocab", "w", encoding='utf-8') as f:
#         for doc in list_docs:
#             print(doc, file=f)
#     del fp

with open(path + "data/list_doc.vocab", encoding='utf-8') as f:
    list_docs = f.read().splitlines()
doc_dict = {doc: k for k, doc in enumerate(list_docs)}

x_matrix = np.memmap(path + "data/Xd.dat", dtype=np.double, mode="r",
                     shape=(len(list_docs), size))

# Get stop-words
SW = set()
for line in open(path + 'vn_stopword.txt'):
    line = line.strip()
    if line != '':
        SW.add(line)
stop_words = list(SW)


def WMD(docs_1, docs_2):
    ds1 = docs_1.split()
    ds2 = docs_2.split()
    list_doc_1 = [word for word in ds1 if word in vocab_dict]
    list_doc_2 = [word for word in ds2 if word in vocab_dict]

    vect_1 = Counter(list_doc_1)
    vect_2 = Counter(list_doc_2)
    vect = Counter(list_doc_1 + list_doc_2)
    vect = sorted(vect.keys())
    v_1 = []
    v_2 = []
    for key in vect:
        if vect_1[key] is not None:
            v_1.append(vect_1[key])
        else:
            v_1.append(0)
        if vect_2[key] is not None:
            v_2.append(vect_2[key])
        else:
            v_2.append(0)

    v_1 = np.ravel(v_1)
    v_1 = np.divide(v_1, v_1.sum())
    v_2 = np.ravel(v_2)
    v_2 = np.divide(v_2, v_2.sum())

    W_ = W[[vocab_dict[w] for w in vect]]
    D_ = euclidean_distances(W_)
    D_ = D_.astype(np.double)
    D_ /= D_.max()

    return emd(v_1, v_2, D_)


def WCD(document):
    x1 = get_xd(document)

    temple = np.matrix(x_matrix) * (np.matrix(x1).transpose())
    results = {}
    for doc in list_docs:
        results[doc_dict[doc]] = math.sqrt(
            math.fabs(np.linalg.norm(x1) ** 2
                      - 2 * temple[doc_dict[doc]]
                      + np.linalg.norm(
                x_matrix[doc_dict[doc]]) ** 2))

    results = sorted(results.items(), key=operator.itemgetter(1))
    return results


def __rwmd(docs_1, docs_2):
    ds1 = docs_1.split()
    ds2 = docs_2.split()
    list_doc_1 = [word for word in ds1 if word in vocab_dict]
    list_doc_2 = [word for word in ds2 if word in vocab_dict]
    vect_1 = Counter(list_doc_1)
    vect_2 = Counter(list_doc_2)

    matrix_1 = W[[vocab_dict[w] for w in vect_1.keys()]]
    matrix_2 = W[[vocab_dict[w] for w in vect_2.keys()]]

    # Calculate word frequency
    v1 = list(vect_1.values())
    v1 = np.ravel(v1)
    v1 = np.divide(v1, v1.sum())

    v2 = list(vect_2.values())
    v2 = np.ravel(v2)
    v2 = np.divide(v2, v2.sum())

    d1_ = euclidean_distances(matrix_1, matrix_2)
    d1_min = np.amin(d1_, axis=1)

    d2_ = euclidean_distances(matrix_2, matrix_1)
    d2_min = np.amin(d2_, axis=1)

    return max(np.dot(d1_min, v1), np.dot(d2_min, v2))


def knn(k, input_doc):
    result = re.sub('\W+', ' ', input_doc.lower()).strip()
    repl = ['muốn đọc sách của nhà văn', 'muốn tìm sách của nhà văn',
            'thích đọc sách của nhà văn', 'muốn sách của nhà văn',
            'thích sách của nhà văn', 'muốn đọc sách của', 'muốn tìm sách của',
            'thích đọc sách của', 'muốn sách của', 'thích sách của', 'có thể',
            'được không', 'được không ạ', 'sách của', 'vài']
    for element in repl:
        result = result.replace(element, "")
    result = " ".join([word for word in result.split() if
                       word in vocab_dict and word not in stop_words])

    if len(result) == 0:
        return []

    wcd = WCD(result)

    return wcd[:k]

    # wmd_k_doc = {}
    # count = 1
    #
    # min_rwmd = __rwmd(list_docs[wcd[0][0]], input_doc)
    # for i in range(0, len(wcd)):
    #     if count <= k:
    #         wmd_k_doc[wcd[i][0]] = WMD(list_docs[wcd[i][0]], input_doc)
    #         rwmd_temp = __rwmd(list_docs[wcd[i][0]], input_doc)
    #         min_rwmd = rwmd_temp if min_rwmd > rwmd_temp else min_rwmd
    #     else:
    #         _rwmd = __rwmd(list_docs[wcd[i][0]], input_doc)
    #         if _rwmd < min_rwmd:
    #             wmd_k_doc[wcd[i][0]] = WMD(list_docs[wcd[i][0]], input_doc)
    #     count += 1
    #
    # wmd_k_doc = sorted(wmd_k_doc.items(), key=operator.itemgetter(1))
    #
    # return wmd_k_doc[:k]


def main():
    d1 = "giết con chim nhại"

    d2 = "gỏi salad và các món khai vị tái bản cẩm tuyết sách tiếng việt sách kinh tế gỏi salad và các món khai vị mục lục 1 salad rau củ xốt mayonnais 2 salad rau câu măng tây 3 salad nga 4 salad hải sản 5 salad heo quay 6 salad cà chua cá thu 7 salad tôm hấp tỏi 8 salad tôm cà ri 9 nghêu trộn măng tây với xốt mù tạt 10 salad chả chiên 50 bò bốp thấu 51 heo bốp thấu 52 bao tử bóp rau răm 53 bò nhúng giấm 54 tai mũi heo ngâm giấm 55 bò ngâm giấm 56 dồi thịt 57 giò thủ 58 chả lụa 59 jam bon 60 pa tê tư vấn gia chánh"

    d3 = "harry potter và đứa trẻ bị nguyền rủa phần một và hai j k rowling jack thorne john tiffany sách tiếng việt sách văn học văn học nước ngoài harry potter và đứa trẻ bị nguyền rủa phần một và hai kịch bản harry potter và đứa trẻ bị nguyền rủa được viết dựa trên câu chuyện của j k rowling jack thorne và john tiffany từ những nhân vật quen thuộc trong bộ harry potter kịch bản nói về cuộc phiêu lưu của những hậu duệ sự can thiệp vào dòng thời gian đã gây ra những thay đổi không ngờ cho tương lai tưởng chừng đã yên ổn sau khi vắng bóng chúa tể voldermort"
    t1 = time.time()
    print(knn(20, d1))
    # print(__rwmd(d1, d2))
    print(WCD(d1)[:20])
    print(time.time() - t1)


if __name__ == '__main__':
    main()
