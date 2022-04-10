import time
import requests
from lxml import etree
import threading, queue
import logging



proxies = {
    "http": "http://user-sp68470966:maiyuan312@gate.dc.smartproxy.com:20000",
    "https": "https://user-sp68470966:maiyuan312@gate.dc.smartproxy.com:20000",
}
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}

url = 'http://web.archive.org/save/http://thesisnailstudio.com'
r = requests.get(url,headers=headers,proxies=proxies)
print(r.text)