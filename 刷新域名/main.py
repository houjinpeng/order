import requests
import threading,queue
import time,datetime
import re
import json
import base64

#初始化url
with open('./url.txt','r',encoding='utf-8') as fr:
    data_list = fr.readlines()



def get_proxies():
    while True:
        if proxy_queue.qsize() >= 200:
            time.sleep(1)
            continue
        url = 'http://39.104.96.30:8888/SML.aspx?action=GetIPAPI&OrderNumber=98b90a0ef0fd11e6d054dcf38e343fe927999888&poolIndex=1628048006&poolnumber=0&cache=1&ExpectedIPtime=&Address=&cachetimems=0&Whitelist=&isp=&qty=20'
        try:
            r = requests.get(url,timeout=3)
            if '尝试修改提取筛选参数' in r.text:
                time.sleep(2)
                continue
            ip_list = r.text.split('\r\n')
            for ip in ip_list:
                proxy_queue.put(ip.strip())
        except Exception as e:
            time.sleep(1)

class Refresh():

    def request_headler(self,url,data=None):
        try:
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Content-Length': '62',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': '47.56.160.68:10299',
                'Origin': 'http://www.jucha.com',
                'Referer': 'http://www.jucha.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
                'Cookie': 'SRVHASH=cbcd42843507235c'
            }
            u = 'http://47.56.160.68:10392/api.php'
            r = requests.post(u,headers=headers,data=data,timeout=3)
            return r

        except Exception as e:
            return self.request_headler(url,data)

    def check(self,data):
        try:
            data = json.loads(data)
            now_time = time.localtime(time.time())
            year = str(now_time.tm_year)
            mon = str(now_time.tm_mon)
            day = '0'+str(now_time.tm_mday) if now_time.tm_mday < 10 else str(now_time.tm_mday)
            time_str = year+mon+day
            if time_str in data['data']['sj_max']:
                return True
            # now_time = str(datetime.datetime.now())[:10]
            # if data['data']['gxsj'] >= now_time+' 00:00:00':
            #     return True
            return False
        except Exception as e:
            return False


    def save_url(self,url):
        with open('successful.txt','a',encoding='utf-8') as fw:
            fw.write(url+'\n')

    def index(self,url):
        # 获取域名
        domain = re.findall('ym=(.*?)&', url)[0]
        domain = base64.b64decode(domain).decode()
        token = re.findall('token=(.*)', url)[0]
        while True:
            post_url = 'http://47.56.160.68:10299/api.php'
            data = f'qg=&ym={domain}&token={token}'
            r = self.request_headler(post_url,data)
            is_refresh = self.check(r.text)
            if is_refresh == True:
                #保存
                self.save_url(url)
                print(f'成功 {url}')
                break
            time.sleep(3)

if __name__ == '__main__':
    proxy_queue = queue.Queue()
    thread_list = []

    for url in data_list:
        if url != '':
            thread_list.append(threading.Thread(target=Refresh().index,args=(url.strip(),)))

    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()