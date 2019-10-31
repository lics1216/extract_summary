#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-21 14:41:49
# @Author  : yangchaojun (YYChildren@gmail.com)
# @Link    : https://git.mingchao.com/yangchaojun
# @Version : $Id$

import requests
import json

import logging
from mtmodel.utils.config import CONFIG

def to_mysql(kv, db, table, logType = 'insert_duplicate'):
    mslog_urls = CONFIG['mslog']['urls']
    data = [dict(database=db, tableName=table, logType=logType, kvs=[kv])]
    payload = json.dumps(data, ensure_ascii=False).encode('utf-8')
    try:
        for mslog_url in mslog_urls:
            resp = requests.post(mslog_url, data=payload)
            text = resp.text.strip()
            if text != 'ok':
                logging.error("kv: %s response: %s" % (kv, text))
                return False
            else:
                logging.info("kv: %s response: %s" % (kv, text))
                return True
    except Exception as e:
        logging.error("kv: %s error: %s" % (kv, e))
        return False