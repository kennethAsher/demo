# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy.conf import settings
from pymongo.errors import DuplicateKeyError
from traceback import format_exc

class ScrapySpiderPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_url = mongo_uri
        self.mongo_db = mongo_db
        self.client = MongoClient(mongo_uri)
        self.db = self.client[mongo_db]

    @classmethod
    def from_crawler(cls, crawler):  # 定义类方法，提取出mongodb配置   先执行此步骤，在执行init
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URI'),
            mongo_db=settings.get('MONGODB_DATABASE', 'items')
        )

    def close_spider(self,spider):
        _ = spider
        self.client.close()    #关闭数据库

    def process_item(self, item, spider):
        try:

            self.db['mongotv1'].update({'comment_id': item['comment_id']}, {'$set': {'comment':item}}, upsert=True)   #True代表如果是新的就插入
            # 通过comment_id判断，有就更新，没有就插入
        except DuplicateKeyError:
            spider.logger.debug('duplicate key error collection')  # 唯一键冲突报错
        except Exception as e:
            _ = e
            spider.logger.error(format_exc())
        return item
