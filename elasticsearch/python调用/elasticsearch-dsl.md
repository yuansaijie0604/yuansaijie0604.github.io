# elasticsearch-dsl

# 查询数据

```python
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search,Q
client = Elasticsearch(
    "30.79.105.206:80", timeout=10, max_retries=1, retry_on_timeout=False
)

# Search().using(client).index("faq")
s = Search(using=client,index="faq")

# Q('query_string', **{"default_field":"product","query":"i康保百万医疗,通用"})
q = Q('bool',
    must = [
        Q('terms', domain=['产品介绍']),
        Q('match', **{'question':{'query':'i康保百万医疗的产品介绍', 'analyzer':"index_ansj"}})
         ],
    should = [
        Q("match_phrase",product="i康保百万医疗"),
        Q("match_phrase",product="e生保2020")
    ],
    minimum_should_match=1,
    filter=[Q('term', is_deleted=0)]
)

print(q.to_dict())

res = s.params(size=5)\
        .filter('term', is_standard=1)\
        .query(q)\
        .source(includes=["question","domain","product","groupid","images"])\
        .execute()

print(res.success())
for h in res:
    print(h.meta.index)
    print(h.meta.doc_type)
    print(h.meta.id)
    print(h.meta.score)
    print(h.to_dict())
```

# 批量获取数据

```python
from elasticsearch_dsl import Document
from elasticsearch import Elasticsearch

client = Elasticsearch(
    "30.79.105.206:80", timeout=10, max_retries=1, retry_on_timeout=False
)
y = Document.mget(docs=[3,2],using=client,index="faq",_source_includes=["question"])

# alldata = []
# for h in y:
#     if h is None:
#         break
#     alldata.append(h.to_dict(skip_empty=False))

```

# 搜索建议数组

[elsaticsearch-dsl中的Suggestions](https://blog.csdn.net/yaohuan2017/article/details/85338508?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param\&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param "elsaticsearch-dsl中的Suggestions")

# dis\_max

```python
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search,Q
client = Elasticsearch(
    "30.79.105.206:80", timeout=10, max_retries=1, retry_on_timeout=False
)

from elasticsearch_dsl.query import DisMax,Bool

dsl = Search(using=client, index="retrieve")

"""
方法一：用Q组装
"""
q1 = Q('bool',
    must = [
        Q('terms', domain=['产品介绍']),
        Q('match', **{'question':{'query':'i康保百万医疗的产品介绍', 'analyzer':"index_ansj"}})
         ],
    should = [Q("term",domain="产品介绍"),Q("term",product="i康保百万医疗")],
    minimum_should_match=1
)
print(q1.to_dict())
print("*"*100)

"""
方法二：用函数组装
"""
Musts = [Q('terms', domain=['产品介绍']), Q('match', **{'question':{'query':'i康保百万医疗的产品介绍', 'analyzer':"index_ansj"}})]
shoulds = [Q("term",domain="产品介绍"),Q("term",product="i康保百万医疗")]
q2 = Bool(must = Musts, should=shoulds, minimum_should_match=1)
print(q2.to_dict())
print("*"*100)

"""
方法三：用空search，再取其query部分
"""
q3 = Search().params(size=3).filter('term', is_deleted=0)\
        .query('match', **{'question': {'query':'i康保百万医疗的产品介绍' , 'analyzer': "index_ansj"}})
print(q3.to_dict())
print("*"*100)

dsl.query = DisMax(queries = [q1,q3.query])
print(dsl.to_dict())
print("*"*100)

res = dsl.params(size=5).source(includes=["question"]).execute()

print(res.success())
for h in res:
    print(h.meta.index)
    print(h.meta.doc_type)
    print(h.meta.id)
    print(h.meta.score)
    print(h.to_dict())
```

    {'bool': {'must': [{'terms': {'domain': ['产品介绍']}}, {'match': {'question': {'query': 'i康保百万医疗的产品介绍', 'analyzer': 'index_ansj'}}}], 'should': [{'term': {'domain': '产品介绍'}}, {'term': {'product': 'i康保百万医疗'}}], 'minimum_should_match': 1}}
    ****************************************************************************************************
    {'bool': {'must': [{'terms': {'domain': ['产品介绍']}}, {'match': {'question': {'query': 'i康保百万医疗的产品介绍', 'analyzer': 'index_ansj'}}}], 'should': [{'term': {'domain': '产品介绍'}}, {'term': {'product': 'i康保百万医疗'}}], 'minimum_should_match': 1}}
    ****************************************************************************************************
    {'query': {'bool': {'filter': [{'term': {'is_deleted': 0}}], 'must': [{'match': {'question': {'query': 'i康保百万医疗的产品介绍', 'analyzer': 'index_ansj'}}}]}}}
    ****************************************************************************************************
    {'query': {'dis_max': {'queries': [{'bool': {'must': [{'terms': {'domain': ['产品介绍']}}, {'match': {'question': {'query': 'i康保百万医疗的产品介绍', 'analyzer': 'index_ansj'}}}], 'should': [{'term': {'domain': '产品介绍'}}, {'term': {'product': 'i康保百万医疗'}}], 'minimum_should_match': 1}}, {'bool': {'filter': [{'term': {'is_deleted': 0}}], 'must': [{'match': {'question': {'query': 'i康保百万医疗的产品介绍', 'analyzer': 'index_ansj'}}}]}}]}}}
    ****************************************************************************************************
