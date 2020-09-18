import random
import time
import requests
from bs4 import BeautifulSoup

# class FaxinSpider(object):
#     def __init__(self,):
#
# if __name__ == '__main__':
#     url = 'http://www.faxin.cn/keyword/index.aspx'



url = 'http://www.faxin.cn/keyword/index.aspx'
response = requests.get(url)
data = response.text
# print(data)
soup = BeautifulSoup(data, 'html.parser')
link = soup.findAll('li')
print(link)
