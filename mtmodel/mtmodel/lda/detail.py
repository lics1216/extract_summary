#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-15 13:45:47
# @Author  : yangchaojun (YYChildren@gmail.com)
# @Link    : https://git.mingchao.com/yangchaojun
# @Version : 

# from utils import text_process, pd_source, store
# import pymysql
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
tqdm.pandas()
import math

