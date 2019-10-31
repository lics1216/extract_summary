#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-21 14:41:49
# @Author  : yangchaojun (YYChildren@gmail.com)
# @Link    : https://git.mingchao.com/yangchaojun
# @Version : $Id$

from hanziconv import HanziConv
from bs4 import BeautifulSoup
from zhon import hanzi
import string
punctuation=hanzi.punctuation + string.punctuation
punctuation = set([i for i in punctuation])
from nltk import corpus
import sys
import re
import jieba
from jieba import analyse
import html
import json
from functools import partial
from mtmodel.utils.config import CONFIG

with open(CONFIG['resources']['stopwords_path'], 'rb') as  file:
    stopwords = file.read().decode('utf-8').splitlines()
    stopwords = set(stopwords + corpus.stopwords.words("english"))

def extract_text(x):
    soup = BeautifulSoup(x, 'html.parser')
    return soup.text

def remove_punctuation(x):
    x = "".join([i for i in x if i not in punctuation])
    return re.sub(r'\s+', ' ', x)

def clear_text(x):
    x = extract_text(x)
    x = html.unescape(x)
    x = remove_punctuation(x)
    x = HanziConv.toSimplified(x)
    return x

def remove_stopwords(words):
    return [i for i in  words if i not in stopwords]

# 判断一个unicode是否是汉字或者数字
def is_chinese_or_number(uchar):         
    return ('\u4e00' <= uchar<='\u9fff') or ('\u0030' <= uchar<='\u0039')

# 判断是不是中文句子（中文或者数字的比例超过50%）
def is_chinese_sentence(sentence):
    if sentence == '':
        return False
    chinese_num = len([i for i in sentence if is_chinese_or_number(i)])
    return (chinese_num / float(len(sentence))) > 0.5

def tokenize(sentence, remove_stopword=True):
    x= [i for i in jieba.cut(sentence) if i != ' ']
    return remove_stopwords(x) if remove_stopword else x

from mtmodel.model import idf_textrank
tfidf=jieba.analyse.TFIDF()
textrank=jieba.analyse.TextRank() 
idf_textrank=idf_textrank.IDFTextRank()

tfidf.stop_words.update(stopwords)
textrank.stop_words.update(stopwords)
idf_textrank.stop_words.update(stopwords)


extract_tfidf_keywords = partial(tfidf.extract_tags, 
    topK=5,
    withWeight=False, 
    allowPOS=('n', 'nr','ns','nz','nl', 'ng','v','vn','a','x'))


extract_textrank_keywords = partial(textrank.extract_tags, 
    topK=5, 
    withWeight=False, 
    allowPOS=('n', 'nr','ns','nz','nl', 'ng','v','vn','a','x'))


extract_keywords = partial(idf_textrank.extract_tags, 
    topK=5, 
    withWeight=False, 
    allowPOS=('n', 'nr','ns','nz','nl', 'ng','v','vn','a','x'))
