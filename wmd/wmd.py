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

# wv = gensim.models.KeyedVectors.load_word2vec_format("../nlp/word2vec/vector",
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

shape = (11832, 300)
path = "wmd/"
# path = ""
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

# if not os.path.exists("data/Xd.dat"):
#     print("Caculate Xd.dat...")
#
#     list_docs = []
#     for filename in glob.glob(os.path.join("../nlp/data-filter/result/", '*.txt')):
#         for line in open(filename, encoding='utf-8'):
#             line = line.strip()
#             if line != '':
#                 list_docs.append(line)
#     # list_docs = sorted(list_docs)
#     # print(list_docs[10])
#     X_dict = []
#     for i in range(0, len(list_docs)):
#         X_dict.append(get_xd(list_docs[i]))
#     fp = np.memmap("data/Xd.dat", dtype=np.double, mode='w+',
#                    shape=(len(list_docs), 300))
#     fp[:] = X_dict[:]
#
#     with open("data/list_doc.vocab", "w", encoding='utf-8') as f:
#         for doc in list_docs:
#             print(doc, file=f)
#     del fp

with open(path+"data/list_doc.vocab", encoding='utf-8') as f:
    list_docs = f.read().splitlines()
doc_dict = {doc: k for k, doc in enumerate(list_docs)}

x_matrix = np.memmap(path+"data/Xd.dat", dtype=np.double, mode="r",
                     shape=(len(list_docs), 300))

# Get stop-words
SW = set()
for line in open(path + 'vn_stopword.txt'):
    line = line.strip()
    if line != '':
        SW.add(line)
stop_words = list(SW)


def WMD(docs_1, docs_2):
    # t1 = time.time()
    ds1 = docs_1.split()
    ds2 = docs_2.split()
    list_doc_1 = [word for word in ds1 if word in vocab_dict]
    list_doc_2 = [word for word in ds2 if word in vocab_dict]
    # print(time.time()-t1)
    # t1 = time.time()

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
    # print(time.time()-t1)
    # t1 = time.time()

    v_1 = np.ravel(v_1)
    v_1 = np.divide(v_1, v_1.sum())
    v_2 = np.ravel(v_2)
    v_2 = np.divide(v_2, v_2.sum())
    # print(time.time()-t1)
    # t1 = time.time()

    W_ = W[[vocab_dict[w] for w in vect]]
    D_ = euclidean_distances(W_)
    D_ = D_.astype(np.double)
    # print(time.time()-t1)
    # t1 = time.time()
    _emd = emd(v_1, v_2, D_)
    # print(time.time()-t1)

    return _emd


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
    # lowercase all the text on the file
    # data_lower = input_doc.lower()
    # create new list punctuation
    # punctuation = re.sub('_', '', string.punctuation)
    # then add some special characters in Vietnamese to this list
    # punctuation += '–“”…'
    # remove all punctuation
    # result = re.sub('[%s]' % punctuation, ' ', data_lower)
    result = re.sub('\W+', ' ', input_doc.lower()).strip()
    result = " ".join([word for word in result.split() if word not in stop_words and word in vocab_dict])
    # print(result)
    if len(result) == 0:
        return []

    wcd = WCD(result)

    wmd_k_doc = {}
    count = 1

    # # Lỗi từ đây
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
    return wcd[:k]

def main():
    doc_1 = "mẹ không thể ép con thuyết phục cynthia ulrich tobias sách tiếng việt sách kinh tế mẹ không thể ép con thuyết phục cẩm nang phát huy tối đa tiềm năng đứa trẻ cứng đầu thật dễ dàng nhận ra đâu đứa trẻ cứng đầu thật khó trừng phạt đưa chúng khuôn khổ thời điểm chúng tỏ khó bảo kiên quyết chịu người lớn cho rằng đứng thực thiết dễ khiến cha mẹ giáo viên cảm thấy mệt mỏi căng thẳng sự nghiệp nuôi dạy đứa trẻ cá tính mạnh mẽ giờ đây bậc cha mẹ tin phép màu thật sách nhỏ sách cung cấp hy vọng đặt mục tiêu tầm tay mang luồng sinh khí gia đình giáo viên tác giả cynthia ulrich tobias giải thích rõ sách mẹ không thể ép thuyết phục cách suy nghĩ đứa trẻ cứng đầu cách cha mẹ thầy cô khai thác tối đa kiến thức cung cấp hỗ trợ hướng phát triển toàn diện sách giúp nhìn thấu cách suy nghĩ trẻ cứng đầu hiểu lý do tại sao lời học cách nhượng bộ giữ uy quyền cha mẹ khám phá phương thức hiệu quả tạo động lực đứa cứng đầu hãy hàn gắn mối quan hệ con cái giúp phát huy tính cách mạnh mẽ thành công mẹ không thể ép thuyết phục"

    doc_2 = "120 món cá quỳnh chi sách tiếng việt sách thường thức đời sống 120 món cá món cá ngon không chỉ phụ thuộc kỹ thuật chế biến mà còn cách lựa chọn cá tẩm ướp cá nấu nướng kinh nghiệm nghệ thuật sách hướng dẫn cách chế biến 120 món cá món cá nướng cá hấp cá gỏi cá cá chiên xào cá kho cá nấu canh hướng dẫn cụ thể tỉ mỉ hy vọng sách giúp chế biến món cá ngon lạ miệng thết đãi gia đình bè bạn"
    t1 = time.time()
    print(knn(5, doc_1))
    # print(__rwmd(doc_1, doc_2))
    print(time.time() - t1)


if __name__ == '__main__':
    main()