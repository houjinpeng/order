import time

import requests
import threading,queue


class Proxy():
    def __init__(self):
        self.proxy_queue = queue.Queue()

    def work(self):
        while True:
            if self.proxy_queue.qsize() >= 200:
                time.sleep(1)
                continue
            url = 'http://39.104.96.30:8888/SML.aspx?action=GetIPAPI&OrderNumber=98b90a0ef0fd11e6d054dcf38e343fe927999888&poolIndex=1628048006&poolnumber=0&cache=1&ExpectedIPtime=&Address=&cachetimems=0&Whitelist=&isp=&qty=20'
            try:
                r = requests.get(url, timeout=3)
                if '尝试修改提取筛选参数' in r.text:
                    time.sleep(2)
                    continue
                ip_list = r.text.split('\r\n')
                for ip in ip_list:
                    self.proxy_queue.put(ip.strip())
            except Exception as e:
                time.sleep(1)

    def get_proxies(self):
        ip = self.proxy_queue.get()
        if ip == '':
            return self.get_proxies()
        proxies = {
            'http': f'http://{ip}',
            'https': f'http://{ip}'
        }
        return proxies


