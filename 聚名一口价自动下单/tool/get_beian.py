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
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

proxy_queue = queue.Queue()
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

class BeiAn():
    def __init__(self):
        self.url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/icpAbbreviateInfo/queryByCondition'
        self.domain = ''
        self.set_proxies()
        self.token = ''


    def set_proxies(self):

        ip = proxy_queue.get()
        self.s = requests.session()
        self.proxies = {
            'http': f'http://{ip}',
            'https': f'http://{ip}'
        }
        print(f'域名：{self.domain}更换代理 {self.proxies}')

    def request_handler(self,url,data,headers,type='data'):
        try:
            if type == 'data':
                r = self.s.post(url, headers=headers, verify=False, data=data, proxies=self.proxies,timeout=10)
            else:
                r = self.s.post(url, headers=headers, verify=False, json=data, proxies=self.proxies,timeout=10)
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

    def get_cookie(self):
        url = "https://beian.miit.gov.cn/"
        headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
        }
        try:
            response = self.s.get(url, proxies=self.proxies,headers=headers,timeout=10)
        except Exception as e:
            self.set_proxies()
            return None
        return response

    def get_token(self):
        m = hashlib.md5()
        m.update(f'testtest{int(time.time() * 1000)}'.encode('utf-8'))
        auth_url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/auth'
        headers = {
            'Accept': "*/*",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            'Connection': "keep-alive",
            'Content-Length': "64",
            'cookie':'__jsluid_s=06ee83aa108ede7f9ba961531738304e',
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
            # self.set_proxies()
            # return self.beian_info(self.domain)
            # return self.get_token()
            return None
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
            self.set_proxies()
            self.token = ''
            return None,None,None
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

    def get_detail_data(self, param, token, uuid,domain):
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
        data_parm = {"pageNum": "", "pageSize": "", "unitName": domain}
        r = self.request_handler(detail_url,data_parm,headers,type='json')
        if r == None:
            return None
        data = json.loads(r.text)
        return data

    def beian_info(self,domain):
        if self.token == '':
            self.domain = domain
            self.s = requests.session()
            cookie_r = self.get_cookie()
            if cookie_r == None:
                self.token = ''
                return None
            r = self.get_token()
            if r == None:
                self.token = ''
                return None

            self.token = json.loads(r.text)['params']['bussiness']

        fg, bg, uuid = self.get_img(self.token)
        if fg == None:
            self.token = ''
            return None
        distance = self.get_distance(fg, bg)
        param = self.check_img(self.token, uuid, distance)
        if param == None:
            self.token = ''
            return None
        return self.get_detail_data(param, self.token, uuid,domain)



if __name__ == '__main__':
    t = threading.Thread(target=get_proxies)
    t.start()
    data = BeiAn().beian_info('baidu.com')
    print(data)

