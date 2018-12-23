#!/usr/bin/env python
#encoding: utf-8
import re
import sys
PATTERN = r'([\u4e00-\u9fa5]{1,20}?(?:的|是|之))([\u4e00-\u9fa5]{1,20}?(?:是|为|有))([\u4e00-\u9fa5]{1,7})'
# PATTERN = r'([\u4e00-\u9fa5]{1,9}?(?:的|之))([\u4e00-\u9fa5]{2,7})'

data = "上证指数的定义是什么"
data = "中国存托凭证的定义是啥"
data2 = "存托凭证跨境转换的分类有哪些"
def intent(data):
    pattern = re.compile(PATTERN)
    m = pattern.search(data)
    intnt = []
    if m.lastindex >= 1:
        first = m.group(1)[:-1]
        # print(first[:-1])
        intnt.append(first)
    if m.lastindex >= 2:
        second = m.group(2)[:-1]
        # print(second[:-1])
        intnt.append(second)
    if m.lastindex >= 2:
        third = m.group(3)
        # print(m.group(3))
        intnt.append(third)
    return intnt


def intent2(data):

    classes = ["接受监管措施和纪律处分","接受日常监督措施","接受上交所监管措施","同步性","开展全球存托凭证跨境转换业务","一致性","公平性", "内容","申请","时间"]
    c1="接受监管措施和纪律处分"
    # c2="上交所会员接受监管措施和纪律处分的情形有几种"
    for item in classes:
        if item in data:
            cls = item
            break
    print(cls)
    PATTERN = r'([\u4e00-\u9fa5]{0,20}?(?:' + cls + '))([\u4e00-\u9fa5]{0,20}?(?:的))([\u4e00-\u9fa5]{1,7}?(?:有|是))([\u4e00-\u9fa5]{1,7})'
    pattern = re.compile(PATTERN)
    m = pattern.search(data)
    intnt = []
    if m.lastindex >= 1:
        first = m.group(1)
        print(first)
        # first = first.replace(c1,'')
        intnt.append(first[:-len(cls)])
    if m.lastindex >= 2:
        second = m.group(2)
        print(second)
        # intnt.append(second)
    if m.lastindex >= 2:
        third = m.group(3)
        print(m.group(3))
        # third = third.replace()
        intnt.append(third[:-1])
    print(intnt)
    return intnt