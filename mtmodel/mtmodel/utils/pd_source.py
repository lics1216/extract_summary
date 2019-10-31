#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-15 13:48:27
# @Author  : yangchaojun (YYChildren@gmail.com)
# @Link    : https://git.mingchao.com/yangchaojun
# @Version : 

import pymysql
import pandas as pd
from mtmodel.utils.config import CONFIG


def from_sql(sql):
    conn_conf = dict(
        host=CONFIG['mysql']['host'],
        port=CONFIG['mysql']['port'],
        user=CONFIG['mysql']['user'],
        password=CONFIG['mysql']['password'],
        charset=CONFIG['mysql']['charset']
    )
    conn = pymysql.connect(**conn_conf)
    df = pd.read_sql(sql, conn)
    conn.close()
    return df