#!/usr/bin/python
# -*- coding: utf8 -*-

import os, glob, math, operator, re, string
# import gensim
import numpy as np
from pyemd import emd
from scipy.spatial.distance import cosine
from sklearn.metrics import euclidean_distances
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter

# wv = gensim.models.KeyedVectors.load_word2vec_format("../nlp/word2vec/vector.txt",
#                                                      binary=False)
# shape = wv.syn0.shape
# if not os.path.exists("data/embed_vn.dat"):
#     print("Caching word embeddings in memmapped format...")
#
#     fp = np.memmap("data/embed_vn.dat", dtype=np.double, mode='w+', shape=shape)
#     fp[:] = wv.syn0[:]
#     with open("data/embed_vn.dat.vocab", "w", encoding='utf-8') as f:
#         for _, w in sorted((voc.index, word) for word, voc in wv.vocab.items()):
#             print(w, file=f)
#     del fp, wv

global W, vocab_dict, stop_words
shape = (11967, 300)

W = np.memmap("wmd/data/embed_vn.dat", dtype=np.double, mode="r", shape=shape)

with open("wmd/data/embed_vn.vocab", encoding='utf-8') as f:
    vocab_list = map(str.strip, f.readlines())
vocab_dict = {w: k for k, w in enumerate(vocab_list)}

# Get stop-words
SW = set()
for line in open('wmd/vnstopword.txt'):
    line = line.strip()
    if line != '':
        SW.add(line)
stop_words = list(SW)

def WMD(docs_1, docs_2):
    list_doc_1 = []
    for word in docs_1.split():
        if (word in vocab_dict and word not in stop_words):
            list_doc_1.append(word)

    list_doc_2 = []
    for word in docs_2.split():
        if (word in vocab_dict and word not in stop_words):
            list_doc_2.append(word)

    vect_1 = Counter(list_doc_1)
    vect_2 = Counter(list_doc_2)
    vect = Counter(list_doc_1 + list_doc_2)
    vect = sorted(vect.keys())
    v_1 = []
    v_2 = []
    for key in vect:
        if vect_1[key] != None:
            v_1.append(vect_1[key])
        else:
            v_1.append(0)
        if vect_2[key] != None:
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

    return emd(v_1, v_2, D_)

def get_Xd(document):
    # Matrix of document
    list_doc = []
    for word in document.split():
        if word in vocab_dict and word not in stop_words:
            list_doc.append(word)
    vect = Counter(list_doc)

    input_vector_matrix = W[[vocab_dict[w] for w in vect.keys()]]
    # Caculate word frequency
    v = list(vect.values())
    v = np.ravel(v)
    frequency = np.divide(v, v.sum())
    # Caculate di*xi
    input_vector = []
    for i in range(0, len(input_vector_matrix)):
        input_vector.append(
            np.multiply(input_vector_matrix[i], frequency[i]))

    X = np.sum(input_vector, axis=0)
    return X

def WCD(document):
    X1 = get_Xd(document)

    if not os.path.exists("wmd/data/Xd.dat"):
        print("Caculate Xd.dat...")

        list_docs = []
        path = "../nlp/data-filter/result/"
        for filename in glob.glob(os.path.join(path, '*.txt')):
            for line in open(filename, encoding='utf-8'):
                line = line.strip()
                if line != '':
                    list_docs.append(line)
        # list_docs = sorted(list_docs)
        # print(list_docs[10])
        X_dict = []
        for i in range(0, len(list_docs)):
            X_dict.append(get_Xd(list_docs[i]))
        fp = np.memmap("wmd/data/Xd.dat", dtype=np.double, mode='w+',
                       shape=(len(list_docs), 300))
        fp[:] = X_dict[:]

        with open("wmd/data/list_doc.vocab", "w", encoding='utf-8') as f:
            for doc in list_docs:
                print(doc, file=f)
            del fp

    # with open("data/list_doc.vocab", encoding='utf-8') as f:
    #     doc_list = map(str.strip, f.readlines())
    with open("wmd/data/list_doc.vocab", encoding='utf-8') as f:
        list_docs = f.read().splitlines()
    doc_dict = {doc: k for k, doc in enumerate(list_docs)}

    X_matrix = np.memmap("wmd/data/Xd.dat", dtype=np.double, mode="r",
                         shape=(len(list_docs), 300))

    temple = np.matrix(X_matrix) * (np.matrix(X1).transpose())
    results = {}
    for doc in list_docs:
        results[doc_dict[doc]] = math.sqrt(
            math.fabs(np.linalg.norm(X1) ** 2
                      - 2 * temple[doc_dict[doc]]
                      + np.linalg.norm(
                X_matrix[doc_dict[doc]]) ** 2))

    results = sorted(results.items(), key=operator.itemgetter(1))
    return results

