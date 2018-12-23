# -*- coding:utf-8 -*-

from __future__ import print_function
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from scipy.linalg import norm

import logging
import re
import csv

import jieba
import jieba.posseg
import pandas as pd
import numpy as np


def get_logger(name="default"):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    return logging.getLogger(name)


class IterDocument(object):
    """
    A class for reading large file memory-friendly
    """

    def __init__(self, path, sep=None):
        """
        :param path: path to the file
        :param sep: delimiter string between fields
        """
        self.path = path
        self.sep = sep

    def __iter__(self):
        """
        :return: iteration in lines
        """
        for line in open(self.path, 'r',encoding="utf-8").readlines():
            line = line.strip()
            if line == '':
                continue
            if self.sep is not None:
                yield [item for item in line.split(self.sep) if item != ' ' and item != '']
            else:
                yield line


class TextCleaner(object):
    """
    A class for cleaning text
    """
    def __init__(self, punctuation=True, number=True, normalize=True):
        """
        Initial
        :param punctuation: whether clean punctuation
        :param number: whether clean number
        :param normalize: whether normalize token
        """
        self.punc = punctuation
        self.num = number
        self.norm = normalize

        self.punctuation = IterDocument("userdict/punctuation")
        

    def clean(self, text):
        """
        Clean data
        :param text: the raw string
        :return: the string after cleaning
        """
        # if self.punc:
        #     for p in self.punctuation:
        #         text = re.sub(p, "", text)

        # 只保留中文的正则表达式
        cop = re.compile("[^\u4e00-\u9fa5]")
        text = cop.sub("", text)

        # 词语书写规范
        # text = re.sub(r"你我","你我贷", text)


        return text.strip()


class Segmentor(object):
    """
    A class for segmenting text
    """
    def __init__(self, user_dict=True):
        """
        Initial
        :param user_dict: whether use user dict
        """
        self.seg = jieba
        self.seg_pos = jieba.posseg
        if user_dict:
            self.seg.load_userdict("userdict/userdict")

    def seg_token(self, text):
        """
        :param text: the raw string
        :return: a list of token
        """
        return self.seg.lcut(text)

    def seg_token_pos(self, text):
        """
        :param text: the raw string
        :return: a list of token/pos
        """
        return ["%s/%s" % (token, pos) for token, pos in self.seg_pos.lcut(text)]


class PreProcess(object):
    """
    A class for feature selecting and extracting
    """
    def __init__(self, file_path):
        """
        Initial
        :param file_path: the comment data path
        """
        self.logger = get_logger("PreProcess")
        self.logger.info("load data from %s" % file_path)

        corpus = pd.read_csv(file_path, "\t")
        # print(corpus)
        self.corpus = corpus.rename(columns={"question": "question",
                                             "answer": "answer"})
        # print(self.corpus)
        self.logger.info("data size: %s" % self.corpus.shape[0])

        self.cleaner = TextCleaner()
        self.seg = Segmentor()
        self.segment()

        # #预处理后保存结果
        # self.corpus.to_csv ("QA.csv" , sep="\t", index=0, encoding = "utf-8")

    def segment(self):
        """
        Segment text
        """
        def seg(row):
            print(row["question"])
            # print(row["answer"])
            s = self.cleaner.clean(row["question"])
            print(s)
            row["question_seg"] = self.seg.seg_token(s)
            print(row["question_seg"])
            #加载停用词表
            stop = [line.strip() for line in open('userdict/stop_words.txt',encoding='UTF-8').readlines()]
            final = ''
            for seg in row["question_seg"]:
            #去停用词
                if seg not in stop:
                    final +=' '+ seg 
            row["question_seg_stop"] = final
            print(row["question_seg_stop"])
            print("\n")
            return row

        self.corpus = self.corpus.apply(seg, axis=1)
        

    def make_data_set(self):
        text = self.corpus["content"].values
        text_seg = np.array(map(lambda x: " ".join(x), self.corpus["content_seg"].values))

        return DataSet(text, text_seg)


class DataSet(object):
    """
    A class for organize data
    """
    def __init__(self, text, text_seg):
        """
        Initialize
        :param text: the raw text data, a numpy array as array(text1, text2, ...)
        :param text_seg: the text data after cleaning and segment, a numpy array as array("token1 token2 ...", ...)
        """
        self.text = text
        self.text_seg = text_seg
        self.data_size = len(text)

    def get_batch(self, _from, _to):
        """
        Get a batch of data
        :param _from: the position to start
        :param _to: the position to end
        :return: a subset of data set
        """
        if _from == 0 and _to >= self.data_size:
            return self
        return DataSet(self.text[_from:_to], self.text_seg[_from:_to])

    def shuffle_data(self):
        """
        Shuffle data set
        :return: random shuffled data
        """
        shuffle_arrays(self.text, self.text_seg)


def shuffle_arrays(*arrays):
    """
    In-place shuffle array
    :param arrays: raw data set
    """
    rng_state = np.random.get_state()
    for array in arrays:
        np.random.shuffle(array)
        np.random.set_state(rng_state)

def cosine_similarity_tf(s1, s2):     
    vectorizer = CountVectorizer(tokenizer=lambda s: s.split())    
    corpus = [s1, s2]    
    # print(corpus)
    X = vectorizer.fit_transform(corpus)
    # print(X)
    vectors = X.toarray()   
    # print(vectors) 
    # result =  np.dot(vectors[0], vectors[1]) / (norm(vectors[0]) * norm(vectors[1]))
    result = cosine_similarity(vectors)
    # print("current:",result[0][1])
    return result[0][1]


if __name__ == "__main__":
    file_name = "QA.csv"
    # pre = PreProcess(file_name)
    Qcleaner = TextCleaner()
    Qseg = Segmentor()
    while(1):
        question = input("请输入您的问题：")
        s = Qcleaner.clean(question)
        # print(s)
        question_seg = Qseg.seg_token(s)
        # print(question_seg)
        #加载停用词表
        stop = [line.strip() for line in open('userdict/stop_words.txt',encoding='UTF-8').readlines()]
        final = ''
        for seg in question_seg:    #去停用词
            if seg not in stop:
                final +=' '+ seg 
        question_data = final
        # print(question_data)
 
        csv_data = pd.read_csv(file_name,encoding="utf-8",sep='\t')
        # print(csv_data.shape)
        list = []
        for i in range(len(csv_data)):
            QA_data = csv_data['question_seg_stop'][i]
            result = cosine_similarity_tf(question_data,QA_data)
            list.append(result)
        final_result = max(list)
        # print(final_result) 
        if final_result>0.6:
            print("余弦相似度：",final_result)
            reply = csv_data['answer'][list.index(final_result)]
            print("回复：", reply)
            print("\n")
        else:
            print("余弦相似度：",final_result)
            print("回复：不好意思，这个问题我不知道呢。\n")
    
 
