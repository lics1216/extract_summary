#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-15 10:31:46
# @Author  : yangchaojun (YYChildren@gmail.com)
# @Link    : https://git.mingchao.com/yangchaojun
# @Version : 

import yaml
import codecs
from . import Singleton


class _config(Singleton, dict):
    """docstring for _config"""
    def __init__(self):
        super(_config, self).__init__()
        self.load_conf()

    def load_conf(self):
        '''
        返回配置字典
        '''
        conf_path = 'config/common.yml'
        self.conf_path=conf_path
        with codecs.open(conf_path, "r", "utf-8") as f:
            cfg=yaml.load(f)
        self.update(cfg)

CONFIG=_config()
