# encoding:utf-8
import datetime
import os
import urllib.parse

from logger import Logger
import re, random
import time
import requests
from lxml import etree
from queue import Queue
from urllib.parse import quote
# from fake_useragent import UserAgent
import threading
import configparser

log = Logger('ym.log', level='debug')

'''读写配置文件'''
config = configparser.ConfigParser()
domain_list_tmp = []
ym_list = []
ym_file = './conf/ym.txt'
paichu_file = './pc.txt'
paichu_list = []
proxies = {
                "http": "http://user-sp68470966:maiyuan312@gate.dc.visitxiangtan.com:20000",
                "https": "http://user-sp68470966:maiyuan312@gate.dc.visitxiangtan.com:20000",
            }
def get_domain(file_path):
    with open(file_path, 'r',encoding='utf-8') as f:
        log.logger.debug(str(datetime.datetime.now()))
        all_data = f.readlines()
    try:
        with open('out.txt', 'r',encoding='utf-8') as f:
            log.logger.debug(str(datetime.datetime.now()))
            all_data1 = f.readlines()
        all_data1 = [d.strip() for d in all_data1]
    except Exception:
        all_data1 = []

    for line in all_data:
        domain = line.strip()
        if domain in all_data1:
            continue
        if domain == '':
            continue
        domain_list.put(domain)
    f.close()
    log.logger.debug(str(datetime.datetime.now()))

#判断是否是中文
def is_Chinese(string):
    for ch in string:
        if '\u4e00' <= ch <= '\u9fff':
            return '是'
        return '否'


# data_file = "./conf/baidu_%s.csv" % int(time.time())
data_file = "百度排名.csv"

# 写文件头
def write_hand():
    if os.path.exists(data_file):
        return
    with open(data_file, 'a',encoding='utf-8-sig') as file:
        file.write("域名,收录数量,是否中文,标题-1,url,排名,标题-2,url,排名")

        file.write("\n")

def save_data():
    while True:
        while not result_queue.empty():
            result = result_queue.get()
            try:
                with open(data_file, 'a+', encoding='utf-8-sig') as fw:
                    fw.write(str(result))
                    fw.write('\n')
            except Exception:
                pass
        time.sleep(5)


def save_out_data():
    while True:
        while not out_domain_queue.empty():
            result = out_domain_queue.get()
            try:
                with open('out.txt', 'a+', encoding='utf-8-sig') as fw:
                    fw.write(str(result))
                    fw.write('\n')

                # log.logger.debug(f'结果队列剩余：{result_queue.qsize()}')
            except Exception:
                pass
        time.sleep(5)



