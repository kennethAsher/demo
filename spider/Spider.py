
'''

'''
def save_data_demo1(response,title):
    import pymysql
    db = pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='spider',charset='utf8')
    cursor = db.cursor()
    try:
        sql = "insert into demo1(url,title) values('%s','%s')" %(response.geturl(),title)
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
    db.close()
def save_data_demo2(url_data):
    import pymysql
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='spider', charset='utf8')
    cursor = db.cursor()
    url = url_data['url']
    _type = url_data['url_type']

    for (i1,i2) in zip(url, _type):
        if i2 != None and 'http' in i1:
            try:
                sql = "INSERT INTO demo2 (url,type) VALUES ('%s', '%s' )" % (i1, i2)
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
        db.close()

def save_url_redis(new_urls):
    redisconn = get_redisconn_util()
    # line=''
    # while line != None:
    #   line = redisconn.rpop('spider_url')
    #    if line != None:
    #        line =line.decode()
    #        new_urls.append(line)
    #    else:
    #        break
    new_urls = list(set(new_urls))
    for line in new_urls:

        if line != None:
            redisconn.lpush('spider_url', line)
'''
采用BeautifulSoup 获取网页的主题（title）
'''
def get_title_BeautifulSoup(html_data):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_data, 'html.parser')  # html.parser Python的内置标准库、执行速度适中 、文档容错能力强
    if soup:
        try:
            title = soup.title.string
            return title
        except:
            print(soup)
    else:
        return 'null'
'''
采用BeautifulSoup 解析页面中的内容
'''
def get_url_BeautifulSoup(html_data):

    url_data = {}
    url = []
    url_type = []

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_data,'html.parser')
    for link in soup.find_all('a'):
        url_str = link.get('href')
        try:
            if '.com' in url_str or '.cn' in url_str and '.exe' not in url_str and '.png' not in url_str and '.pdf' not in url_str:
                if 'http' not in url_str:
                    url_str = 'https' + url_str
                    # url_split = url_str.split('/')
                    # url_str = url_split[0] + '//' + url_split[2]
                    url.append(url_str)
                    url_type.append(link.string)
                else:
                    # url_split = url_str.split('/')
                    # url_str = url_split[0] + '//' + url_split[2]+'/'+url_split[3]
                    url.append(url_str)
                    url_type.append(link.string)
        except Exception as e:
            print('url参数为空',e)
    url_data['url'] = url
    url_data['url_type'] = url_type
    # print(url_data['url'])
    # print('***********************************')
    # print(url_data['url_type'])
    return url_data

'''
下载页面
'''
def downhtml(url):
    import urllib.request
    #请求
    #爬取结果
    try:
        request = urllib.request.Request(url)   #下载页面
        response = urllib.request.urlopen(request)  #打开页面
        data = response.read()
        return response,data
    except Exception as e:
        return None,None


def spider_run(url):
    # 下载页面
    response,html = downhtml(url)

    # 调试信息
    # print(html)      #输出页面
    # print(type(response))     #页面的类型
    # print(response.info())    #次返回值的介绍
    # print(response.geturl())  #返回值所使用的url

    # 解析页面 <title></title>标签
    if html:
        title = get_title_BeautifulSoup(html)
        print(title)

        # 网站主题信息数据写入数据库表
        if response:
            save_data_demo1(response, title)
        # 解析页面中的url  放到爬取队列
        url_data = get_url_BeautifulSoup(html)
        # 网站类别数据写入数据库表
        save_data_demo2(url_data)

        #
        # 需要写一个写入动态队列（redis）
        # save_url_redis(url_data['url'])

        # 写入队列的数据进行去重




def get_redisconn_util():
    import redis
    # 线程池
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    return redis.Redis(connection_pool=pool)

def run():
    redis_conn = get_redisconn_util()
    load_url = ''
    while load_url != None:
        load_url = redis_conn.rpop('spider_url')
        num = redis_conn.sadd('spider_used_url',load_url)   #添加一条，如果数据里面有返回0，没有的话返回1
        if load_url != None and num == 1:
            print(load_url.decode())
            spider_run(load_url.decode())


def push_data():
    url2 = 'https://www.hao123.com'
    redis_conn = get_redisconn_util()
    redis_conn.lpush('spider_url',url2)

if __name__ == '__main__':
    # push_data()
    # run()
    spider_run('https://www.hao123.com')