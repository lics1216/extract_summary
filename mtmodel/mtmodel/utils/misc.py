#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-15 17:47:40
# @Author  : yangchaojun (YYChildren@gmail.com)
# @Link    : https://git.mingchao.com/yangchaojun
# @Version :

import os
from mtmodel.utils.config import CONFIG
import dill


def get_sklearn_path(name):
    p = os.path.join(CONFIG['base']['datadir'], 'sklearn')
    os.makedirs(p, mode=0o755, exist_ok=True)
    return os.path.join(p, name)


def get_gensim_path(name):
    p = os.path.join(CONFIG['base']['datadir'], 'gensim')
    os.makedirs(p, mode=0o755, exist_ok=True)
    return os.path.join(p, name)


def get_output_path(name):
    p = os.path.join(CONFIG['base']['datadir'], 'output')
    os.makedirs(p, mode=0o755, exist_ok=True)
    return os.path.join(p, name)


def dump(obj, path):
    with open(path, 'wb') as f:
        dill.dump(obj, f)


def load(path):
    with open(path, 'rb') as f:
        return dill.load(f)
