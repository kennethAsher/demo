# encoding=utf-8
# ----------------------------------------
#   版本： 0.1
#   日期： 2018-01-17
#   作者： TDLang
#
#   项目状态：
#         a.基本测试已经通过，可以正常下载和解析页面。
#   项目问题：
#         a.部分网站内容通过BeautifulSoup 解析失败，出现乱码  （小问题）
#         b.存储url的redis队列没有做去重操作，会造成网页的重复下载  （大问题）
# -----------------------------------------



'''
电信dpi项目中，url识别子项目： 爬虫部分
 '''


'''
网页下载
'''
def dowmhtml(url):
    import  urllib.request
    # 请求
    # 爬取结果
    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        data = response.read()
        #.decode('utf8')
        return response, data
    except Exception as err :
        return None, None



'''
采用BeautifulSoup 获取网页的主题（title）
'''
def get_title_BeautifulSoup(htmldata):
    '''
    :param htmldata:
    :return: title 网页主题
    '''
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(htmldata ,'html.parser') #html.parser Python的内置标准库、执行速度适中 、文档容错能力强
    if soup==None:
        return  'null'
    else:
        try:
            title = soup.title.string
            return title
        except:
            print(soup)


''''
采用BeautifulSoup 解析页面中的内容

'''
def  get_url_BeautifulSoup( htmldata):
    '''
    :param: htmldata
    :return: url
    '''
    url_data = {}
    url = []
    url_type = []

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(htmldata,'html.parser')
    for link in soup.find_all('a'):
            url_str = link.get('href')
            print(url_str)

    url_data['url'] = url
    url_data['url_type'] = url_type
    return url_data


def save_data_demo1(response,title):
   import pymysql
   db = pymysql.connect(host='localhost',port=3306,user='root',passwd='root',db='spider',charset='utf8')
   cursor = db.cursor()
   try:
        sql = "INSERT INTO demo1 (url,title) VALUES ('%s', '%s' )" % (response.geturl(), title)
        cursor.execute(sql)
        db.commit()
   except :
        db.rollback()
   db.close()

def save_data_demo2(url_data):
    import pymysql
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='spider', charset='utf8')
    cursor = db.cursor()
    url = url_data['url']
    type = url_data['url_type']
    #
    for (i1,i2) in zip(url,type):
        if i2 !=None and 'http' in i1:
            try:
                sql = "INSERT INTO demo2 (url,type) VALUES ('%s', '%s' )" % (i1, i2)
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
    db.close()

def save_url_redis(new_urls):
    redisconn = get_redisconn_util()
    #line=''
    #while line != None:
    #   line = redisconn.rpop('spider_url')
    #    if line != None:
    #        line =line
    #        new_urls.append(line)
    #    else:
    #        break
    new_urls = list(set(new_urls))
    for line in new_urls:

        if line !=None:
            redisconn.lpush('spider_url',line)

def get_redisconn_util():
    import redis
    #线程池
    pool = redis.ConnectionPool(host='192.168.5.134',port=6379)
    return redis.Redis(connection_pool=pool)



'''对单个网页的操作'''
def spider_run(url):
    #下载页面
    response, html = dowmhtml(url)
    # 调试信息
    print(html)
    print(type(response))
    print(response.info())
    print(response.geturl())
    # 解析页面 <title></title>标签
    if html !=None:
        title = get_title_BeautifulSoup(html)
    # 网站主题信息数据写入数据库表
        #if  response  !=None:
            #save_data_demo1(response, title)

    # 解析页面中的url  放到爬取队列
        #url_data = get_url_BeautifulSoup(html)
    #网站类别数据写入数据库表
        #save_data_demo2(url_data)
    #
    # 需要写一个写入动态队列（redis）
#        save_url_redis(url_data['url'])

    # 写入队列的数据进行去重
    
def push_data():
    url2 = 'https://www.hao123.com'
    redisconn = get_redisconn_util()
    redisconn.lpush('spider_url',url2)
def run():
    redisconn = get_redisconn_util()
    load_url = ''
    while load_url != None:
        load_url = redisconn.rpop('spider_url')
        num = redisconn.sadd('sider_used_url',load_url)
        if load_url != None and num == 1:
            print(load_url.decode())
            spider_run(load_url.decode())

if __name__ == '__main__':
    htmldata=dowmhtml('https://movie.douban.com/')
    print(htmldata)
    #get_url_BeautifulSoup(htmldata)
















