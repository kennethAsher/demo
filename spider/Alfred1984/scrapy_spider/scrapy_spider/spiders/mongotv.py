# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import Request

class MongotvSpider(scrapy.Spider):
    name = 'mongotv'
    allowed_domains = ['mongotv.com']
    subject_id = 4327535  # 视频的id
    pages = list(range(1, 638))  # 需要爬取的评论页数

    def start_requests(self):  #重写start_request函数
        start_urls = ['https://comment.mgtv.com/video_comment/list/?callback='
                      'jQuery182040635960604983135_1524066975165&_support=10000000'
                      '&type=hunantv2014&subject_id={}&page={}'.format(self.subject_id,page) for page in self.pages]
        # 生成所有需要爬取的url保存进start_urls
        for url in start_urls:  #遍历start_utls发出的请求
            # print('==============================')
            yield Request(url)
    def parse(self, response):
        _text = response.text[response.text.find('{'):-1]  #通过字符串选取的方式吧‘jQuery...()’去掉
        json_data = json.loads(_text)                      #转成json格式
        for i in json_data['comments']:# 遍历每页的评论列表
            item = {'comment_id':i['comment_id'],         #取出comment_id用来作为唯一标识符
                    'comments':i}                         #每条评论的相关信息全部塞进'comments'
            # print('+++++++++++++++++++++++++++++')
            yield item                                    #yield item之后，会进入到pipelines进行处理
