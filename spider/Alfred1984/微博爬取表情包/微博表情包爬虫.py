import os
import time
import requests

class CommentPhotoCrawler(object):
    '''
    微博评论图片爬取
    '''
    def __init__(self, sleep_time = 2):
        '''
        初始化函数：
            :param sleep_time: int, 默认为2, 爬取评论数据及图片的间隔时间
            :attr mid: string, 初始化为None, 由get_m_url方法爬取
            :attr login_headers: dict, 模拟登录请求头
            :attr session: requests Session
            :param sleep_time:
        '''
        self.sleep_time = sleep_time
        self.mid = '4333036507864049'
        self.login_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 '
                          '(KHTML, like Gecko)Chrome/48.0.2564.116 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Origin': 'https://passport.weibo.cn',
            'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&r'
                       '=https%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt='
        }
        self.session = None
    def get_m_url(self, url):
        '''
        爬取电脑端微博url对应的手机端微博id，从而拼接出手机端微博的url
        :param url:所需爬取的电脑端微博url，结构为：https://weibo.com/博主的id/9位数字+字母
        :return:
        '''
        with open('cookies.txt', 'r') as f:
            cookie = f.read()
        headers = {'Cookie': cookie}
        res = requests.get(url, headers = headers)
        idx = res.text.find('mblog&act=')  #手机网页端id就在网页源代码的"mblog&act="字符串后面16位,这里find返回的是坐标
        self.mid = res.text[idx+10, idx+26]
        print(f'手机对应的ID是{self.mid}')

    def login(self, user, password):
        '''
        模拟手机登录微博,需要记录下来session， 当不需要登录的时候，直接使用post或者get请求即可
        :param user:用户名
        :param password:密码
        :return:
        '''
        self.session = requests.session()
        login_data = {
            'username':user,
            'password':password,
            'savestate': '1',
            'r': 'https://weibo.cn/',
            'ec': '0',
            'pagerefer': 'https://passport.weibo.cn/signin/welcome?entry='
                         'mweibo&r=https%3A%2F%2Fm.weibo.cn%2Fdetail%2F4333036507864049',
            'entry': 'mweibo',
            'mainpageflag': '1'
        }
        login_url = 'https://passport.weibo.cn/sso/login'
        self.session.post(login_url, headers = self.login_headers, data= login_data)
        print('模拟登录成功')

    def get_comments(self, max_page):
        '''
        爬取评论数据
        :param max_page: int or 'all'， 传入数字代表爬取的页数， 传入all时，代表全部爬取
        :return:
        '''
        if isinstance(max_page, int):
            # 第一页url不一样，需要单独处理
            url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0'.format(self.mid, self.mid)
            response = self.session.get(url, headers = self.login_headers)
            max_id = response.json()['data']['max_id']
            max_id_type = response.json()['data']['max_id_type']
            self._store_pic_url(response)
            print('成功抓去第一页的图片链接')

            if max_page > 1:
                for page in range(1, max_page):
                    url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}' \
                          '&max_id_type={}'.format(self.mid, self.mid, max_id, max_id_type)
                    response = self.session.get(url, headers=self.login_headers)
                    max_id = response.json()['data']['max_id']
                    max_id_type = response.json()['data']['max_id_type']
                    self._store_pic_url(response)
                    print('成功抓取第{}页的图片链接！'.format(page + 1))
                    time.sleep(self.sleep_time)  # 隔两秒再爬下一页

    @staticmethod
    def _store_pic_url(response):
        """
                解析响应的JSON数据里面的图片url，并把图片url保存在photourl.txt里
                :param response: 响应的评论数据
                :return: None
                """
        for comment in response.json()['data']['data']:
            if 'pic' in comment.keys():  #检查评论是否含有图片
                with open('photourl.txt', 'a') as f:
                    f.write(comment['pic']['large']['url'] + '\n')

    def down_photo(self, output='.'):
        """
                从photourl.txt提取图片url，并下载图片到指定文件夹photos
                :param output: string, 保存photos文件夹的路径, 默认为当前工作路径
                :return: None
                """
        os.mkdir(output + '/photos')
        with open('photourl.txt', 'r') as f:
            photo_utls = [url.strip() for url in f.readlines()]
        for url in photo_utls:
            res = requests.get(url)
            name = url.split('/')[-1]
            with open(output + '/photos/' + name, 'wb') as pic:
                pic.write(res.content)
                print(f'图片{name}保存成功')
                time.sleep(self.sleep_time)

if __name__ == '__main__':
    crawler = CommentPhotoCrawler()
    crawler.login('17778049587', 'guo930315@')
    crawler.get_comments(max_page=3)
    crawler.down_photo()