def RWMD(docs_1, docs_2):

    list_doc_1 = []
    for word in docs_1.split():
        if word in vocab_dict and word not in stop_words:
            list_doc_1.append(word)
    vect_1 = Counter(list_doc_1)

    list_doc_2 = []
    for word in docs_2.split():
        if word in vocab_dict and word not in stop_words:
            list_doc_2.append(word)
    vect_2 = Counter(list_doc_2)

    matrix_1 = W[[vocab_dict[w] for w in vect_1.keys()]]
    matrix_2 = W[[vocab_dict[w] for w in vect_2.keys()]]

    # Caculate word frequency
    v1 = list(vect_1.values())
    v1 = np.ravel(v1)
    v1 = np.divide(v1, v1.sum())

    v2 = list(vect_2.values())
    v2 = np.ravel(v2)
    v2 = np.divide(v2, v2.sum())

    D1_ = euclidean_distances(matrix_1, matrix_2)
    D1_min = np.amin(D1_, axis=1)

    D2_ = euclidean_distances(matrix_2, matrix_1)
    D2_min = np.amin(D2_, axis=1)

    return max(np.dot(D1_min, v1), np.dot(D2_min, v2))

def KNN(k, input_doc):
    # lowercase all the text on the file
    dataLower = input_doc.lower()
    # create new list punctuation
    punctuation = re.sub('_', '', string.punctuation)
    # then add some special characters in Vietnamese to this list
    punctuation += '–“”…'
    # remove all punctuation
    result = re.sub('[%s]' % punctuation, ' ', dataLower)
    wcd = WCD(result)

    with open("wmd/data/list_doc.vocab", encoding='utf-8') as f:
        list_docs = f.read().splitlines()
    doc_dict = {doc: k for k, doc in enumerate(list_docs)}

    wmd_k_doc = {}
    count = 1
    max_rwmd = RWMD(list_docs[wcd[0][0]], input_doc)
    for i in range(0, len(wcd)):
        if (count <= k):
            wmd_k_doc[wcd[i][0]] = WMD(list_docs[wcd[i][0]], input_doc)
            if max_rwmd < RWMD(list_docs[wcd[i][0]], input_doc):
                max_rwmd = RWMD(list_docs[wcd[i][0]], input_doc)
        else:
            rwmd = RWMD(list_docs[wcd[i][0]], input_doc)
            if rwmd < max_rwmd:
                wmd_k_doc[wcd[i][0]] = WMD(list_docs[wcd[i][0]], input_doc)
        count += 1

    wmd_k_doc = sorted(wmd_k_doc.items(), key=operator.itemgetter(1))

    k_doc = []
    for i in range(0, k):
        k_doc.append(wmd_k_doc[i])

    print(k_doc)


# def main():
#     # doc = "thật dễ dàng thể đâu đứa trẻ cứng đầu thật khó thể trừng phạt đưa chúng khuôn khổ thời điểm chúng tỏ khó bảo kiên chịu đứng thực thiết dễ khiến mẹ giáo viên cảm mệt mỏi căng thẳng nghiệp nuôi dạy đứa trẻ cá tính mạnh mẽ giờ bậc mẹ thể tin phép màu thật sách nhỏ sách cung cấp hy vọng đặt mục tiêu tầm tay mang luồng sinh khí gia đình giáo viên tác giả cynthia ulrich tobias giải thích rõ sách mẹ thể ép thuyết phục cách suy nghĩ đứa trẻ cứng đầu cách mẹ thầy thể khai thác tối đa kiến thức cung cấp hỗ trợ hướng phát triển toàn diện sách giúp nhìn thấu cách suy nghĩ trẻ cứng đầu hiểu lý lời học cách nhượng giữ uy quyền mẹ khám phá phương thức hiệu tạo động lực đứa cứng đầu hãy hàn gắn mối quan hệ giúp phát huy tính cách mạnh mẽ thành công mẹ thể ép thuyết phục"
#     # KNN(5, doc)
#     print(W[0][0])
#
# if __name__ == '__main__':
#     main()