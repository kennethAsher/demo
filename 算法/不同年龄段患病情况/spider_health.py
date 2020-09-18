# coding:utf-8

import urllib
from bs4 import BeautifulSoup
import pymysql.cursors
import importlib,sys
from queue import Queue
import threading
import re
import time
import ssl

#爬虫需要设置字符类型
importlib.reload(sys)
context = ssl._create_unverified_context()
#获取当前疾病所在的页数起始页，因为前n页太老已经为空，从m页开始才有数值
def check_state():
    conn = pymysql.connect(host = 'localhost',
                           user='root',
                           password='root',
                           db='test',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)
    #初始化链接数据库
    cursor = connection.cursor()
    # 使用 execute()  方法执行 SQL 查询
    sql = "select * from fuck_ill where 1 order by ill_id desc limit 1"
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    return results

#下载页面
def getHtml(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
    req = urllib.request.Request(url,headers=headers)
    page = urllib.request.urlopen(url, context=context)
    print(page)
    html = page.read()
    return html

#获取页面详细信息
def get_info(html):
    soup = BeautifulSoup(html)
    #find默认寻找第一个，find_all使用查找时直接使用[n]取定位寻找的位置,get_text指定拿出文字信息，当信息里面包含其他标签的时候，同意吧所有的都拿出来，
    time = soup.find('div', 'g-under-askT').find_all('span')[0].get_text().strip()
    sex = soup.find('div', 'g-under-askB').find_all('span')[0].get_text()
    age = soup.find('div', 'g-under-askB').find_all('var')[0].get_text()
    #清洗年龄
    age = age.replace('年龄', '')
    age = age.replace('岁', '')
    age = age.replace('：', '')
    title = soup.find('div', 'g-under-askT').find_all('h1')[0].get_text()
    info = soup.find('p', 'crazy_keyword_inlink').get_text()
    # answer = soup.find('div','g-otherask-b article-cont').find_all('div','g-under-askB')[0].get_text()
    # answer = re.sub('\n','',answer)
    answer = ""
    drugs = soup.find('div','g-otherask-b article-cont').find_all('p','crazy_keyword_inlink')
    for i in drugs:
        answer = answer + i.get_text()
    answer = re.sub('\n', '', answer)
    data = {}
    data['time'] = time
    data['sex'] = sex
    data['age'] = age
    data['title'] = title
    data['info'] = info
    data['answer'] = answer
    return data

#将爬取的数据入库：
def add_data(data, id):
    connection = pymysql.connect(host="localhost", user="root",password="root",database="test",charset="utf8")
    cursor = connection.cursor()
    # 使用 execute()  方法执行 SQL 查询
    # sql = "INSERT INTO fuck_ill(age,sex,time,ill_detail,doctor_answer,title,ill_id) VALUES('" + data['age'] + "','" + data['sex'] + "','" + data['time'] + "','" + data['info'] + "','" + data['answer'] + "','" + data['title'] + "','" + id + "')"
    #如果不rollback的话会一直卡死在第一条不成功出，一直不释放，无法插入
    try:
        sql = "INSERT INTO fuck_ill(age,sex,time,ill_detail,doctor_answer,title,ill_id) VALUES('%s','%s','%s','%s','%s','%s','%s')" %(data['age'],data['sex'],data['time'],data['info'],data['answer'],data['title'],id)
        cursor.execute(sql)
        connection.commit()
    except:
        connection.rollback()
    cursor.close()




#获取数据入库，线程任务
def do_scan(ill_id):
    x_s = str(ill_id)
    html = getHtml('https://m.120ask.com/askg/posts_detail/' + x_s)
    try:
        results = get_info(html)
    except Exception as e:
        pass
    else:
        try:
            add_data(results, x_s)
        except Exception as e:
            pass
        else:
            pass
        pass



#线程
def worker():
    while not q.empty():
        ill_id = q.get()
        do_scan(ill_id)
        time.sleep(1)

# a = check_state()
# newest =  a[0]['ill_id']
#该网站数值小的网址为空值
newest = 2200000
goal = newest + 100000
q = Queue()
#将任务都加载到队列中
for x in range(newest,goal):
    q.put(x)

for i in range(50):
    t = threading.Thread(target=worker)
    t.setDaemon(True)
    t.start()

while True:
    if threading.activeCount() <= 1:
        break
    else:
        try:
            time.sleep(1)
        except KeyboardInterrupt as e:
            print('\n[WARNING] User aborted, wait all slave threads to exit, current(%i)' % threading.activeCount())
            exit()