#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-06-12 17:35:58
# @Author  : yangchaojun (YYChildren@gmail.com)
# @Link    : https://git.mingchao.com/yangchaojun
# @Version : 1.0.0

import pymysql


def get_comment(fields, index1, index2):
    fs = ",".join(fields)             
    sql = "SELECT %s FROM c_lcs_game_comment_summary_base_asp where cast(game_id as signed)>=%s order by cast(game_id as signed) asc limit %s" % (fs, index1, index2)
    conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='eXYhzAWjyvy8grwM',db='game_process',charset='utf8mb4')
    # 创建mysql 游标
    cursor = conn.cursor()
    cursor.execute(sql)
    # fetchall 获取all数据、 fetchone 获取单条
    # a = [1, 2, 3] b = [4, 5, 6] zip(a, b) = [(1,4), (2,5), (3,6)]
    rs = [dict(zip(fields, i)) for i in cursor.fetchall()]
    cursor.close()
    conn.close()
    return rs

def last_comment(fields, index1, index2):
    fs = ",".join(fields)             
    sql = "select * from (SELECT %s FROM c_lcs_game_comment_summary_base_asp where cast(game_id as signed)<=%s order by cast(game_id as signed) desc limit %s) a  order by cast(a.game_id as signed) asc" % (fs, index1, index2)
    conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='eXYhzAWjyvy8grwM',db='game_process',charset='utf8mb4')
    # 创建mysql 游标
    cursor = conn.cursor()
    cursor.execute(sql)
    # fetchall 获取all数据、 fetchone 获取单条
    # a = [1, 2, 3] b = [4, 5, 6] zip(a, b) = [(1,4), (2,5), (3,6)]
    rs = [dict(zip(fields, i)) for i in cursor.fetchall()]
    cursor.close()
    conn.close()
    return rs

# def update_comment(index, field, value):
#     sql = "UPDATE s_lcs_game_comments_qq SET %s=%s WHERE id=%s" % (field, value, index)
#     conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='eXYhzAWjyvy8grwM',db='game_process',charset='utf8mb4',autocommit=True)
#     cursor = conn.cursor()
#     cursor.execute(sql)
#     cursor.close()
#     conn.close()
#     return True
