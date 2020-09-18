# encoding:utf-8
import urllib
from bs4 import BeautifulSoup
import pymysql

def download_html(url):
    response = urllib.request.Request(url)
    html = urllib.request.urlopen(url).read()
    # html = html.decode()
    return html

def get_uer_agent_BeautifulSoup(html):
    soup = BeautifulSoup(html,'html.parser')
    mobile_phone = []
    phone_type = []
    app = []
    usr_agent = []
    data = {}
    i = 0
    links = soup.find_all('tr')
    for idx,tr in enumerate(links):
        tds = tr.find_all('td')
        #content返回的是bytes类型的  get_text返回的是unicode类型的
        if idx != 0:
            tds = tr.find_all('td')
            mobile_phone.append(tds[0].get_text())
            phone_type.append(tds[1].get_text())
            app.append(tds[2].get_text())
            usr_agent.append(tds[3].get_text())
            save_user_mysql(tds[0].get_text(),tds[1].get_text(),tds[2].get_text(),tds[3].get_text())

def save_user_mysql(mobile,phone_type,app,user_agent):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='test', charset='utf8')
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO mobile(mobile,phone_type,app,user_agent) VALUES ('%s', '%s', '%s', '%s' )" % (mobile, phone_type,app,user_agent)
        cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()


def run(url):
    data = download_html(url)
    get_uer_agent_BeautifulSoup(data)

if __name__ == '__main__':
    i = 0
    while i < 888:
        i = i+1
        url = 'http://www.fynas.com/ua/search?d=&b=&k=&page=%s' % (i)
        print(url)
        run(url)