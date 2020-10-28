##### API 文档

------

1. **GET**    /news/index0    查询50条实时微博热搜

   **Parameters：**no parameters

   **Responses：**

   | code | description                                                  |
   | ---- | ------------------------------------------------------------ |
   | 200  | 返回新闻列表:                                                                                                                                      [        {                                                                                                                                                                     'id':1,                                                                                                                                        'title':"青岛核酸检测已采样307万份",                                                                                                                                              'hot':1113715                                                                                                                               },....  ] |
   | 400  | 参数异常                                                     |

2. **GET**      /news/wordcloud/\<cluster_id\>/\<topk\>  返回对应簇的topk词语词频

   **Parameters：**cluster_id: 新闻簇的编号，[0,20)的整数；

   ​                           topk：返回前k个频率最高的词的词频，可根据前端展示美观程度进行调整。

   **Responses：**

   | code | description                                                  |
   | ---- | ------------------------------------------------------------ |
   | 200  | 返回词频字典:                                                                                                                                      {"回购": 148, "亿元": 67, "公司": 63, "股份": 54, "格力电器": 52 ...} |
   | 400  | 参数异常                                                     |

## 数据搜索

### 接口设计

#### 接口说明

|   类目   |    说明     |
| :------: | :---------: |
| 请求方法 |     GET     |
| url定义  | news/search |

#### 参数说明

| 参数名 |  类型  | 是否必须 |     描述     |
| :----: | :----: | :------: | :----------: |
|   q    | 字符串 |    否    | 查询的关键字 |

#### 返回结果实例

搜索：http://127.0.0.1:8000/news/search/?q=a

```json
{
    "code": 200,
    "data": [
        {
            "_index": "xxswl",
            "_type": "modelresult",
            "_id": "news.articles.214",
            "_score": 3.8047872,
            "_source": {
                "id": "news.articles.214",
                "django_ct": "news.articles",
                "django_id": "214",
                "text": "602份A股季报预告：医药生物“冰火两重天”\n\nsina_mobile\n",
                "title": "602份A股季报预告：医药生物“冰火两重天”",
                "author": "sina_mobile",
                "body": ""
            }
        },
        {
            "_index": "xxswl",
            "_type": "modelresult",
            "_id": "news.articles.187",
            "_score": 3.5242052,
            "_source": {
                "id": "news.articles.187",
                "django_ct": "news.articles",
                "django_id": "187",
                "text": "A股开盘倒计时 长假海外市场一波三折影响几何？\n\nsina_mobile\n",
                "title": "A股开盘倒计时 长假海外市场一波三折影响几何？",
                "author": "sina_mobile",
                "body": ""
            }
        },
        {
            "_index": "xxswl",
            "_type": "modelresult",
            "_id": "news.articles.15",
            "_score": 3.398881,
            "_source": {
                "id": "news.articles.15",
                "django_ct": "news.articles",
                "django_id": "15",
                "text": "中1签狂赚11万、医美巨头首秀火了 股价冲进A股前十\n\nsina_mobile\n",
                "title": "中1签狂赚11万、医美巨头首秀火了 股价冲进A股前十",
                "author": "sina_mobile",
                "body": ""
            }
        },
        {
            "_index": "xxswl",
            "_type": "modelresult",
            "_id": "news.articles.157",
            "_score": 3.2821636,
            "_source": {
                "id": "news.articles.157",
                "django_ct": "news.articles",
                "django_id": "157",
                "text": "海外股市普涨、A股10月“开门红”稳了？六大券商最新观点出炉\n\nsina_mobile\n",
                "title": "海外股市普涨、A股10月“开门红”稳了？六大券商最新观点出炉",
                "author": "sina_mobile",
                "body": ""
            }
        },
        {
            "_index": "xxswl",
            "_type": "modelresult",
            "_id": "news.articles.213",
            "_score": 3.2821636,
            "_source": {
                "id": "news.articles.213",
                "django_ct": "news.articles",
                "django_id": "213",
                "text": "又一家：太平人寿宣布终止以19亿元参与中联重科A股定增\n\nsina_mobile\n",
                "title": "又一家：太平人寿宣布终止以19亿元参与中联重科A股定增",
                "author": "sina_mobile",
                "body": ""
            }
        },
        {
            "_index": "xxswl",
            "_type": "modelresult",
            "_id": "news.articles.182",
            "_score": 3.1731968,
            "_source": {
                "id": "news.articles.182",
                "django_ct": "news.articles",
                "django_id": "182",
                "text": "假期全球涨声一片：港股科技股最猛一天飙升20% A股开门红稳了？\n\nsina_mobile\n",
                "title": "假期全球涨声一片：港股科技股最猛一天飙升20% A股开门红稳了？",
                "author": "sina_mobile",
                "body": ""
            }
        }
    ]
}
```
   

