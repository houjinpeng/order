# @Time : 2021/5/15 16:18
# @Author : HH
# @File : longin.py
# @Software: PyCharm
# @explain:
import hashlib
import os
import time
import re
from verif_code import verif_api, reportError
import requests
import json



class Login():
    def __init__(self):
        self.code_url = 'http://www.juming.com/xcode.htm?0.43599163831308596'
        self.login_url = 'http://www.juming.com/if.htm'
        self.tiao_url = 'http://www.juming.com/waibu/new.htm'
        self.s = requests.session()
        self.headers = {
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Content-Length': "67",
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",


            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
            'X-Requested-With': "XMLHttpRequest",
        }
        self.headers1 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
            'Upgrade-Insecure-Requests':'1',
            'Host': 'www.juming.com',
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        }


    def get_code(self,file_path):
        r = self.s.get(self.code_url,headers=self.headers1)
        with open(file_path,'wb') as fw:
            fw.write(r.content)
        print('验证码下载完毕')

    def login(self,username,password):

        m = hashlib.md5()
        m1 = hashlib.md5()
        m.update(f'[jiami{password}mima]'.encode())
        m1.update(('SF3mg34s9Vs'+m.hexdigest()[0:19]).encode())
        password_md5 = m1.hexdigest()[0:19]

        # data_raw = f're_mm={password_md5}&re_yx={username}&re_yzm='
        data = f'tj_fs=1&re_yx={username}&re_code=SF3mg34s9Vs&re_mm={password_md5}'
        # data = data_raw + result[0]
        r = self.s.post(self.login_url,data=data,headers=self.headers)


        if '登陆成功' in r.text:
            print('登录成功 获取cookie中')
            r2 = self.s.get(self.tiao_url, headers=self.headers1)
            t_url = re.findall("location.href=\\'(.*)\\'", r2.text)[0]
            r3 = self.s.get(t_url, headers=self.headers1)
            cookie = r3.history[0].cookies._cookies['www.juming.com']['/']['PHPSESSID'].value
            cookie = 'PHPSESSID=' + cookie

            return self.s,r.text,cookie
        elif '抱歉，登录次数太多，请输入验' in r.text:
            # 获取验证
            img_path = './code.jpg'
            self.get_code(img_path)
            result = verif_api(uname='15211731111', pwd='esb104', img=img_path, typeid=3)
            data = f'tj_fs=1&re_yx={username}&re_code=SF3mg34s9Vs&re_mm={password_md5}&re_yzm={result[0]}'
            r = self.s.post(self.login_url, data=data, headers=self.headers)
            if '登陆成功' in r.text:
                print('登录成功 获取cookie中')
                r2 = self.s.get(self.tiao_url, headers=self.headers1)
                t_url = re.findall("location.href=\\'(.*)\\'", r2.text)[0]
                r3 = self.s.get(t_url, headers=self.headers1)
                cookie = r3.history[0].cookies._cookies['www.juming.com']['/']['PHPSESSID'].value
                cookie = 'PHPSESSID='+cookie
                return self.s, r.text, cookie
            elif '验证码不正确' in r.text:
                reportError(result[1])
                return self.login(username, password)
        else:
            print(r.text)
            time.sleep(1)
            return self.login(username,password)

if __name__ == '__main__':
    Login().login('104038','qq123123')