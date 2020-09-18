# encoding=utf8
import sys
import importlib

importlib.reload(sys)
import urllib.request
from bs4 import BeautifulSoup


def download_html(url):
    try:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
        _request = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(_request)
        data = response.read()
    except Exception as e:
        return None
    # print(data)
    return data

def get_content(data):
    if data is not None:
        soup = BeautifulSoup(data, 'html.parser')
        link = soup.findAll('div')
        for div in link:
            if div.get('class') == ['f-list-item', 'ershoufang-list']:
                dls = div.findAll('dl')
                for dl in dls:
                    dds = dl.findAll('dd')
                    for dd in dds:
                        if dd.get('class') == ['dd-item', 'title']:
                            a = dd.findAll('a')
                            for i in a:
                                href = i.get('href')
                                if href.startswith("//"):
                                    href = "https:" + href
                                if '58' in href:
                                    continue
                                # print(href)
                                data = download_html(href)
                                get_useragent(href, data)

def get_useragent(href,data):
    if data is not None:
        soup = BeautifulSoup(data, 'html.parser')
        divs = soup.findAll('div')
        phone = ""
        region = ""
        # print(divs)
        for div in divs:
            if div.get('class') == ['phone']:
                las = div.findAll('a')
                # print(las)
                for i in las:
                    phone = i.get_text()
            if div.get('class') == ['card-info', 'f-fr']:
                uls = div.findAll('ul')
                for ul in uls:
                    las = ul.findAll('a')
                    for la in las:
                        re = la.findAll('span')
                        for r in re:
                            region = r.get_text()

        line = href + "|" + region + "|" + phone + "\n"
        print(href)
        print(region)
        print(phone)
        file_write.writelines(line)





def run(url):
    # data = download_html("https://baoding.ganji.com/ershoufang/37498253813914x.shtml")
    data = download_html(url)
    get_content(data)
    # get_useragent(url, data)



if __name__ == '__main__':
    file_write = open('result_gaji','w',encoding='utf8')
    url = 'http://baoding.ganji.com/daodingzhuozhou/ershoufang/pn'
    for i in range(1,71):
        url_use = url + str(i)
        print(url_use)
        run(url_use)
    # url_use = url
    # run(url_use)
    file_write.close()
