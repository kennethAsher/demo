# coding:utf-8
import importlib,sys
from queue import Queue
import urllib
from bs4 import BeautifulSoup
import pymysql.cursors
import threading
import re
import subprocess
import os
import time
importlib.reload(sys)

'''
监听爬虫程序，入库比较慢的时候重新启动爬虫
'''

def check_state():
    conn = pymysql.connect(host='localhost', user='root',password='root',database='test',charset='utf8')
    cursor = conn.cursor()
    #拿到第一条消息
    sql = "select * from fuck_ill where 1 order by ill_id desc limit 1"
    cursor.execute(sql)
    #返回搜索到的内容
    result = cursor.fetchall()
    cursor.close()
    return result

a = check_state()
#拿到搜索到内容的第一条的id字段
newest =  a[0]['ill_id']
time.sleep(3)
print('the newest id is:'+str(newest))
#重新启动爬虫
while True:
    a = check_state()
    new = a[0]['ill_id']
    if ((new - newest) < 20):
        print('ready to restart health')
        try:
            std.kill()    #杀死其他进程
        except Exception as e:
            print(e)
            print('kill std fail')
        else:
            print('kill std sucess')
        std = subprocess.Popen('python health.py')
    else:
        how = int(new) - int(newest)
        how = str(how)
        newest = new
        print('fetch ' + how + ' datas in the last 5 seconds')
    time.sleep(5)