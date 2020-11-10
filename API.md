##### API 文档

------

一、news服务 
1. **GET**    /news/index0    查询50条实时微博热搜

   **Parameters：**  no parameters

   **Responses：**

   | code | description                                                  |
   | ---- | ------------------------------------------------------------ |
   | 200  | 返回新闻列表:                                                                                                                                      [        {                                                                                                                                                                     'id':1,                                                                                                                                        'title':"青岛核酸检测已采样307万份",                                                                                                                                      'hot':1113715,                                                                                                                            },....  ] |
   | 400  | 参数异常       

2. **GET**    /news/index1    查询50条实时微博要闻

   **Parameters：**  no parameters

   **Responses：**

   | code | description                                                  |
   | ---- | ------------------------------------------------------------ |
   | 200  | 返回新闻列表:                                                                                                                                      [        {                                                                                                                                                                     'id':0,                                                                                                                                        'title':"#进口冷链食品不提供消毒证明不能上市#",                                                                                                                                      'url':"https://s.weibo.com/weibo?q=%23%E8%BF%9B%E5%8F%A3%E5%86%B7%E9%93%BE%E9%A3%9F%E5%93%81%E4%B8%8D%E6%8F%90%E4%BE%9B%E6%B6%88%E6%AF%92%E8%AF%81%E6%98%8E%E4%B8%8D%E8%83%BD%E4%B8%8A%E5%B8%82%23"                                                                                                                              },....  ] |
   | 400  | 参数异常  


3. **GET**    /news/index2    查询50条最新新闻

   **Parameters：**  no parameters

   **Responses：**

   | code | description                                                  |
   | ---- | ------------------------------------------------------------ |
   | 200  | 返回新闻列表:                                                                                                                                      [{"title": "特斯拉回应上海工厂明年计划生产55万辆：无法公布具体数字", "url": "https://finance.sina.cn/chanjing/gsxw/2020-11-09/detail-iiznctke0409104.d.html", "time": "2020-11-09 13:17:53"}......] |
   | 400  | 参数异常  


4. **GET**      /news/wordcloud/\<cluster_id\>/\<topk\>  返回对应簇的topk词语词频

   **Parameters：**  cluster_id: 新闻簇的编号，[0,20)的整数；

   ​                           topk：返回前k个频率最高的词的词频，可根据前端展示美观程度进行调整。

   **Responses：**

   | code | description                                                  |
   | ---- | ------------------------------------------------------------ |
   | 200  | 返回词频字典:                                                                                                                                      {"回购": 148, "亿元": 67, "公司": 63, "股份": 54, "格力电器": 52 ...} |
   | 400  | 参数异常   |


5. **GET**      /news/timeline/\<keyword\>/\<starttime\>/\<endtime\> 返回和该关键词有关的、时间在starttime和endtime之间的新闻列表

   **Parameters：**  keyword: 关键词,如"特朗普","新冠","美股";
                     starttime,endtime: 时间戳

   **Responses：**

   | code | description                                                  |
   | ---- | ------------------------------------------------------------ |
   | 200  | 返回新闻列表:                                                                                                                                      [{"title": "佩洛西拒绝特朗普的新冠援助提议 迅速达成协议的希望变得渺茫", "time": 1602601920, "body": "美国众议院议长佩洛西...."},...]|
   | 400  | 参数异常                                                     |

 

二、heatmap服务
1. **GET**      /heatmap/heatmap/\<cluster_id\>/\<starttime\>/\<endtime\> 返回对应簇的、时间在starttime和endtime之间【取日期的闭区间】的热力图数据

   **Parameters：**   cluster_id: 新闻簇的编号，[0,20)的整数；
                     starttime,endtime: 时间戳 ，如： 参数为时间戳2020-10-13 18:27:57 到 时间戳2020-10-29 14:14:36，返回的数据是 [2020-10-13 0:0:0,2020-10-29 23:59:59]的数据
   
   **Responses：**

| code | description                                                  |
| ---- | ------------------------------------------------------------ |
| 200  | 返回热力图列表:                                                                                                                                      [{ "lng": 121.48789948569473, "lat": 31.24916171001514,"count": 75},...]|
| 400  | 参数异常                                                     |



三、search服务 （含复合型接口）

1. **GET**      /news/search/ 新闻搜索

   **Parameters：**

   | 参数名      | 类型   | 是否必须       | 描述                     |
   | :---------- | ------ | -------------- | ------------------------ |
   | q           | 字符串 | 否，默认为“a”  | 查询的关键字             |
   | from        | 字符串 | 否，默认到最初 | 查询的起始日期（开区间） |
   | to          | 字符串 | 否，默认到最后 | 查询的终止日期（闭区间） |
   | start_index | 整型   | 否，默认0      | 查询的起始编号           |

   **Responses example：**

   | code | description                                                  |
   | ---- | ------------------------------------------------------------ |
   | 200  | `response["data"]["total"]["value"]`为搜索结果的总数；`response["data"]["hits"]`为搜索结果的列表，列表内为以start_index为起始的10条新闻。 |
   | 400  | 参数异常                                                     |

   http://127.0.0.1:8000/news/search/?q=a&from=2020-10-15&start_index=1

   ```json
   {
       "code": 200,
       "data": {
           "total": {
               "value": 8,
               "relation": "eq"
           },
           "max_score": 4.635893,
           "hits": [
               {
                   "_index": "xxswl",
                   "_type": "modelresult",
                   "_id": "news.articles.1322",
                   "_score": 3.853687,
                   "_source": {
                       "id": "news.articles.1322",
                       "django_ct": "news.articles",
                       "django_id": "1322",
                       "text": "名创优品上市首日 收盘较发行价涨4.4%\n新浪……划在纽交所上市。文件显示，与腾讯有关联的实体在发行股票后将拥有名创优品4.8%的股份。高盛和美国银行证券是此次发行的承销商。\nsina_mobile\n创优,品,发行价,名,首日,存托,纽交所,涨名,美国,文件,多亿美元,股类,端名,腾讯,筹资,每份,股份,上市,普通股,日名\n",
                       "title": "名创优品上市首日 收盘较发行价涨4.4%",
                       "author": "sina_mobile",
                       "body": "新浪科技……的承销商。",
                       "url": "https://tech.sina.cn/it/2020-10-16/detail-iiznctkc5804589.d.html",
                       "time": "2020-10-16T04:28:23",
                       "keywords": "创优,品,发行价,名,首日,存托,纽交所,涨名,美国,文件,多亿美元,股类,端名,腾讯,筹资,每份,股份,上市,普通股,日名",
                       "cluster_id": 19,
                       "emotion": 0.9242208121794773
                   }
               },
           …………………………………………（共返回十条）
           ]
       }
   }
   ```

   

