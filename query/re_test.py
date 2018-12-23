# import re
# pattern = re.compile(r'[\x80-\xff]')
# str = u'脚本之家'
# print(pattern.search(str))
#
# import re
# #测试文档
# text_string='文本最重要的来源无疑是网络。我们要把网络中的文本获取形成一个文本数据库。利用一个爬虫爬取到网络中的信息。爬取的策略又广度爬取和深度爬取。根据用户的需求，爬虫可以有主题爬虫和通用爬虫。'
# #定义一个简单的正则表达式
# regex1='爬虫'
# regex2='爬.'
# #使用。把测试文档进行分割
# p_string=text_string.split("。")
# #对分割后的句子进行遍历，找出与正则表达式匹配的句子
# for line in p_string:
#     if re.search(regex2, line) is not None:
#         print("符合regex2:"+line)


import re

hanzi = re.compile(u"[\u4e00-\u9fa5]") #一个汉字
hanzi2 = re.compile(u"[\u4e00-\u9fa5]{2}") #两个汉字
# [\u4e00-\u9fa5] 是汉字的Unicode编码范围
# 注意这里不包括标点符号，标点符号一般会在停用词过滤时去掉

all_hanzi = re.compile(u"^[\u4e00-\u9fa5]+$") #全是汉字
# ^和$分别匹配字符串的开头和结尾

s1 = "这句话全是汉字"
s2 = "这1句话不全是汉字s"
s3 = "this sentence has one 字"
s4 = "this sentence has two 汉字s"
s5 = "this 句 has three 汉字s"

for s in [s1, s2, s3, s4, s5]:
  print(s)
  print(bool(all_hanzi.match(s))) #是否全是汉字
  print(bool(hanzi.search(s))) #是否含有（至少）一个汉字
  print(bool(hanzi2.search(s))) #是否含有（至少）两个汉字
  print(hanzi.findall(s)) #字符串中含有的所有汉字的列表

regex_test = []
for i in range(5):
  regex_test.append(re.compile(r'Iteration (\d+), Testing net \(#' + str(i) + '\)'))
  print(regex_test[i])