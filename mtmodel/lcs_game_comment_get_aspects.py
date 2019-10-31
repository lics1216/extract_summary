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
import html
import pymysql
from tqdm import tqdm
from collections import Counter
import json

def clear_text(x):
    x = BeautifulSoup(x, 'html.parser').text
    x = html.unescape(x)
    x = HanziConv.toSimplified(x)
    x = re.sub(r'\s+', '', x) # tab \n 去除 匹配任何非空白字符。等价于 [^ \f\n\r\t\v]。
    x = re.sub(r'[\(（【](.*?)[\)）】]', '', x) # 替换 （）是单元， ?非贪婪匹配，否则.*把后面的括号也匹配掉了
    x = re.sub(r'([–-—=…]*)', '',x)
    x = x.strip()
    return x

def from_sql(sql):
    conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='eXYhzAWjyvy8grwM',charset='utf8mb4')
    df = pd.read_sql(sql, conn)  
    conn.close()
    return df

import nltk
import jieba
jieba.load_userdict('/home/mingchao/lcs_data/comment_jieba_add_word.txt')
import jieba.posseg as pseg
def leaves(tree):
    for subtree in tree.subtrees(filter=lambda t: t.label()=='NP'):
        yield subtree.leaves()
def extract_asp_by_grammar(text):     
    # text = "因为这个风格蛮喜欢的,加上TapTap的推荐就下载来玩了,bgm挺好的游戏（开着bgm写的评论）,然后游戏体验相当棒了"
    words = pseg.cut(text)
    sent_tags = [(x,y) for x,y in words]
    # NP(名词短语块) DT(限定词) JJ(形容词) NN(名词)
    # 名词名词，或者名词形容词
    # grammar = "NP: {<n>{2,4}}"
    grammar = r"""
                NP: {<n>+<d>*<a>+}
                    {<v><n><d>*<a>+}
                """
    # 进行分块
    cp = nltk.RegexpParser(grammar)
    tree = cp.parse(sent_tags)
    aspects = [[w for w,t in leaf] for leaf in leaves(tree)]
    return [''.join(asp) for asp in aspects]

def extract_sents_aspects(content_clear):
    sents = re.split(r'[!。！? ？]', content_clear)
    sents = [x for x in sents if x is not '']
    sents_tags = [extract_asp_by_grammar(text) for text in sents] # [[],[],[]]
    #是否要去掉，单字特征
    return [y for x in sents_tags if x!=[] for y in x if len(y)>2] # [ ]

def get_n_v_a(s1):
    v_n = ''
    a = ''
    for x,y in pseg.cut(s1):
        if y=='v' or y=='n':
            v_n=v_n+x
        elif '不' in x or y=='a':
            a=a+x
        else:
            pass
    return v_n, a
# write 
def write_txt(text, t_name):
    with open(t_name, 'a') as f:
        for x in text:
            f.write(x+'\n')

def sents_len(content_clear):
    sents = re.split(r'[!。！? ？]', content_clear)
    sents = [x for x in sents if x is not '']
    return len(sents)

comment_sentiment = []
sql = "SELECT distinct game_id FROM game_source.s_game_comments_taptap_game WHERE source='taptap' limit 400"
game_id_list = from_sql(sql)
for game_id in tqdm(list(game_id_list['game_id'])):
    sql = """
    SELECT source,game_name, game_id, score, up, content FROM game_source.s_game_comments_taptap_game where game_id = %s  and cast(up as signed)>5 
    """% (game_id,)
    df = from_sql(sql)

    # 去除\n，替换空格 和（xxx） 
    df['content_clear'] = df['content'].apply(clear_text)

    # sentens_aspects
    df['sents_asp'] = df['content_clear'].apply(extract_sents_aspects)

    df['sents_len'] = df['content_clear'].apply(sents_len)

    # 改善提取特征，
    sents_aspects = [y for _,x in df.iterrows() for y in x['sents_asp']]

    asp_v_n = [(x,)+get_n_v_a(x) for x in sents_aspects]
    asp_v_n_4 = [(x, y, z) for x,y,z in asp_v_n if len(y)>3]

    sentences_len = sum(df['sents_len'])
    #  if count/sentences_len > 0.00017
    asp_n_n = [y for x,y,z in asp_v_n_4]
    aspects = [asp for asp,count in Counter(asp_n_n).most_common(20) if count/sentences_len > 0.00017]
    comment_sentiment.extend([z for x in aspects for _,y,z in asp_v_n_4  if x in y])

write_txt(set(comment_sentiment), '/home/mingchao/lcs_data/comment_sentiment.txt')