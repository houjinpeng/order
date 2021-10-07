# @Time : 2021/4/22 16:13 
# @Author : HH
# @File : complain.py
# @Software: PyCharm
# @explain: 模拟登录
import configparser
import requests
import cairosvg
import json
import random
import threading, queue
from fake_useragent import UserAgent
from verif_code import Chaojiying_Client
import os
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
    end_list.append(init_list[-count:].strip()) if count != 0 else end_list
    return end_list


class SouGou():
    def __init__(self, q):
        self.ua = UserAgent().chrome
        self.q = q


        with open('./taskdata/liyou.txt', 'r', encoding='UTF-8') as f:
            self.reason = f.readlines()

        self.postUrl = 'http://zhanzhang.sogou.com/api/feedback/addMultiShensu'
        self.linkUrl = 'http://zhanzhang.sogou.com/index.php/sitelink/index'
        self.indexUrl = 'http://zhanzhang.sogou.com/'
        self.verifUrl = 'http://zhanzhang.sogou.com/api/user/generateVerifCode?timer=1619079025251'
        self.headersIndex = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            'Cache-Control': "max-age=0",
            'Connection': "keep-alive",
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

        self.headersLogin = {
            'Accept': "application/json, text/plain, */*",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Content-Length': "145",
            'Content-Type': "application/json;charset=UTF-8",
            'Host': "zhanzhang.sogou.com",
            'Origin': "http://zhanzhang.sogou.com",
            'Referer': "http://zhanzhang.sogou.com/index.php/sitelink/index",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        }
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
                fw.write(u)

    def index(self, num,cookie):
        while not self.q.empty():
            url = self.q.get()
            # 先去请求页面
            # sgid_sig = cookie['sgid.sig']
            # sgid = cookie['sgid']
            # username = cookie['username']
            ZHANZHANG_SID_sig = cookie['__ZHANZHANG_SID__.sig']
            ZHANZHANG_SID = cookie['__ZHANZHANG_SID__']
            # 请求验证码
            # headers = {
            #     'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            #     'Accept-Encoding': "gzip, deflate",
            #     'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            #     'Cache-Control': "max-age=0",
            #     'Connection': "keep-alive",
            #     'Cookie': '__ZHANZHANG_SID__=%s; __ZHANZHANG_SID__.sig=%s; sgid=%s; sgid.sig=%s; username=%s' % (ZHANZHANG_SID,ZHANZHANG_SID_sig,
            #     sgid_sig, sgid, username),
            #     'Host': "zhanzhang.sogou.com",
            #     'Upgrade-Insecure-Requests': "1",
            #     'User-Agent': cookie['ua']
            # }
            # print(num,username,ZHANZHANG_SID_sig,ZHANZHANG_SID,sgid_sig,sgid)
            # s = requests.session()
            # r1 = s.get(self.linkUrl, headers=headers)
            # verif_resp = s.get(self.verifUrl, headers=headers)
            # # 保存验证码
            # self.saveVerifCode(verif_resp, num)
            email = build_email()
            if len(url) == 1:
                urls = url[0].strip()
            else:
                for u in url:
                    urls = u+'↵'
            if urls[-1] == '↵':
                urls = urls[:-1]
            # urls = str('↵'.join(url).strip()),
            # im = open('./verif/verifCode_%s.png'%num, 'rb').read()
            # chaojiying = Chaojiying_Client('672477135', 'qq13111110508', '1004')
            # code = chaojiying.PostPic(im, 1004)['pic_str']  # 超级硬代码
            code = cookie['code']
            # code = input('请输入验证:')
            reason = random.choice(self.reason).strip()
            ul = []
            for u in url:
                ul.append(u.strip())
            sites = ul
            # data = {
            #     'site_type': task,
            #     'email': email,
            #     'urls': urls,
            #     'reason': reason,
            #     'code': code,
            #     'sites': sites
            # }
            # headers = {
            #     'Accept': "application/json, text/plain, */*",
            #     'Accept-Encoding': "gzip, deflate",
            #     'Accept-Language': "zh-CN,zh;q=0.9",
            #     'Connection': "keep-alive",
            #     # 'Content-Length': str(len(str(data))),
            #     'Content-Type': "application/json;charset=UTF-8",
            #     # 'Cookie': '__ZHANZHANG_SID__=%s;__ZHANZHANG_SID__.sig=%s; sgid=%s; sgid.sig=%s; username=%s'% (ZHANZHANG_SID,ZHANZHANG_SID_sig, sgid_sig, sgid, username),
            #     # 'Cookie': '__ZHANZHANG_SID__=%s;__ZHANZHANG_SID__.sig=%s;'% (ZHANZHANG_SID,ZHANZHANG_SID_sig),
            #     'Cookie': '__ZHANZHANG_SID__=%s;__ZHANZHANG_SID__.sig=%s;'% (ZHANZHANG_SID,ZHANZHANG_SID_sig),
            #     'Host': "zhanzhang.sogou.com",
            #     'User-Agent': cookie['ua'],
            # }
            url = "http://zhanzhang.sogou.com/api/feedback/addMultiShensu"

            payload = "{\"site_type\":%s,\"email\":\"%s\",\"urls\":\"%s\",\"reason\":\"%s\",\"code\":\"%s\",\"sites\":%s}"%(task,email,urls,reason,code,sites)
            headers = {
                'Accept': "application/json, text/plain, */*",
                'Accept-Encoding': "gzip, deflate",
                'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                'Connection': "keep-alive",
                'Content-Type': "application/json;charset=UTF-8",
                'Cookie': "__ZHANZHANG_SID__=%s;__ZHANZHANG_SID__.sig=%s;"%(ZHANZHANG_SID,ZHANZHANG_SID_sig),
                'Host': "zhanzhang.sogou.com",
                'User-Agent': cookie['ua'],
            }

            response = requests.request("POST", url, data=payload.encode("utf-8").decode("latin1"), headers=headers)

            print(response.text)
            # r = requests.post(self.postUrl, headers=headers, json=data)

            resp = json.loads(response.text)
            print(f'线程{num}正在请求成功 {resp}')

            if resp['msg'] == 'success':
                print('%s  投诉成功 %s' %(num ,resp))
                self.saveSucceed(url)
                print('==' * 20)
            elif resp['msg'] == '验证码有误':
                print(f'验证码有误 重新输入中 {cookie}')
                verif_resp = requests.get(self.verifUrl, headers=headers)
                # 保存验证码
                self.saveVerifCode(verif_resp, num)
                # self.index(num)
                # self.q.put(url)
                pass
            elif resp['msg'] == 'anti校验失败':
                print('检验失败  当前账号不能提交数据')
                break
                # self.q.put(url)
                # self.index(num)
            else:
                print(resp)


if __name__ == '__main__':
    q = queue.Queue()
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

    doUrlAll = list_of_groups(urls, 1)

    for url in doUrlAll:
        q.put(url)

    def run():
        t = []
        for i,cookie in enumerate(Cookies):
            t.append(threading.Thread(target=SouGou(q).index, args=(i,eval(cookie))))
        for j in t:
            j.start()


    run()
