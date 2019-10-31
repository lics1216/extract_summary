## extract_summary

=====================

### 提取思路介绍

#### 思路1

根据游戏评分提取评论摘要，利用[自然语言处理工具包HanLP](https://github.com/hankcs/pyhanlp)实现的。内部采用TextRankSentence实现，[参考](http://www.hankcs.com/nlp/textrank-algorithm-java-implementation-of-automatic-abstract.html)
```
from pyhanlp import HanLP
HanLP.extractSummary(x, 1, r'[ ]')
```
1. textRank 借鉴PageRank
    - [PageRank 理解](https://www.letiantian.me/2014-06-10-pagerank/)
    - [textRank 关键词、短语、摘要提取](https://blog.csdn.net/AndrewLee_/article/details/55095538)
        - 对句子分词、词性标注，并过滤掉停用词，只保留指定词性的单词，如v/n/adj
    - [HanLP textRank的java实现](http://www.hankcs.com/nlp/textrank-algorithm-java-implementation-of-automatic-abstract.html) 
    - [HanLp工具包实现textRank摘要提取](https://github.com/hankcs/pyhanlp)
2. [BM25 相似度计算](https://www.jianshu.com/p/1e498888f505)

game_summaries_taptap4 是提取评论的测试juptyer测试。最终结果如下

![summary1](image/summary1)

存在问题，提取出来的摘要有些语句不顺。

#### 思路2
提取游戏评论，类似淘宝商品的归纳评论
1. 我认为在语料不充足下，优秀算法和模型，不能解决全部问题，如特征冗余、相似特征替换
2. 提取特征规则简单化`{<n><n><d>*<a>+}`和`{<v><n><d>*<a>+}`，特征的同义特换
3. 再根据`<n><n>`或者`<v><n>` 的频率过滤
4. `<d><a>` 判断情感，手动标注情感值

game_summaries_taptap_by_minig_feature 是提取评论的测试juptyer测试。最终结果如下

![summary2](image/summary2)

### web 页面
extract_summary_web 是用来展示结果的web页面

### mtmodel
是处理全部评论的项目代码，用supervisor 管理项目进程