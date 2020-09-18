# encoding=utf8

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
        das = soup.findAll('a')
        for da in das:
            if da.get('class') == ['color000']:
                href = 'http://www.zhuozhoufangchan.com'+da.get('href') + "\n"
                print(href)
                file_w.writelines(href)



def run(url):
    data = download_html(url)
    get_content(data)

if __name__ == '__main__':
    file_w = open('result_2','w',encoding='utf-8')
    url = 'http://www.zhuozhoufangchan.com/shop/sale.php?id=96162&pageno='
    for i in range(1,7):
        url_res = url + str(i)
        print(url_res)
        print()
        run(url_res)
    file_w.close()