2. **GET**      /news/search_heatmap/ 新闻搜索+热力图

   **Parameters：**

   | 参数名 | 类型   | 是否必须       | 描述                     |
   | :----- | ------ | -------------- | ------------------------ |
   | q      | 字符串 | 否，默认为“a”  | 查询的关键字             |
   | from   | 字符串 | 否，默认到最初 | 查询的起始日期（开区间） |
   | to     | 字符串 | 否，默认到最后 | 查询的终止日期（闭区间） |

   **Response example：**

   | code | description                                                  |
   | ---- | ------------------------------------------------------------ |
   | 200  | `response["data"]["search_res"]`和`response["data"]["heatmap"]`分别为针对查询内容的新闻搜索结果和对应的热力图 |
   | 400  | 参数异常                                                     |

   http://127.0.0.1:8000/news/search_heatmap/?q=a&from=2020-10-13

   ```json
   {
       "code": 200,
       "data": {
           "search_res": [
               {
                   "_index": "xxswl",
                   "_type": "modelresult",
                   "_id": "news.articles.362",
                   "_score": 0.96147084,
                   "_source": {
                       "id": "news.articles.362",
                       "django_ct": "news.articles",
                       "django_id": "362",
                       "text": "暴风还值得救吗？\n欢迎关注“创事记”的微信订阅号：sinachuangshiji　文/森语谢东霞编辑/……值得救吗？”\nsina_mobile\n暴风,风行,影音,冯鑫,播放器,电视,体育,视频,图源,拯救,会员,在线,代,驰,集团,互联网,兆,广告,救,蔡文胜\n",
                       "title": "暴风还值得救吗？",
                       "author": "sina_mobile",
                       "body": "欢迎关注“创事记”的微信订阅号：sinachuangshiji　文/森语谢东霞编辑/子夜沉寂已久的暴风，又有了新动静。&nbsp;10月9日，不少网友发现，暴风影音官网上的Windows版客户端完成了……",
                       "url": "http://tech.sina.cn/csj/2020-10-13/doc-iiznezxr5776210.d.html",
                       "time": "2020-10-13T20:08:41",
                       "keywords": "暴风,风行,影音,冯鑫,播放器,电视,体育,视频,图源,拯救,会员,在线,代,驰,集团,互联网,兆,广告,救,蔡文胜",
                       "cluster_id": 2,
                       "emotion": 1.0
                   }
               },
               ………………
           ],
           "heatmap": [
               {
                   "lng": 116.39564503787867,
                   "lat": 39.92998577808024,
                   "count": 74
               },
               ………………
           ]
       }
   }
   ```

3. **GET**      /news/search_date_cluster_info/ 热点演进按照日期统计

   **Parameters：**

   | 参数名 | 类型   | 是否必须      | 描述         |
   | :----- | ------ | ------------- | ------------ |
   | q      | 字符串 | 否，默认为“a” | 查询的关键字 |

   **Response example：**

   | code | description                                      |
   | ---- | ------------------------------------------------ |
   | 200  | `response["data"]`是一个日期对应该日期信息的字典 |
   | 400  | 参数异常                                         |

   | 位置                                              | 含义                                             |
   | ------------------------------------------------- | ------------------------------------------------ |
   | `response["data"][某日期]["num"]`                 | 搜索到该日期的新闻数量                           |
   | `response["data"][某日期]["cluster_ids"]`         | 该日期的聚类id及对应信息                         |
   | `response["data"][某日期]["cluster_ids"][聚类ID]` | 聚类id对应的数量和关键词列表（按照出现次数排序） |

   http://127.0.0.1:8000/news/search_date_cluster_info/?q=a

   ```json
   {
       "code": 200,
       "data": {
           "2020-10-15": {
               "num": 46,
               "cluster_ids": {
                   "2": {
                       "id_num": 4,
                       "keywords": [
                           "学校",
                           "课程",
                           "学生",
                           …………
                       ]
                   },
                   "1": {
                       "id_num": 10,
                       "keywords": [
                           "手机",
                           "苹果",
                           "基金",
                           …………
                       ]
                   },
                   …………
               }
           },
           "2020-10-13": {
               "num": 50,
               "cluster_ids": {
                   "13": {
                       "id_num": 2,
                       "keywords": [
                           "升势",
                           "股指",
                           …………
                       ]
                   },
                 	…………
               }
           },
           …………
       }
   }
   ```

   