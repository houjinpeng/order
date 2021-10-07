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





def build_email():
    email = ''
    for i in range(10):
        email += str(random.randint(1, 10))
    return email[:10] + '@qq.com'


def list_of_groups(init_list, children_list_len):
    url_list = []
    url_l = []
    for url in init_list:
        if len(url_l) == 20:
            url_list.append(copy.copy(url_l))
            url_l = []
        url_l.append(url)
    url_list.append(copy.copy(url_l))
    return url_list
    # list_of_groups = zip(*(iter(init_list),) * children_list_len)
    # end_list = [list(i) for i in list_of_groups]
    # count = len(init_list) % children_list_len
    # end_list.append(init_list[-count:]) if count != 0 else end_list
    # return end_list


class SouGou():
    def __init__(self, q):
        self.q = q
        self.i = 0
        with open('./taskdata/liyou.txt', 'r', encoding='UTF-8') as f:
            self.reason = f.readlines()

        self.postUrl = 'http://zhanzhang.sogou.com/api/feedback/addMultiShensu'
        self.linkUrl = 'http://zhanzhang.sogou.com/index.php/sitelink/index'
        self.indexUrl = 'http://zhanzhang.sogou.com/'
        self.verifUrl = 'http://zhanzhang.sogou.com/api/user/generateVerifCode?timer=1619079025251'
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
            for u in url:
                fw.write(u+'\n')

    def index(self, num,cookie):
        while not self.q.empty():
            url = self.q.get()
            # 先去请求页面
            sgid_sig = cookie['sgid.sig']
            sgid = cookie['sgid']
            username = cookie['username']
            SUID = cookie['SUID']
            SNUID = cookie['SNUID']
            ZHANZHANG_SID_sig = cookie['__ZHANZHANG_SID__.sig']
            ZHANZHANG_SID = cookie['__ZHANZHANG_SID__']

            email = build_email()
            if len(url) == 1:
                urls = url[0].strip()
            else:
                for u in url:
                    urls = u+'↵'
            if urls[-1] == '↵':
                urls = urls[:-1]

            code = cookie['code']
            reason = random.choice(self.reason).strip()
            ul = []
            for u in url:
                ul.append(u.strip())
            sites = ul
            data = {
                'site_type': task,
                'email': email,
                'urls': urls,
                'reason': reason,
                'code': code,
                'sites': sites
            }

            headers = {
                'Accept': "application/json, text/plain, */*",
                'Accept-Encoding': "gzip, deflate",
                'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                'Connection': "keep-alive",
                'Content-Type': "application/json;charset=UTF-8",
                'Cookie': 'SNUID=%s; IPLOC=CN; SUID=%s;__ZHANZHANG_SID__=%s;__ZHANZHANG_SID__.sig=%s; sgid=%s; sgid.sig=%s; username=%s'% (SNUID,SUID,ZHANZHANG_SID,ZHANZHANG_SID_sig, sgid_sig, sgid, username),
                'Host': "zhanzhang.sogou.com",
                'User-Agent': cookie['ua'],
            }

            try:
                r = requests.post(self.postUrl, headers=headers, json=data,timeout=3)
            except Exception as e:
                self.q.put(sites)
                continue
            try:
                resp = json.loads(r.text)
            except Exception as e:
                resp = {'msg':e}
            # print(f'线程{num}正在请求成功 {resp}')

            if resp['msg'] == 'success':
                print('%s  %s 推送成功 %s' %(num,url ,resp))
                self.saveSucceed(sites)
                print('==' * 20)
            elif resp['msg'] == '验证码有误':
                print(f'验证码有误 请登录后自己更新{cookie}')
                # verif_resp = requests.get(self.verifUrl, headers=headers)
                # 保存验证码
                # self.saveVerifCode(verif_resp, num)
                # self.index(num)
                self.q.put(sites)
                break
            elif resp['msg'] == 'anti校验失败':
                print(f'线程{num}检验失败  当前账号不能提交数据1分钟后重试 ')
                self.q.put(sites)
                time.sleep(60*1)
            else:
                print(resp)

        print(f'============={num}任务结束=============')


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

    # 去掉投诉过的
    for row in rows:
        if row in urls:
            try:
                urls.remove(row)
            except Exception as e:
                print(e)

    doUrlAll = list_of_groups(urls, 20)

    for url in doUrlAll:
        q.put(url)


    def run():
        t = []
        for i,cookie in enumerate(Cookies):
            t.append(threading.Thread(target=SouGou(q).index, args=(i,eval(cookie))))
        for j in t:
            j.start()


    run()