class BaiDu():
    def __init__(self):
        global count
        self.s = requests.session()

    def requests_handler(self, url1):

        url = "https://www.baidu.com/s"

        querystring = {"wd": f"site:{url1}"}
        payload = ""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
        }
        try:


            # response = requests.request("GET", url, data=payload, headers=headers, params=querystring,proxies=self.ip,timeout=3)
            response = requests.request("GET", url, data=payload, headers=headers, params=querystring,proxies=proxies,timeout=3)
            response.encoding = 'utf-8'
            if '验证码' in response.text or '百度安全验证' in response.text:
                # self.get_proxy()
                # log.logger.error('出现百度安全验证 更换代理')
                return self.requests_handler(url1)

            return response
        except Exception as e:
            # self.get_proxy()
            # log.logger.error(f'更换代理 {e}')
            return self.requests_handler(url1)

    #获取排名
    def get_paiming(self,title,domain):
        try:
            url = f'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd={urllib.parse.quote(title)}&op={urllib.parse.quote(title)}'
            # r = requests.get(url,proxies=proxies,timeout=5)
            headers = {
                # 'Cookie':'BD_UPN=12314753; PSTM=1649637155; BAIDUID=792DD341145E85AF03D2DE66531C8971:FG=1; BIDUPSID=B2CE0F7F4FACBD5E54D7A2EF967F7D5D; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=36166_34584_36120_36125_35802_36224_26350_36300_36313_36061; delPer=0; BD_CK_SAM=1; PSINO=1; BAIDUID_BFESS=792DD341145E85AF03D2DE66531C8971:FG=1; BA_HECTOR=a0a18h058k21ah8leb1h67krt0q; H_PS_645EC=c0aapuyySUjGlEPYfoLP3%2FsDRxLNvxtOOLorsr%2B4CrQ%2BUHWo%2FRcAzBX8L%2Bk; BDSVRTM=234; COOKIE_SESSION=1_0_9_9_0_9_0_0_9_9_2_0_0_0_0_0_0_0_1650709375%7C9%2384040_32_1648517612%7C9; WWW_ST=1650709382534',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
            }
            r = requests.get(url,headers=headers,proxies=proxies,timeout=5)
            r.encoding='utf-8'
            if '百度安全验证' in r.text:
                return self.get_paiming(title, domain)
            # elif '抱歉没有找到与' in r.text:
            #     return self.get_paiming(title, domain)

            e = etree.HTML(r.text)
            h3_list = e.xpath('//h3[@class="c-title t t tts-title"]')
            for i,d in enumerate(h3_list):
                try:
                    # 获取title
                    domain_l = self.get_domain_url(''.join(d.xpath('./a//@href')))
                    if domain in domain_l:
                        return i+1
                except :
                    pass

            return 0

        except Exception as error:
            return self.get_paiming(title,domain)

    def get_domain_url(self,baidu_url,count=0):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
            }
            # r = requests.get(baidu_url,headers=headers,verify=False)
            r = requests.get(baidu_url, headers=headers, verify=False, allow_redirects=False)
            url = r.headers._store['location'][1].replace('http://','').replace('https://','')

            return url
        except Exception as e:
            if count < 5:
                return self.get_domain_url(baidu_url,count+1)
            return ''

    def index(self):
        global ym_list
        while not domain_list.empty():
            domain = domain_list.get()
            log.logger.debug(f'队列剩余{domain_list.qsize()} {domain} 域名开始任务')

            r = self.requests_handler(domain)
            try:
                record_num = re.findall('找到相关结果数约(.*?)个',r.text)[0].replace(',','')
            except Exception as e:
                record_num = 0
            if record_num == 0:
                out_domain_queue.put(domain)
                continue

            html = etree.HTML(r.text)
            if html == None:
                domain_list.put(domain)
                continue

            # 数据量
            h3_list = html.xpath('//h3[@class="c-title t t tts-title"]')
            if len(h3_list) == 0:
                h3_list = html.xpath('//h3[@class="t"]')

            if len(h3_list) == 0:
                out_domain_queue.put(domain)
                continue



            is_chinese = is_Chinese(''.join(h3_list[0].xpath('./a/text()')))
            data = domain + ',' + str(record_num) + ','+is_chinese+','
            for d in h3_list[:2]:
                try:
                    # 获取title
                    title = ''.join(d.xpath('./a/text()')).replace(',','|')
                    #获取url
                    url = self.get_domain_url(''.join(d.xpath('./a/@href')))
                    if url.replace('/','')== domain or url.replace('/','') == 'www.'+domain:
                        #获取排名
                        paiming = self.get_paiming(title,domain)
                        data += title + ',' + url + ','+str(paiming)+ ','
                    else:
                        out_domain_queue.put(domain)
                        continue
                except Exception as e:
                    log.logger.error(f'出错了 {e}')
                    continue
            result_queue.put(data)
            out_domain_queue.put(domain)

        # log.logger.debug(f'退出线程  {domain_list.empty()}')



if __name__ == '__main__':
    result_queue = Queue()
    domain_list = Queue()
    out_domain_queue = Queue()
    #写头文件
    write_hand()

    # 初始化域名  存入队列
    file_name = "urls.txt"
    get_domain(file_name)

    # 开启保存数据任务
    threading.Thread(target=save_data).start()
    threading.Thread(target=save_out_data).start()


    thread_list = []
    for i in range(1):
        thread_list.append(threading.Thread(target=BaiDu().index))
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()

    log.logger.info('所有任务已完成')