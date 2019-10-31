#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-21 10:35:51
# @Version : 

import pymysql
import pandas as pd
import re, json, html, string
from bs4 import BeautifulSoup
from hanziconv import HanziConv
from zhon import hanzi
import pymysql
from tqdm import tqdm
from collections import Counter
from mtmodel.utils import store, pd_source

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
                NP: {<n><n><d>*<a>+}
                    {<v><n><d>*<a>+}
                """
    # 进行分块
    cp = nltk.RegexpParser(grammar)
    tree = cp.parse(sent_tags)
    aspects = [[w for w,t in leaf] for leaf in leaves(tree)]
    return [''.join(asp) for asp in aspects]

def sents_len(content_clear):
    sents = re.split(r'[!。！? ？]', content_clear)
    sents = [x for x in sents if x is not '']
    return len(sents)

import jieba.posseg as pseg
def extract_sents_aspects(content_clear):
    sents = re.split(r'[!。！? ？]', content_clear)
    sents = [x for x in sents if x is not '']
    sents_tags = [extract_asp_by_grammar(text) for text in sents] # [[],[],[]]
    #是否要去掉，单字特征
    return [y for x in sents_tags if x!=[] for y in x if len(y)>1] # [ ]

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

# 统计
def asp_content_count(asp_p):
    asp_p_n = [y for _,y,_ in asp_p]
    asp_p_n_count = [(asp,count) for asp,count in Counter(asp_n_n).most_common(20)]
    # 找出区别
    asp_p_content = [x for x,_,_ in asp_p]
    asp_p_content_count = []
    for x,y in asp_p_n_count:
        for content in asp_p_content:
            if x in content:
                a = content + '(' + str(y) + ')'
                asp_p_content_count.append(a)
                break
    return asp_p_content_count

sentiment_dict = {}
with open('/home/mingchao/lcs_data/comment_sentiment.txt', 'r') as f:
    for x in f.readlines():
        try:
            x = x.strip()
            sentiment_dict[x.split(' ')[0]] = x.split(' ')[1]
        except:
            print(x.strip().split(' ')[0],'dict key is exist')

sql = "SELECT distinct game_id FROM game_source.s_game_comments_taptap_game WHERE source='taptap'"
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

    from collections import Counter
    sentences_len = sum(df['sents_len'])
    # count/sentences_len > 0.00017
    asp_n_n = [y for x,y,z in asp_v_n_4]
    aspects = [(asp,count) for asp,count in Counter(asp_n_n).most_common(10) if count/sentences_len > 0.0002]
    
    ### 分开成
    asp_n = [] # n代表消极
    asp_p = [] # p代表积极
    for asp,_ in aspects:
        for x,y,z in asp_v_n_4:
            if asp in y:
                try:
                    if sentiment_dict[z] == '1':
                        asp_p.append((x,y,z))
                    elif sentiment_dict[z] == '0':
                        asp_n.append((x,y,z))
                except:
                    write_txt([z], 'comment_sentiment_miss_word.txt')
    
    p = asp_content_count(asp_p)
    n = asp_content_count(asp_n)
    p_n_dict = dict(zip(['p', 'n'], [p,n]))

    trg_db='game_process'
    trg_table='c_lcs_game_comment_asp_count'
    
    try:
        row = df.iloc[0]
    except :
        print('df is null')
        continue

    # 如果game_summa_dict 空
    if not p_n_dict:
        continue
    
    aspects = json.dumps(p_n_dict, ensure_ascii=False)
    kv = dict(
        source = str(row['source']),
        game_id = str(row['game_id']),
        game_name = str(row['game_name']), 
        aspects = aspects
        )
    store.to_mysql(kv, trg_db, trg_table)