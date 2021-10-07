import datetime
import logging
import os
import time
import base64
from io import BytesIO
import cv2
import requests
import json
import numpy as np
import hashlib
import threading, queue

logging.basicConfig(level=logging.INFO, format='%(asctime)s -line:%(lineno)d - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

domain_queue = queue.Queue()
proxy_queue = queue.Queue()
file_name = "urls.txt"
data_file = "beian_%s.csv" % int(time.time())
lock = threading.Lock()

try:
    with open('outurl.txt', 'r', encoding='utf-8') as f:
        out_url_list = f.readlines()
except Exception:
    out_url_list = []


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

# 把域名存入队列
def get_domain(file_path):
    with open(file_path, 'r') as f:
        logger.info(str(datetime.datetime.now()))
        all_data = f.readlines()
        data = list(set(all_data).difference(set(out_url_list)))
        for line in data:
            domain = line.strip()
            if domain == '':
                continue
            domain_queue.put(domain)
        f.close()
        logger.info(str(datetime.datetime.now()))

# 写文件头
def write_hand():
    if os.path.exists(data_file):
        return
    with open(data_file, 'a', encoding='utf-8-sig') as file:
        file.write("域名,主办方单位名称,主办方单位性质,网站备案号,网站名称,网站首页,审核日期,是否限制接入")
        file.write("\n")


class BeiAn():
    def __init__(self):
        self.url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/icpAbbreviateInfo/queryByCondition'

    def set_proxies(self):
        # logger.info('更换代理')
        ip = proxy_queue.get()
        self.proxies = {
            'http': f'http:{ip}',
            'https': f'https:{ip}'
        }

    def request_handler(self,url,data,headers,type='data'):
        try:
            if type == 'data':
                r = requests.post(url, headers=headers, data=data, proxies=self.proxies,timeout=10)
            else:
                r = requests.post(url, headers=headers, json=data, proxies=self.proxies,timeout=10)
            try:
                data = json.loads(r.text)
            except Exception as e:
                return None
            if data['success'] == False:
                return None
            return r
        except Exception as e:
            return None

    def get_distance(self, fg, bg):
        """
        计算滑动距离
        """
        target = cv2.imdecode(np.asarray(bytearray(fg.read()), dtype=np.uint8), 0)
        template = cv2.imdecode(np.asarray(bytearray(bg.read()), dtype=np.uint8), 0)
        result = cv2.matchTemplate(target, template, cv2.TM_CCORR_NORMED)
        _, distance = np.unravel_index(result.argmax(), result.shape)
        return distance

    def get_token(self):
        # logger.info('获取token')
        m = hashlib.md5()
        m.update(f'testtest{int(time.time() * 1000)}'.encode('utf-8'))
        auth_url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/auth'
        headers = {
            'Accept': "*/*",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            'Connection': "keep-alive",
            'Content-Length': "64",
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
            'Host': "hlwicpfwc.miit.gov.cn",
            'Origin': "https://beian.miit.gov.cn",
            'Referer': "https://beian.miit.gov.cn/",
            'sec-ch-ua-mobile': "?0",
            'Sec-Fetch-Dest': "empty",
            'Sec-Fetch-Mode': "cors",
            'Sec-Fetch-Site': "same-site",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55",
            # 'User-Agent': UserAgent().chrome,
        }
        data = f'authKey={m.hexdigest()}&timeStamp={int((time.time() * 1000))}'
        r = self.request_handler(auth_url,data,headers)
        if r == None:
            proxies = self.set_proxies()
            return self.get_token()
        # logger.info('获取token成功  获取验证码图片 ')
        return r

    def get_img(self, token):
        # logger.info('获取验证码')
        img_url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/image/getCheckImage'
        headers = {
            'Accept': "application/json, text/plain, */*",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Content-Length': "0",
            'Cookie': "__jsluid_s=5a0a7ae4dcb6eea5a1621a0fb51d8efe",
            'Host': "hlwicpfwc.miit.gov.cn",
            'Origin': "https://beian.miit.gov.cn",
            'Referer': "https://beian.miit.gov.cn/",
            'sec-ch-ua-mobile': "?0",
            'Sec-Fetch-Dest': "empty",
            'Sec-Fetch-Mode': "cors",
            'Sec-Fetch-Site': "same-site",
            'token': f"{token}",
            # 'User-Agent': UserAgent().chrome,
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        }
        # 获取验证码图片 并返回
        img_resp = self.request_handler(img_url,data='',headers=headers)
        if img_resp == None:
            proxies = self.set_proxies()
            return self.get_img(token)
        # logger.info("验证码获取成功  破解中···")
        img_data = json.loads(img_resp.text)
        big_img = img_data['params']['bigImage']
        fg = BytesIO(base64.b64decode(big_img))
        small_img = img_data['params']['smallImage']
        bg = BytesIO(base64.b64decode(small_img))
        uuid = img_data['params']['uuid']
        return fg, bg, uuid

    def check_img(self, token, uuid, distance):
        # 验证滑动验证码
        headers = {
            'Accept': "application/json, text/plain, */*",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Content-Length': "60",
            'Content-Type': "application/json",
            'Cookie': "__jsluid_s=5a0a7ae4dcb6eea5a1621a0fb51d8efe",
            'Host': "hlwicpfwc.miit.gov.cn",
            'Origin': "https://beian.miit.gov.cn",
            'Referer': "https://beian.miit.gov.cn/",
            'sec-ch-ua-mobile': "?0",
            'Sec-Fetch-Dest': "empty",
            'Sec-Fetch-Mode': "cors",
            'Sec-Fetch-Site': "same-site",
            'token': token,
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        }
        check_url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/image/checkImage'

        data = {"key": uuid, "value": f"{distance}"}
        r = self.request_handler(check_url,data,headers,type='json')
        if r ==None:
            return None
        # logger.info('破解成功')
        result = json.loads(r.text)
        if result['success'] == True:
            return result['params']
        else:
            return None

    def get_detail_data(self, param, token, uuid):
        detail_url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/icpAbbreviateInfo/queryByCondition'
        headers = {
            'Accept': "application/json, text/plain, */*",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Content-Length': "51",
            'Content-Type': "application/json",
            'Cookie': "__jsluid_s=5a0a7ae4dcb6eea5a1621a0fb51d8efe",
            'Host': "hlwicpfwc.miit.gov.cn",
            'Origin': "https://beian.miit.gov.cn",
            'Referer': "https://beian.miit.gov.cn/",
            'sec-ch-ua-mobile': "?0",
            'Sec-Fetch-Dest': "empty",
            'Sec-Fetch-Mode': "cors",
            'Sec-Fetch-Site': "same-site",
            'sign': param,
            'token': token,
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            'uuid': uuid,
        }
        while not domain_queue.empty():
            try:
                domain = domain_queue.get(timeout=3)
            except Exception as e:
                return
            data = {"pageNum": "", "pageSize": "", "unitName": domain}
            r = self.request_handler(detail_url,data,headers,type='json')
            if r == None:
                domain_queue.put(domain)
                return
            data = json.loads(r.text)
            logger.info(f'队列剩余任务：{domain_queue.qsize()} {r.text}')
            with open('outurl.txt', 'a', encoding='utf-8') as fw:
                fw.write(domain+'\n')
            self.parse_detail(domain,data)

    def save_data(self,data_dict):
        with open(data_file,'a',encoding='utf-8-sig') as fw:
            try:
                fw.write(data_dict['domain']+',')
                fw.write(data_dict['unitName']+',')
                fw.write(data_dict['natureName']+',')
                fw.write(data_dict['serviceLicence']+',')
                fw.write(data_dict['serviceName']+',')
                fw.write(data_dict['homeUrl']+',')
                fw.write(data_dict['updateRecordTime']+',')
                fw.write(data_dict['limitAccess'])
                fw.write('\n')
            except Exception as e:
                fw.write('\n')

    def parse_detail(self,domain, data):
        if data['params']['list'] == []:
            lock.acquire()  # 加锁
            self.save_data({'domain':domain})
            lock.release()  # 释放锁
            return None
        d = data['params']['list'][0]
        data_dict = {
            'domain':domain,
            'unitName': d['unitName'],
            'natureName': d['natureName'],
            'serviceLicence': d['serviceLicence'],
            'serviceName': d['serviceName'],
            'homeUrl': d['homeUrl'],
            'updateRecordTime': d['updateRecordTime'],
            'limitAccess': d['limitAccess'],
        }
        lock.acquire()  # 加锁
        self.save_data(data_dict)
        lock.release()  # 释放锁

    def index(self,i):
        self.proxies = self.set_proxies()
        while not domain_queue.empty():
            r = self.get_token()
            token = json.loads(r.text)['params']['bussiness']
            fg, bg, uuid = self.get_img(token)
            distance = self.get_distance(fg, bg)
            param = self.check_img(token, uuid, distance)
            if param == None:
                continue
            self.get_detail_data(param, token, uuid)

        logger.info(f'线程{i}结束任务')
if __name__ == '__main__':
    #初始化域名 写文件头
    get_domain(file_name)
    logger.info(f'总任务数量：{domain_queue.qsize()}')
    write_hand()

    # 开启线程代理
    t = threading.Thread(target=get_proxies)
    t.start()


    thread_list = []
    if domain_queue.qsize() > 200:
        num = 200
    else:
        num = domain_queue.qsize()
    for i in range(num):
        thread_list.append(threading.Thread(target=BeiAn().index,args=(i,)))
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()

# BeiAn().start()
# BeiAn().index()