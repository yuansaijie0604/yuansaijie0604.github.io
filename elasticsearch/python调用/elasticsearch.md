# elasticsearch

# 建数据库

```python
import elasticsearch
es = elasticsearch.Elasticsearch(hosts=[{"host": "30.79.105.206", "port": 80}])
# es = elasticsearch.Elasticsearch(hosts=[{"host": "30.23.109.145", "port": 80}], \
#                                  http_auth=('elastic', 'sU0TlaQ4#'),\
#                                  timeout=10, \
#                                  max_retries=1, \
#                                  retry_on_timeout=False)

# create index
myindex = "yuansaijie"
faqbody = {
    "mappings": {
        "properties": {
            "id": {"type": "integer"},
            "is_standard": {"type": "integer"},
            "is_deleted": {"type": "integer"},
            "question": {
                "type": "text",
                "analyzer": "index_ansj"
            },
            "answer": {"type": "text"},
            "domain": {"type": "keyword"},
            "groupid": {"type": "integer"},
            "product": {"type": "keyword"},
            "keyword": {"type": "keyword"},
            "create_time": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
            "update_time": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"}
        }
    }
}
res = es.indices.create(index=myindex, ignore=400, body=faqbody)
print(res)
```

# 批量插入数据

```python
import elasticsearch
from elasticsearch import helpers
es = elasticsearch.Elasticsearch(hosts=[{"host": "30.79.105.206", "port": 80}])

import datetime

data = pd.read_excel("all_data.xlsx")
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
data.fillna({"images": "", "files": ""}, inplace=True)
data.rename(columns={"Products": "products"}, inplace=True)
data["create_time"] = now
data["update_time"] = now
data["is_deleted"] = 0

rows = data.shape[0]
for i in range(0, rows, 1000):
    action = []
    for k in range(i, min(i + 1000, rows)):
        d = data.loc[[k]].to_dict("records")[0]
        d["id"] = k
        d["flag"] = int(d["flag"])
        d["products"] = list(eval(d["products"]))
        action.append({
            "_index": myindex,
            "_type": "_doc",
            "_id": str(k),
            "_source": d
        })
    helpers.bulk(es, action)
```

# 逐条插入

```python
ysj_dict = df.to_dict("records")    # dataframe to dict

from tqdm import tqdm
for i in tqdm(range(len(ysj_dict))):
    d = ysj_dict[i]
    result = es.index(index='chitchat', doc_type='_doc', body=d, id=i)
    
print("DONE!!!!!")
```

# 查询数据

```python
import elasticsearch
es = elasticsearch.Elasticsearch(hosts=[{"host": "30.79.105.206", "port": 80}])
dsl = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"question": {"query": "我想理赔", "analyzer": "index_ansj"}}}
                ],
                "filter": [
                    {"term": {"is_deleted": 0}}
                ]
            }
        },
        "size": 5
}

res = es.search(index="xiaoan", body=dsl)

result = []
for d in res["hits"]["hits"]:
    score = d["_score"]
    print(d["_source"]["question"])
```

# 更新数据

修改已知id的某字段值

```python
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search,Q
client = Elasticsearch(
    "30.79.105.206:80", timeout=10, max_retries=1, retry_on_timeout=False
)

dsl ={
    "doc":{"is_deleted":1} 
}

# id此范围内为 待删数据
for k in range(18721,18938):
    client.update("faq",k,body=dsl)
```
