import time
import requests
from lxml import etree
import threading, queue
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s -line:%(lineno)d - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

proxies = {
    "http": "http://user-sp68470966:maiyuan312@gate.dc.visitxiangtan.com:20000",
    "https": "http://user-sp68470966:maiyuan312@gate.dc.visitxiangtan.com:20000",
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
try:
    with open('url.txt', 'r', encoding='utf-8') as fr:
        data = fr.readlines()
    with open('faill_url.txt', 'r', encoding='utf-8') as fr:
        data1 = fr.readlines()
    with open('succeed_url.txt', 'r', encoding='utf-8') as fr:
        data2 = fr.readlines()
except Exception as e:
    data1 = []
    data2 = []
a = data1 + data2
data = set(data).difference(set(a))


def save_txt(url, status):
    if status == 'faill':
        with open('faill_url.txt', 'a', encoding='utf-8') as fw:
            fw.write(url + '\n')
    else:
        with open('succeed_url.txt', 'a', encoding='utf-8') as fw:
            fw.write(url + '\n')


def get_url_titile(url):
    try:
        yuan_url = url.split('save')[1][1:]
        r = requests.get(yuan_url, headers=headers, timeout=10)
        r.encoding = 'utf-8'
        e = etree.HTML(r.text)
        title = e.xpath('//title/text()')
        return title
    except Exception as e:
        return '???'


def index():
    while not url_queue.empty():
        i = 0
        url = url_queue.get()
        while True:
            i += 1
            try:
                # r = requests.get(url.strip(),headers=headers,timeout=40)
                r = requests.get(url.strip(), headers=headers, timeout=30, proxies=proxies)
                if '?????????????????????????????????' in r.text:
                    logger.info('?????????????????????????????????  ??????5????????????????????? ??????????????????ip')
                    time.sleep(5 * 60)
                    continue
                e = etree.HTML(r.text)
                title = e.xpath('//title/text()')
                if 'Please contact your service provider for more details' in r.text:
                    logger.info(f'?????????{url_queue.qsize()} ??????:{url.strip()} ?????? Please contact your service provider for more details ')
                    save_txt(url.strip(), 'faill')
                    break
                if len(title) != 1 or title[0] == '502 Bad Gateway':
                    time.sleep(1)  # Your use of the Wayback Machine is subject to the Internet Archive's
                    url_queue.put(url)
                    break
                yuan_title = get_url_titile(url.strip())
                if yuan_title == title:
                    logger.info(f'?????????{url_queue.qsize()} ??????:{url.strip()} ??????  ?????????:{title[0]} {yuan_title[0]}')
                    save_txt(url.strip(), 'succeed')
                    i = 0
                    break
                else:
                    if i > 5:
                        i = 0
                        logger.info(f'?????????{url_queue.qsize()} ??????:{url.strip()} ??????  ?????????:{title[0]} {yuan_title[0]}')
                        save_txt(url.strip(), 'faill')
                        time.sleep(1)
                        break

            except Exception as e:
                logger.info(e)


# ?????????????????????????????????????????????
if __name__ == '__main__':
    url_queue = queue.Queue()
    for u in data:
        url_queue.put(u)
    t = []
    for i in range(100):
        t.append(threading.Thread(target=index))
    for j in t:
        j.start()
    for j in t:
        j.join()

    logger.info('??????,???????????????')
    time.sleep(100000)
