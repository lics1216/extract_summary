#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-15 11:27:48
# @Author  : yangchaojun (YYChildren@gmail.com)
# @Link    : https://git.mingchao.com/yangchaojun
# @Version : 

class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)  
        return cls._instance