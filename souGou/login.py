# @Time : 2021/4/22 16:13
# @Author : HH
# @File : complain.py
# @Software: PyCharm
# @explain: 模拟登录
import configparser

import os
import requests
import threading, queue
import cairosvg
import json
from fake_useragent import UserAgent
from verif_code import verif_api, reportError

import random

'''读写配置文件'''
config = configparser.ConfigParser()
# 文件路径
logFile = r"./conf/setting.cfg"
config.read(logFile, encoding="utf-8")
config = config.defaults()
task = config.get('task')


def build_email():
    email = ''
    for i in range(10):
        email += str(random.randint(1, 10))
    return email[:11] + '@qq.com'


def list_of_groups(init_list, children_list_len):
    list_of_groups = zip(*(iter(init_list),) * children_list_len)
    end_list = [list(i) for i in list_of_groups]
    count = len(init_list) % children_list_len
    end_list.append(init_list[-count:]) if count != 0 else end_list
    return end_list


class SouGou():
    def __init__(self, q):
        self.q = q
        self.ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        self.indexUrl = 'https://zhanzhang.sogou.com/'
        self.verifUrl = 'https://zhanzhang.sogou.com/api/user/generateVerifCode?timer=1635384258573'
        self.loginUrl = 'https://zhanzhang.sogou.com/api/user/login'
        self.headersIndex = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            'Cache-Control': "max-age=0",
            'Connection': "keep-alive",
            # 'Cookie': "GOTO=Af22712-0052; IPLOC=CN2301; SUID=B4360071C830A40A0000000060711B6B; QIDIANID=xT9viG080sSqjmMvSx4cAb86OgHEfnXlwpKjFaTk5DK8/o9XJtWUc8cphn4Bq1CT3x9QftK8kaOjNSeCdrvjUA==; usid=xHL1mR8zRMMm5x1b; SUV=0073FE91710036B460711B6B7E506293; ld=5Zllllllll2kNlmAlllllpx1jfwllllltyy4gZllll9lllllRllll5@@@@@@@@@@; LSTMV=202%2C195; LCLKINT=1418; SNUID=3B7650205155900F2394DDD05186D9B8; BAIDU_SSP_lcr=http://sgcs.edge.ker58.com/; __ZHANZHANG_SID__=X_MB-y9ka956XITA7sZGzj567hd88Df0; __ZHANZHANG_SID__.sig=9-V1pZLcwYeqa--fBDac_qhFZog",
            'Host': "zhanzhang.sogou.com",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent': self.ua,
        }
        self.headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            'Cache-Control': "max-age=0",
            'Connection': "keep-alive",
            'Host': "zhanzhang.sogou.com",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent': self.ua,
        }
        self.code_header = {
            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'zhanzhang.sogou.com',
            'Referer': 'https://zhanzhang.sogou.com/index.php/site/index',
            'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'image',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        }

        self.headersLogin = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '57',
            'Content-Type': 'application/json;charset=UTF-8',
            'Host': 'zhanzhang.sogou.com',
            'Origin': 'https://zhanzhang.sogou.com',
            'Referer': 'https://zhanzhang.sogou.com/index.php/site/index',
            'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
        }

    def requestHandler(self, url, headers, num, method='get', data=None):
        if method == 'get':
            try:
                r = self.s.get(url, headers=headers)
                # print('请求完毕')
                return r
            except Exception as e:
                print(e)
        else:
            r = self.s.post(url, headers=headers, json=data)
            print(f'线程{num}正在登录')
            print(r.text)
            if 'svg' in r.text:
                self.saveVerifCode(r, num)
                return self.requestHandler(url, headers, num, method='post', data=data)
            return r

    def saveVerifCode(self, resp, i):
        with open('./verif/verifCode_%s.svg' % i, 'wb') as fw:
            fw.write(resp.content)
        svg_path = './verif/verifCode_%s.svg' % i
        png_path = './verif/verifCode_%s.png' % i
        cairosvg.svg2png(url=svg_path, write_to=png_path)
        os.remove(svg_path)

    def saveCookie(self, resp, code, user, pwd):
        print(resp)
        cookieDict = {}
        cookies = self.s.cookies._cookies['.sogou.com']['/']
        verifCookie = resp.cookies._cookies['zhanzhang.sogou.com']['/']
        Cookie = resp.cookies._cookies['.zhanzhang.sogou.com']['/']
        cookieDict['sgid'] = Cookie['sgid'].value
        cookieDict['sgid.sig'] = Cookie['sgid.sig'].value
        cookieDict['sgid.sig'] = Cookie['sgid.sig'].value
        cookieDict['SUID'] = cookies['SUID'].value
        cookieDict['SNUID'] = cookies['SNUID'].value
        cookieDict['__ZHANZHANG_SID__'] = verifCookie['__ZHANZHANG_SID__'].value
        cookieDict['__ZHANZHANG_SID__.sig'] = verifCookie['__ZHANZHANG_SID__.sig'].value
        cookieDict['username'] = json.loads(resp.text)['data']['username']
        cookieDict['username.sig'] = Cookie['username.sig'].value
        cookieDict['user'] = user
        cookieDict['user_id'] = Cookie['user_id'].value
        cookieDict['user_id.sig'] = Cookie['user_id.sig'].value
        cookieDict['pwd'] = pwd
        cookieDict['code'] = code
        cookieDict['ua'] = self.ua

        with open('./userPool/cookiePool.txt', 'a', encoding='utf-8') as fw:
            fw.write(str(cookieDict) + '\n')
        print('cookie保存完毕')

    def login(self, num):
        global cookieList
        while not self.q.empty():
            self.s = requests.session()
            user = self.q.get()
            if user[0] in cookieList:
                print(f'{user[0]} 已登录')
                continue
            self.requestHandler(self.indexUrl, self.headersIndex, num)
            # 请求验证码
            r = self.requestHandler(self.verifUrl, self.code_header, num)
            # 保存验证码
            self.saveVerifCode(r, num)
            # 登录
            img_path = './verif/verifCode_%s.png' % num
            code, verif_id = verif_api(uname='15211731111', pwd='esb104', img=img_path, typeid=3)
            # code = input(f'请输入验证码 verifCode_{num} :')
            data = {
                'code': code,
                'pwd': user[1],
                'userid': user[0],
            }
            resp = self.requestHandler(self.loginUrl, self.headersLogin, num, method='post', data=data)
            # 判断是否成功  成功保存cookie
            d = json.loads(resp.text)
            if d['msg'] == 'success':
                print(f'{user[0]} {user[1]}登录成功')
                self.saveCookie(resp, code, user[0], user[1])
                os.remove(img_path)
                print('==' * 20)
            # r如果验证码错误 重新登录
            elif d['msg'] == '验证码有误':
                print('验证码错误重新输入')
                reportError(verif_id)
                self.q.put(user)
            elif d['msg'] == '用户名或密码错误':
                print(f'{user[0]} {user[1]} 有误 请查看是否准确')
            else:
                print(d)


if __name__ == '__main__':
    q = queue.Queue()

    with open('./taskdata/搜狗站长账号 .txt', 'r', encoding='utf-8') as fr:
        usertxt = fr.readlines()
    for u in usertxt:
        q.put(u.strip().split('----')) if len(u.strip().split('----')) > 1 else 1
    with open('./userPool/cookiePool.txt', 'r', encoding='utf-8') as fr:
        Cookies = fr.readlines()

    cookieList = []
    for c in Cookies:
        cookieList.append(eval(c)['user'])


    def run():
        t = []
        for i in range(10):
            t.append(threading.Thread(target=SouGou(q).login, args=(i,)))
        for j in t:
            j.start()
    run()
