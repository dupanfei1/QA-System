
import jieba
import jieba.posseg
import pandas as pd
import numpy as np
import logging
import re
import csv

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

from sqltest import *
from intent import intent,intent2
import mysql.connector
if __name__ == "__main__":
    conn = mysql.connector.connect(host='123.207.254.194', user='lab_mate', password='NLP!research2018',
                                   database='nlp_resource')
    while (1):
        question = input("请输入您的问题：")
        # question = "中国存托凭证的定义是什么"
        try:
            intnt = intent2(question) #提取意图
        except:
            intnt = intent(question) #提取意图
        print(intnt)
        entity1 = intnt[0]
        entity2 = intnt[1]
        sql= "SELECT obj_entity FROM knowledge WHERE sub_entity LIKE '%"+entity1+"%' AND relation='"+entity2+"'"
        # sql = "SELECT obj_entity FROM knowledge WHERE find_in_set('%"+entity1+"%', sub_entity) AND relation='"+entity2+"'"
        result = search(conn, sql)  #查表
        print(result)
    conn.close()

        # Qcleaner = TextCleaner()
        # Qseg = Segmentor()
        # s = Qcleaner.clean(question)
        # # print(s)
        # question_seg = Qseg.seg_token(s)
        # print(question_seg)
        # 加载停用词表
        # stop = [line.strip() for line in open('userdict/stop_words.txt', encoding='UTF-8').readlines()]
        # final = ''
        # for seg in question_seg:  # 去停用词
        #     if seg not in stop:
        #         final += ' ' + seg
        # question_data = final
        # print('done')