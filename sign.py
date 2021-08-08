# -*- coding: utf8 -*-
from requests import session
from hashlib import md5
from random import random
from time import sleep

class Tieba():
    def __init__(self, BDUSS, STOKEN):
        self.BDUSS = BDUSS
        self.STOKEN = STOKEN
        self.count = [0, 0, 0] # 签到成功, 已经签到, 总
        self.session = session()
        self.session.headers.update(
            {'Accept': 'text/html, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'tieba.baidu.com',
            'Referer': 'http://tieba.baidu.com/i/i/forum',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/71.0.3578.98 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'}
        )
    def set_cookie(self):
        self.session.cookies.update({'BDUSS': self.BDUSS, 'STOKEN': self.STOKEN})
    def fetch_tbs(self):
        r = self.session.get('http://tieba.baidu.com/dc/common/tbs').json()
        if r['is_login'] == 1: self.tbs = r['tbs']
        else: raise Exception('获取tbs错误！以下为返回数据：' + str(r))
    def fetch_likes(self):
        self.rest = set()
        self.already = set()
        r = self.session.get('https://tieba.baidu.com/mo/q/newmoindex?').json()
        if r['no'] == 0:
            for forum in r['data']['like_forum']:
                self.count[2] += 1
                if forum['is_sign'] == 1:
                    self.already.add(forum['forum_name'])
                else:
                    self.rest.add(forum['forum_name'])
        else: raise Exception('获取关注贴吧错误！以下为返回数据：' + str(r))
    def sign(self, forum_name):
        data = {
            'kw': forum_name,
            'tbs': self.tbs,
            'sign': md5(f'kw={forum_name}tbs={self.tbs}tiebaclient!!!'.encode('utf8')).hexdigest()
        }
        r = self.session.post('http://c.tieba.baidu.com/c/c/forum/sign', data).json()
        if r['error_code'] == '160002':
            print(f'"{forum_name}"已签到！')
            self.count[1] += 1
            return True
        elif r['error_code'] == '0':
            print(f'"{forum_name}"签到成功，您是第{r["user_info"]["user_sign_rank"]}个签到的用户！') # Modify!
            self.count[0] += 1
            return True
        else:
            print(f'"{forum_name}"签到失败！以下为返回数据：{str(r)}')
            return False
    def loop(self, n):
        print(f'* 开始第{n}轮签到 *')
        rest = set()
        self.fetch_tbs()
        for forum_name in self.rest:
            sleep(random() * 3)
            flag = self.sign(forum_name)
            if not flag: rest.add(forum_name)
        self.rest = rest
    def main(self, max):
        self.set_cookie()
        self.fetch_likes()
        n = 0
        if self.already:
            print('* 已经签到的贴吧 *')
            for forum_name in self.already:
                print(f'"{forum_name}"已签到！')
                self.count[1] += 1
        while n < max and self.rest:
            n += 1
            self.loop(n)
        print('* 本日签到报告 *')
        print(f'共{self.count[2]}个贴吧，其中签到成功{self.count[0]}个，已经签到{self.count[1]}个，签到失败{len(self.rest)}个。')
        if self.rest:
            print('* 签到失败列表 *')
            for forum_name in self.rest:
                print(f'"{forum_name}"签到失败！')

def main_handler(*args):
    with open('BDUSS.txt') as f: BDUSS = f.read()
    with open('STOKEN.txt') as f: STOKEN = f.read()
    task = Tieba(BDUSS, STOKEN)
    task.main(3)
