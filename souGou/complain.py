# @Time : 2021/4/22 16:13 
# @Author : HH
# @File : complain.py
# @Software: PyCharm
# @explain: 模拟登录
import configparser
import requests
import cairosvg
import json
import copy
import random
import threading, queue

import time
import os
'''读写配置文件'''
config = configparser.ConfigParser()
# 文件路径
logFile = r"./conf/setting.cfg"
config.read(logFile, encoding="utf-8")
config = config.defaults()
task = config.get('task')
ipQ = queue.Queue()
q = queue.Queue()

class SouGou():
    def __init__(self, q):
        self.q = q
        self.i = 0
        self.postUrl = 'https://zhanzhang.sogou.com/api/feedback/addMultiShensu'
        self.linkUrl = 'https://zhanzhang.sogou.com/index.php/sitelink/index'
        self.indexUrl = 'https://zhanzhang.sogou.com/'
        self.verifUrl = 'https://zhanzhang.sogou.com/api/user/generateVerifCode?timer=1619079025251'
        self.s = requests.session()

    def saveVerifCode(self, resp, i):
        with open('./verif/verifCode_%s.svg' % i, 'wb') as fw:
            fw.write(resp.content)
        svg_path = './verif/verifCode_%s.svg' % i
        png_path = './verif/verifCode_%s.png' % i
        cairosvg.svg2png(url=svg_path, write_to=png_path)
        os.remove(svg_path)

    def saveSucceed(self, url):
        with open('./taskdata/urls_out.txt', 'a', encoding='utf-8') as fw:
            fw.write(url)

    def index(self, num,cookie):
        sgid_sig = cookie['sgid.sig']
        sgid = cookie['sgid']
        username = cookie['username']
        username_sig = cookie['username.sig']
        SUID = cookie['SUID']
        SNUID = cookie['SNUID']
        ZHANZHANG_SID_sig = cookie['__ZHANZHANG_SID__.sig']
        ZHANZHANG_SID = cookie['__ZHANZHANG_SID__']
        user_id_sig = cookie['user_id.sig']
        user_id = cookie['user_id']

        code = cookie['code']
        while not self.q.empty():
            url = self.q.get()
            # 先去请求页面
            data = {
                'site_address': "www.reLayserve.com",
                'site_id':'44692839',
                'url': url.strip(),
                'urlSubFlag': False,
                'code': code,
                'urls': []
            }
            headers = {

                'cookie':f'IPLOC=CN2301; SUID={SUID}; __ZHANZHANG_SID__={ZHANZHANG_SID}; __ZHANZHANG_SID__.sig={ZHANZHANG_SID_sig}; sgid={sgid}; sgid.sig={sgid_sig}; username={username}; username.sig={username_sig}; user_id={user_id}; user_id.sig={user_id_sig}; SNUID={SNUID}; show_wxapp=0',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Content-Length': '144',
                'Content-Type': 'application/json;charset=UTF-8',
                'Host': 'zhanzhang.sogou.com',
                'Origin': 'https://zhanzhang.sogou.com',
                'Referer': 'https://zhanzhang.sogou.com/index.php/sitelink/index',
                'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
            }

            try:
                r = requests.post(self.postUrl, headers=headers, json=data,timeout=3)
            except Exception as e:
                self.q.put(url)
                continue
            try:
                resp = json.loads(r.text)
            except Exception as e:
                resp = {'msg':e}
            # print(f'线程{num}正在请求成功 {resp}')

            if resp['msg'] == 'success':
                print('线程：%s  推送url:%s  返回结果:%s' %(num,url.strip() ,resp))
                self.saveSucceed(url)
            elif resp['msg'] == '验证码有误':
                print(f'验证码有误 请登录后自己更新{cookie}')
                self.q.put(url)
                break
            else:
                print(resp)
            try:
                count_url = 'https://zhanzhang.sogou.com/api/feedback/getUrlShouluCountNotVerify'
                r = requests.post(count_url, headers=headers, json={}, timeout=3)
                resp = json.loads(r.text)
                if resp['data'] >= 200:
                    print(f'剩余任务：{self.q.qsize()}  线程:{num} 账号:{username} 提交数量 {resp["data"]} 停止继续提交')
                    break
            except Exception as e:
                pass
        print(f'=============线程：{num}任务结束=============')


if __name__ == '__main__':
    # 初始化cookie池
    with open('./userPool/cookiePool.txt', 'r', encoding='utf-8') as fr:
        Cookies = fr.readlines()
    # 处理完成的
    with open("./taskdata/urls_out.txt", "r", encoding="UTF-8") as f:
        rows = f.readlines()

    # 初始化url任务
    with open('./taskdata/推送.txt', 'r', encoding='utf-8') as fr:
        urls = fr.readlines()

    doUrlAll = set(urls).difference(set(rows))

    for url in doUrlAll:
        q.put(url)

    def run():
        t = []
        for i,cookie in enumerate(Cookies):
            t.append(threading.Thread(target=SouGou(q).index, args=(i,eval(cookie))))
        for j in t:
            j.start()
    run()
