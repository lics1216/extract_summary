#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-21 10:35:51
# @Version : 

import pymysql
import pandas as pd
import re
from bs4 import BeautifulSoup
from hanziconv import HanziConv
from zhon import hanzi
import string
punctuation=hanzi.punctuation + string.punctuation
punctuation = set([i for i in punctuation])
import html
import pymysql
import jieba
from tqdm import tqdm

import nltk
with open('resources/corpus/stopwords-zh.txt', 'rb') as  file:
    stopwords = file.read().decode('utf-8').splitlines()
    stopwords = set(stopwords + nltk.corpus.stopwords.words("english"))
from pyhanlp import HanLP
from mtmodel.utils import store, pd_source
import json

def extract_text(x):
    soup = BeautifulSoup(x, 'html.parser')
    return soup.text

def clear_text(x):
    x = html.unescape(x)
    x = HanziConv.toSimplified(x)
    x = x.strip()
    return x

def remove_punctuation(x):
    x = "".join([i for i in x if i not in punctuation])
    return re.sub(r'\s+', ' ', x)

def get_help_content(x):
    x = "".join([i if i not in punctuation else " " for i in x])
    x = re.sub(r'\s+', ' ', x)
    x = x.strip()
    return x

def distinct_count(sentence):
    return len(set([i for i in sentence]))

def tokenize(x):
    x= [i for i in HanLP.segment(x) if i != ' ']
    return x

def join(L):
    return " ".join([j for i in L for j in i])

def from_sql(sql):
    conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='eXYhzAWjyvy8grwM',charset='utf8mb4')
    df = pd.read_sql(sql, conn)  
    conn.close()
    return df
def extract_summa(s):
    summa = HanLP.extractSummary(s, 15, r'[ ]')
    return [x for x in summa if 10< len(x) <40]

def extract_s_nature(s):
    return ['{}'.format(term.nature) for term in HanLP.segment(s)]
def clear_summa(summaries):
    return [s for s in summaries if 'c' not in extract_s_nature(s) and 'cc' not in extract_s_nature(s)]

sql = "SELECT distinct game_id FROM game_source.s_game_comments_taptap_game WHERE source='taptap'"
game_id_list = from_sql(sql)
game_s = pd.DataFrame()
from datetime import datetime
for game_id in tqdm(list(game_id_list['game_id'])):
    sql = """
    SELECT source, game_id, game_name, content FROM game_source.s_game_comments_taptap_game where game_id = %s and length(content)>300
    """ % (game_id, )
    df = from_sql(sql)
    
    df['content'] = df['content'].apply(clear_text)
    df['content'] = df['content'].apply(get_help_content)

    df['summaries']=df['content'].apply(lambda x: list(HanLP.extractSummary(x, 1, r'[ ]')))
    df_new = df[['source', 'game_id', 'game_name', 'summaries']].groupby(['source', 'game_id','game_name']).agg(join).reset_index()
    
    #做了两次的提取摘要，
    try:
        df_new['summaries'] = df_new['summaries'].apply(extract_summa)
        df_new['summaries'] = df_new['summaries'].apply(clear_summa)
    except:
        print('summar is []')
        continue

    if df_new.iloc[0]['summaries'] == []:
        continue

    trg_db='game_process'
    trg_table='c_lcs_game_comment_summary'

    for index in tqdm(df_new.index):
        row = df_new.iloc[index]
        game_name = row['game_name']
        summaries = json.dumps(row['summaries'], ensure_ascii=False)
        kv = dict(
            source = str(row['source']),
            game_id = str(row['game_id']),
            game_name = str(row['game_name']), 
            summaries = summaries
            )
        store.to_mysql(kv, trg_db, trg_table)
