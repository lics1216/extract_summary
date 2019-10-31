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
import json
from mtmodel.utils import store, pd_source
from collections import Counter
from snownlp import SnowNLP
from gensim.models import KeyedVectors
taptap_vector = KeyedVectors.load("/home/mingchao/lcs_data/taptap_comments_vector", mmap='r')

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
def leaves(tree):
    for subtree in tree.subtrees(filter=lambda t: t.label()=='NP'):
        yield subtree.leaves()
def extract_asp_by_grammar(text):     
    # text = "因为这个风格蛮喜欢的,加上TapTap的推荐就下载来玩了,bgm挺好的游戏（开着bgm写的评论）,然后游戏体验相当棒了"
    words = pseg.cut(text)
    sent_tags = [(x,y) for x,y in words]
    # NP(名词短语块) DT(限定词) JJ(形容词) NN(名词)
    grammar = "NP: {<n>{2,4}}"
    # 进行分块
    cp = nltk.RegexpParser(grammar)
    tree = cp.parse(sent_tags)
    aspects = [[w for w,t in leaf] for leaf in leaves(tree)]
    return [''.join(asp) for asp in aspects]

def sents_lenght(content_clear):
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

# 过滤特征 all([true, true, true]) = true
stop_asp = ['垃圾', '辣鸡', '感觉', '公司', '问题', '腾讯', '时候']
def vaild_asp(aspects):
    return [s for s in aspects if all([stop not in s for stop in stop_asp])]

# asp x len都等于4
# asp=游戏画风/ x=游戏画质  asp=玩家素质/x=素质玩家  
def is_similar(asp,x):
    a = [asp[0:2],asp[2:4]]
    b = [x[0:2],x[2:4]]
    try:
        similar = [taptap_vector.similarity(y, z) for y in a for z in b]
    except:
        print('word2vec have no',asp,x)
        return False
    return True if len([y for y in similar if y>0.8])>1 else False

# 根据特征提取句子，返回一个dict
def extract_summa_by_asp(content_clear):
    sents = re.split( r'[!。！? ？]', content_clear)
    sents_len_40 = [x for x in sents if 20<len(x)<80]
    sents_by_asp = [[s for s in sents_len_40 if asp in s] for asp in all_sents_aspects] 
    return dict(zip(all_sents_aspects, sents_by_asp))


sql = "SELECT distinct game_id FROM game_source.s_game_comments_taptap_game WHERE source='taptap'"
game_id_list = from_sql(sql)
for game_id in tqdm(list(game_id_list['game_id'])):
    sql = """
    SELECT source,game_name, game_id, score, up, content FROM game_source.s_game_comments_taptap_game where game_id = %s  and cast(up as signed)>5 
    """% (game_id,)
    df = from_sql(sql)
   
    # 去除\n，替换空格 和（xxx） 
    df['content_clear'] = df['content'].apply(clear_text)
    
    # sents_len
    df['sents_len'] = df['content_clear'].apply(sents_lenght)

    # sentens_aspects
    df['sents_asp'] = df['content_clear'].apply(extract_sents_aspects)
   
    # 改善提取特征
    sents_aspects = [y for _,x in df.iterrows() for y in x['sents_asp']]
    asp_4 = []
    for asp in sents_aspects:
        if len(asp)==4:
            asp_4.append(asp)
    # 可以直接返回 asp, 不用（asp,count）,但是我想看看数据 0.0024是根据经验来的
    sents_len = sum(df['sents_len'])
    sents_aspects_tuple_20 = [(asp,count) for asp,count in Counter(asp_4).most_common(15) if count/sents_len > 0.0024]
    sents_aspects_20 = [s for s,_ in sents_aspects_tuple_20]
    
    # 过滤停用词
    all_sents_aspects = vaild_asp(sents_aspects_20)
    
    # 过滤 一些相似的特征
    if len(all_sents_aspects) > 1:
        aspects_unique = [all_sents_aspects[0]]
        for asp in all_sents_aspects[1:len(all_sents_aspects)]:
            if not any([is_similar(asp,x) for x in aspects_unique]):
                aspects_unique.append(asp)
        all_sents_aspects = aspects_unique
    
    # extract_sents_by_asp
    df['summ_asp'] = df['content_clear'].apply(extract_summa_by_asp)
   
    # 感情判断 过滤摘要
    game_summa_asp = [[s for _,x in df.iterrows() for s in x['summ_asp'][asp] if not 0.15<SnowNLP(s).sentiments<0.85] for asp in all_sents_aspects]
    game_summa_dict = dict(zip(all_sents_aspects, game_summa_asp))

    # 只留下 ch长度, 取前五条
    retain_len = 4
    del_asp = [asp for asp,comm in game_summa_dict.items() if len(comm)<retain_len]
    for asp in del_asp:
        game_summa_dict.pop(asp)
    for asp,comm in game_summa_dict.items():
        game_summa_dict[asp] = game_summa_dict[asp][:(5 if len(comm)>5 else len(comm))]

    trg_db='game_process'
    trg_table='c_lcs_game_comment_summary_base_asp'
    
    try:
        row = df.iloc[0]
    except :
        print('df is null')
        continue

    # 如果game_summa_dict 空
    if not game_summa_dict:
        continue

    summaries = json.dumps(game_summa_dict, ensure_ascii=False)
    kv = dict(
        source = str(row['source']),
        game_id = str(row['game_id']),
        game_name = str(row['game_name']), 
        summaries = summaries
        )
    store.to_mysql(kv, trg_db, trg_table)