#!/usr/bin/env python
#encoding: utf-8
#description: 从字符串中提取省市县等名称,用于从纯真库中解析解析地理数据
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#匹配规则必须含有u,可以没有r
#这里第一个分组的问号是懒惰匹配,必须这么做
PATTERN = \
ur'([\u4e00-\u9fa5]{2,5}?(?:省|自治区|市))([\u4e00-\u9fa5]{2,7}?(?:市|区|县|州)){0,1}([\u4e00-\u9fa5]{2,7}?(?:市|区|县)){0,1}'
data_list = ['北京市', '陕西省西安市雁塔区', '西班牙', '北京市海淀区', '黑龙江省佳木斯市汤原县', '内蒙古自治区赤峰市',
'贵州省黔南州贵定县', '新疆维吾尔自治区伊犁州奎屯市']
for data in data_list:
 data_utf8 = data.decode('utf8')
 print data_utf8
 country = data
 province = ''
 city = ''
 district = ''
 #pattern = re.compile(PATTERN3)
 pattern = re.compile(PATTERN)
 m = pattern.search(data_utf8)
 if not m:
  print country + '|||'
  continue
 #print m.group()
 country = '中国'
 if m.lastindex >= 1:
  province = m.group(1)
 if m.lastindex >= 2:
  city = m.group(2)
 if m.lastindex >= 3:
  district = m.group(3)
 out = '%s|%s|%s|%s' %(country, province, city, district)
 print out