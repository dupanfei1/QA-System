#encoding: utf-8
import mysql.connector

# change root password to yours:
# conn = mysql.connector.connect(host='123.207.254.194', user='lab_mate', password='NLP!research2018',
#                                database='nlp_resource')
#SELECT obj_entity FROM knowledge WHERE sub_entity='中国存托凭证' AND relation='定义'
def search(conn, sql):
    cursor = conn.cursor()
    # sql ='SELECT * FROM knowledge'
    # sql = "SELECT obj_entity FROM knowledge WHERE sub_entity='中国存托凭证' AND relation='定义'"
    cursor.execute(sql)
    # print(cursor.rowcount)
    # result = cursor.fetchone()#fetch后就cursor就变了
    # print(result)
    # print(cursor.rowcount)
    result = cursor.fetchall()
    # for data in result:
    #     print(data)
    a = len(result)
    # cursor.scroll(-a, mode='absolute')
    # cursor.close()
    # conn.rollback()
    return result

# entity1 ='中国存托凭证'
# entity2 = '定义'
# sql = "SELECT obj_entity FROM knowledge WHERE sub_entity='"+entity1+"' AND relation='"+entity2+"'"
# print(search(conn,sql))
# # 关闭数据连接
# conn.close()


#
# # 运行查询:
# cursor = conn.cursor()
# cursor.execute('select * from user where id = %s', ('1',))
# values = cursor.fetchall()
# print(values)
# # 关闭Cursor和Connection:
# cursor.close()
# conn.close()