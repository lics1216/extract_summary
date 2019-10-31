#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-31 11:00:20
# @Author  : yangchaojun (YYChildren@gmail.com)
# @Link    : https://git.mingchao.com/yangchaojun
# @Version :

import math

# http://www.ruanyifeng.com/blog/2012/02/ranking_algorithm_hacker_news.html
def gravit_hot(P, T, G=1.8):
    """重力下降
    Args:
        P: 得票数
        T: 帖子距离现在的小时数
        G: 帖子热度的重力因子
    Returns:
        Float
    """
    return (P - 1) / math.pow(T + 2, G)

# http://www.ruanyifeng.com/blog/2012/03/ranking_algorithm_reddit.html
def reddit_hot(ups, downs, t):
    """The hot formula. Should match the equivalent function in postgres.
    args:
        t: 当前时间戳
    Returns:
        Float
    """
    s = ups - downs
    order = math.log(max(abs(s), 1), 10)
    sign = 1 if s > 0 else -1 if s < 0 else 0
    seconds = t - 1134028003
    return round(order + sign * seconds / 45000, 7)

# http://www.ruanyifeng.com/blog/2012/03/ranking_algorithm_stack_overflow.html
def sf_hot(Qviews, Qanswers, Qscore, Ascores, Qage, Qupdated):
    """stackoverflow排名
    Args:
        Qviews: 问题的浏览次数
        Qanswers: 问题的回答数
        Qscore: 问题的得分（赞成数 - 反对数）
        Ascores: 答案的得分
        Qage: 问题发布距离当前的时间(小时)
        Qupdated: 问题最后一次修改距离当前的时间(小时)
    Returns:
        Float
    """
    # return (math.log(10, Qviews) * 4 + (Qanswers * Qscore)/5 + sum(Ascores)) / math.pow((Qage+1) - (Qage - Qupdated)/2, 1.5)
    return (math.log(10, Qviews) * 4 + (Qanswers * Qscore)/5 + sum(Ascores)) / math.pow(Qage/2 + Qupdated/2 + 1, 1.5)

# http://www.ruanyifeng.com/blog/2012/03/ranking_algorithm_newton_s_law_of_cooling.html
def new_tom_cooling(T0, t0, t, alpha = 0.004125876074761579, H=0):
    """牛顿冷却定律
    Args:
        T0: 上一状态温度
        t0: 上一状态时间戳
        t: 当前状态时间戳
        H: 环境温度
        alpha: 冷却因子,该值是0.004125876074761579时，7天后温度冷却一半
    Returns:
        Float
    """
    return H + (T0 - H) * math.pow(math.e, -alpha * ((t - t0) / 3600))

# http://www.ruanyifeng.com/blog/2012/03/ranking_algorithm_wilson_score_interval.html
def wilson_score(p, n, z=1.96):
    """威尔逊区间的下限值
    Args: 
        p: 赞成票比例
        n: 样本的大下
        z: 某个置信区间的z统计量。一般情况下，在95%的置信水平下，z统计量的值为1.96
    Returns:
        Float
    """
    return (p + (z*z) / (2*n) - z*math.sqrt(p*(1-p) / n + z*z / (4*n*n))) / (1 + 1/n*z*z)

# http://www.ruanyifeng.com/blog/2012/03/ranking_algorithm_bayesian_average.html
def bma(v, m, R, C):
    """Bayesian model averaging,BMA,贝叶斯平均
    Args:
        v，参与为这个物品评分的人数
        m，全局平均每个物品的评分人数
        R，物品的平均得分
        C，全局平均每个物品的平均得分
    Returns:
        Float
    """
    return (v * R + m * C) / (v + m)


## 该算法时间因素影响较大，适合用于新游榜
def wilson_tscore(p, n, gage, cupdated):   
    """stackoverflow排名
    Args:
        p: 赞成票比例
        n: 样本的大下
        gage: 游戏发布距离当前的时间(小时)
        cupdated: 最后一次评论距离当前的时间(小时)
    Returns:
        Float
    """
    return wilson_score(p,n) / math.pow(gage/2 + cupdated/2 + 1, 1.5)