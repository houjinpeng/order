#encode=utf-8
import threading
import datetime
import logging
import os
import time
import requests,queue
import json
from lxml import etree
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

proxies = {
            "http": "http://user-sp68470966:maiyuan312@gate.dc.visitxiangtan.com:20000",
            "https": "http://user-sp68470966:maiyuan312@gate.dc.visitxiangtan.com:20000",
        }
class BeiAn():
    def __init__(self):
        self.url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/icpAbbreviateInfo/queryByCondition'

    def request_haders(self,url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            }
            r = requests.get(url,headers=headers)
            return r
        except Exception as e:
            return self.request_haders(url)


    def beian_info(self,domain):
        url = f'https://www.beianx.cn/search/{domain}'
        r = self.request_haders(url)
        e = etree.HTML(r.text)
        try:
            data = {
                'beian_num':e.xpath('//tr[1]/td/text()')[4].strip(),
                'xingzhi':e.xpath('//tr[1]/td/text()')[3].strip(),
                'shenhe_time':e.xpath('//tr[1]/td/text()')[-4].strip(),
                'shouye':e.xpath('//tr[1]/td//@href')[1],
            }
            try:
                info_url = 'https://www.beianx.cn'+ e.xpath('//td[@nowrap="nowrap"]/a/@href')[0]
                print(domain,info_url)
                resp = requests.get(info_url,proxies=proxies)
                if resp.status_code == 404:
                    # print(resp)
                    pass

            except Exception as e:
               # print(resp)
                pass


            return data
        except Exception as e:
            return {}

    def index(self):
        while not q.empty():
            domain = q.get()
            domain_info = self.beian_info(domain)
            print(domain,domain_info)


if __name__ == '__main__':
    q = queue.Queue()
    with open('../conf/urls.txt','r') as fr:
        data = fr.readlines()

    for d in data:
        q.put(d.strip())
    t = []
    for i in range(10):
        t.append(threading.Thread(target=BeiAn().index))
    for j in t:
        j.start()
    for j in t:
        j.join()