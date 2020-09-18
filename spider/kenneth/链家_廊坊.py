# encoding=utf8
import sys
import importlib

importlib.reload(sys)
import urllib.request
from bs4 import BeautifulSoup



def download_html(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
        _request = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(_request)
        data = response.read()
    except Exception as e:
        return None
    return data

def get_content(data):
    if data is not None:
        soup = BeautifulSoup(data, 'html.parser')
        divs = soup.findAll('div')
        for div in divs:
            if div.get('class') == ['title']:
                das = div.findAll('a')
                for a in das:
                    hurl = a.get('href')
                    if 'http' in hurl:
                        print(hurl)
                        data = download_html(hurl)
                        get_useragent(hurl, data)

def get_useragent(hurl, data):
    region = ''
    telno = ''
    if data is not None:
        soup = BeautifulSoup(data, 'html.parser')
        divs = soup.findAll('div')
        for div in divs:
            if div.get('class') == ['areaName']:
                das = div.findAll('a')
                for a in das:
                    region += a.get_text() + " "
                # print(region)
            if div.get('class') == ['phone']:
                for i in div:
                    if i.string is not None and '400' in i.string:
                        telno = i.string
        line = hurl +"|"+ region +"|"+ telno + "\n"
        file_w.writelines(line)


def run(url):
    data = download_html(url)
    get_content(data)

if __name__ == '__main__':
    file_w = open('result_lianjia2','w',encoding='utf8')
    url = 'https://lf.lianjia.com/ershoufang/pg'
    for i in range(78,101):
        url_res = url + str(i)
        print(url_res)
        print()
        run(url_res)
    file_w.close()