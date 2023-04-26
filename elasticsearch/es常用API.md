# 系统

```Python
GET /
--user elastic:sU0TlaQ4# GET /

GET /_cat/indices
GET /_cat/plugins
GET /_cat/templates

GET /_cluster/state
GET /_cluster/health

```

# mapping

```Python
GET /bot_question/_mapping?include_type_name=true

PUT /test
{
  "mappings": {
    "properties": {
    }
  }
}

PUT /test/_mapping
{
   "properties": {
      "question": {
         "type": "text",
         "fields": {
            "keyword": {
               "type": "keyword",
               "ignore_above": 256
            }
         },
         "analyzer": "index_ansj"
      }
   }
}

```

# 增查

```Python
POST /ysj_question/_doc/1000 插数据
GET /ysj_question/_doc/1000  拿数据
POST /ysj_question/_doc/_mget
{
  "ids":[123,456,12]
}

POST /bot_question/_search   查询数据
{
    "query": {
        "match_all": {}
    }
}

POST /bot_question/_doc/_search
{
   "query": {
      "bool": {
         "must": [
            {
               "match": {
                  "question": {
                     "query": "提供哪些服务",
                     "analyzer": "query_ansj"
                  }
               }
            }
         ],
         "filter": [
            {
               "terms": {
                  "qtype":["app", "ssy"]
               }
            }
         ]
      }
   }
}

```

# 更新

```Python
POST /bot_question/_doc/1/_update     # 更新的内容用doc包起来
{
   "doc":{
       "is_deleted":0
   }
}

POST /bot_question/_doc/_update_by_query  # 把clusterid=1916的question字段修改为指定内容
{
  "query": {
    "term": {
      "clusterid": 1916
    }
  },
  "size":100,
  "script": {
    "lang": "painless",
    "source": "ctx._source.question = params.live_name",
    "params": {
      "live_name": "有了<product>还需要买<product>吗"
    }
  }
}
```

# 删除

```PowerShell
DELETE /ysj_question/_doc/1000
POST /bot_channel_question/_doc/_delete_by_query
DELETE /ysj_question
```

# SQL查询

```PowerShell
POST /_sql?format=txt
{
  "query": "SELECT qid, question FROM bot_faq_question where qid>17080"
}

POST /_sql/translate  # SQL翻译成es查询语法
{
    "query": "select count(*) from bot_faq_question group by qtype",
    "fetch_size": 5000
}
```

# 分词

```Python
POST _all/_close
PUT _all/_settings?preserve_existing=true
{
  "index.analysis.analyzer.default.type":"index_ansj",
  "index.analysis.analyzer.default_search.type":"query_ansj"
}
POST _all/_open

# ansj
GET /_cat/ansj/config
GET /_ansj/flush/config
GET /_ansj/flush/dic
GET /_cat/ansj?text=<product>e生保2020可不可以报销&type=index_ansj&dic=dic&stop=stop&ambiguity=ambiguity&synonyms=synonyms

GET /test/_analyze
{
    "analyzer": "index_ansj",
    "text": "4"
}
```