# encoding=utf-8
# --------------------------------------------------------------
#    版本：0.0.1
#    日期：2018—01-25
#    author： TDLang
#
#   项目描述： 爬取一个特定网站 （http://www.fynas.com/ua），用来补充DPI项目中usr_agent 的解析  手机
#
#
# --------------------------------------------------------------

'''
下载页面
'''
def download_homl(url):
    import urllib.request
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    data = response.read()
    return data

'''
存储在mysql中
'''
def save_uerAgent_mysql(i1,i2,i3,i4):
    import pymysql
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='spider', charset='utf8')
    # db = pymysql.connect('localhost','root','','spider')
    cursor = db.cursor()
    try:
        sql = "INSERT INTO user_agent (mobile_phone,phone_type,app,user_agent) VALUES ('%s', '%s', '%s', '%s' )" % (i1, i2, i3, i4)
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    # sql = "INSERT INTO user_agent (mobile_phone,phone_type,app,user_agent) VALUES ('%s', '%s', '%s', '%s' )" % (
    # i1, i2, i3, i4)
    # cursor.execute(sql)
    # db.commit()

'''
解析页面
'''
def get_useragent(htmldata):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(htmldata,'html.parser')
    link = soup.findAll('tr')
    i = 0
    mobile_phone = []
    phone_type = []
    app = []
    useragent = []
    data = {}
    for idx, tr in enumerate(link):   #返回表格的行数和所有的tr包含的内容
        if idx != 0:
            tds = tr.findAll('td')    #返回所有td所包含的内容
            mobile_phone.append(tds[0].string)
            phone_type.append(tds[1].string)
            app.append(tds[2].string)
            useragent.append(tds[3].string)
            save_uerAgent_mysql(tds[0].string, tds[1].string, tds[2].string, tds[3].string)
            # print(tds[0].string, tds[1].string, tds[2].string, tds[3].string)


'''
调度流程
'''
def run(url):
    data = download_homl(url)
    get_useragent(data)


if __name__ == '__main__':
    i = 0
    while i < 5:
        i = i+1
        url = 'http://www.fynas.com/ua/search?d=&b=&k=&page=%s'%i
        print(url)
        run(url)