## 提取评论摘要（类似淘宝商品评论归纳）

### jupyter 的测试代码 
game_summanies_taptap_by mini_feature6 是jupyther 测试代码。

#### 思路1
理解 pyhanlp实现，内部采用TextRankSentence实现，[参考](http://www.hankcs.com/nlp/textrank-algorithm-java-implementation-of-automatic-abstract.html)
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

存在问题
1. 摘要有语法错误的问题


#### 思路2
换了一种处理思路
1. 我认为在语料不充足下，优秀算法和模型，不能解决全部问题，如特征冗余、相似特征替换
2. 提取特征规则简单化`{<n><n><d>*<a>+}`和`{<v><n><d>*<a>+}`，特征的同义特换
3. 再根据`<n><n>`或者`<v><n>` 的频率过滤
4. `<d><a>` 判断情感，手动标注情感值


最终结果为

![summary1](image/summary.png)

参考文献
>1. [淘宝商品评论归纳-知乎](https://www.zhihu.com/question/20905103)
>2. [用户评论中的标签抽取以及排序](https://pan.baidu.com/s/1sjAuHch)

#### mtmodel 
mtmodel 是项目代码，用supervisor 管理运行处理数据

#### extract_summary_web
展示提取结果的web 页面

