import os
import time
from datetime import datetime
import requests
from pymongo import MongoClient

class MaoYan(object):
    '''
    猫眼电影影评爬虫
    '''
    def __init__(self):
        '''
        初始化函数
        headers:请求头
        time: 当前时间戳
        premiere_time:首映电影时间戳
        '''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.'
                          '38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'Connection': 'keep-alive',
            'Cookie': '_lxsdk_cuid=168d5d128e7c8-033114908a580c-10376654-fa000-168d5d128e7c8;'
                      ' _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; uuid_n_v=v1;'
                      ' iuuid=5D49FF702DB211E9AF1B8D0648275EC02D381B7848144BC1A299A63C05094BF5;'
                      ' webp=true; selectci=true; ci=281%2C%E6%83%A0%E5%B7%9E;'
                      ' __mta=247299643.1549775481575.1549783540088.1549862773375.3;'
                      ' _lxsdk=5D49FF702DB211E9AF1B8D0648275EC02D381B7848144BC1A299A63C05094BF5;'
                      ' _lxsdk_s=168db05185a-332-e0d-bc5%7C%7C157'
        }
        self.time = int(time.time())*1000
        self.premiere_time = int(time.mktime(time.strptime('2019-02-05 00:00:00', '%Y-%m-%d %H:%M:%S'))*1000)

        #配置mongodb数据库
        # host = os.environ.get('MONGODB_HOST', '127.0.0.1')  #os.environ 获取系统环境变量
        # port = os.environ.get('MONGODB_PORT', '27017')
        # mongo_url = 'mongodb://{}:{}'.format(host, port)
        client = MongoClient(host='localhost', port=27017)
        mongo_db = client.maoyan
        # mongo_db = os.environ.get('MONGODB_DATABASE', 'maoyan')
        # client = MongoClient(mongo_url)
        self.db = mongo_db
        # self.db['maoyan'].create_index('id', unique=True)   #以评论的id为主键，进行去重

    def get_comment(self):
        '''
        爬取首映到当前时间的所有影评
        url：评论真实的url， ts为时间戳
        :return:
        '''
        url = 'http://m.maoyan.com/review/v2/comments.json?movieId=248906&userId=-1&' \
              'offset={}&limit=15&ts={}&type=3'
        offest = 0
        while offest < 10000:
            url.format(offest, self.time)
            res = requests.get(url, headers = self.headers)
            print(res)
            # count = 0
            for com in res.json()['data']['comment']:
                self.parse_comment(com)
                # count += 1
                # if count == 15:
                #     offest += 15
            offest += 15
        print(f'成功爬取到{offest}的数据')

    def parse_comment(self, com):
        '''
        解析函数：用来解析爬虫爬取回来的json数据，并且存到mongodb数据库中
        com：每条爬取回来的json数据
        :param com:
        :return:
        '''
        comment = {
            'content': com['content'], 'gender': com['gender'], 'id': com['id'],
            'nick': com['nick'], 'replyCount': com['replyCount'], 'score': com['score'],
            'time': com['time'], 'upCount': com['upCount'],
            'userId': com['userId'], 'userLevel': com['userLevel']
        }    #构造评论字典
        # self.db['maoyan'].update_one({'id': comment['id']}, {'$set': comment}, upsert=True)
        self.db.insert(comment)

if __name__ == '__main__':
    my = MaoYan()
    my.get_comment()