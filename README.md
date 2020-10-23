# backend of xxswl 

The backend was bootstrapped with [`django-admin startproject app`](https://docs.djangoproject.com/en/2.2/ref/django-admin/).

## Comments for project content 




## 单元测试
测试入口：各文件夹中的 tests.py 
推荐各功能模块自己实现测试模块，例：新建 funcAtests.py （pytest写法），在此目录的 tests.py 中import  funcAtests。
> 示例  https://gitlab.secoder.net/example/monolithic-example/-/blob/master/meeting/tests.py

## Comments for CI/CD

> frame from: https://gitlab.secoder.net/example/monolithic-example

### Structure

* __app__ Core settings for Django.
* __meeting__ Created by `python manage.py startapp meeting`.
* __manage.py__   settings for Django.

==the following files should remain unmodified==
* __pytest.ini__ Configuration for [pytest](https://docs.pytest.org/en/latest/).
* __requirements.txt__ Package manager with `pip`.
* __requirements_dev.txt__ Package manager with `pip`, including extra tools for development.
* **Dockerfile**  configure our docker image to run,  ' EXPOSE 80 '  set the port we can use
* **.gitlab-ci.yml**  configure  our CI/CD settings
* **sonar-project.properties**  configure  sonar 

### Tools

* `python manage.py runserver` Run this project in development mode.
* `python manage.py makemigrations` Detect changes in data schema.
* `python manage.py migrate` Apply migrations to current database.
* `pytest` Test.
* `pylint --load-plugins=pylint_django app meeting` Advanced [PEP8](https://www.python.org/dev/peps/pep-0008/) checking.

### Usage  [ I haven't  tried yet ]

    docker build -t something .
    docker run --rm something

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

