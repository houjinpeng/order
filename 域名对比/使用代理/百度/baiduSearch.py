# encoding:utf-8
import datetime
import os
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
# 文件路径
logFile = r"./conf/setting.cfg"
config.read(logFile, encoding="utf-8")
config = config.defaults()
count = eval(config['count'])
domain_list_tmp = []
ym_list = []
ym_file = './conf/ym.txt'
paichu_file = './pc.txt'
paichu_list = []


# 初始化敏感词
def sensitive():
    try:
        words = []
        with open("敏感词.txt", encoding="UTF-8-sig") as f:
            rows = f.readlines()
            for row in rows:
                row = row.replace("\n", "")
                words.append(row)

        words = [x for x in words if x]
        return words
    except Exception:
        return []


words = sensitive()


def get_domain(file_path):
    with open(file_path, 'r') as f:
        log.logger.debug(str(datetime.datetime.now()))
        all_data = f.readlines()
        for line in all_data:
            domain = line.strip()
            if domain == '':
                continue
            domain_list.put(domain)
        f.close()
        log.logger.debug(str(datetime.datetime.now()))


def get_proxies():
    while True:
        if proxy_queue.qsize() >= 20:
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



data_file = "./conf/baidu_%s.csv" % int(time.time())
# data_file = "./conf/baidu.csv"

# 写文件头
def write_hand():
    if os.path.exists(data_file):
        return
    with open(data_file, 'a',encoding='utf-8-sig') as file:
        file.write("网址,统计数量,敏感词,")
        for i in range(1, 16):
            # file.write("敏感词-" + str(i) + ",")
            file.write("搜索-" + str(i) + ",")
            file.write("快照-" + str(i) + ",")
        file.write("\n")


write_hand()


class BaiDu():
    def __init__(self):
        global count
        self.count = count
        self.s = requests.session()

    def get_proxy(self):
        try:
            ip = proxy_queue.get()
            proxies = {
                'http': f'http:{ip}',
                'https': f'http:{ip}'
            }
            self.ip = proxies
            self.s = requests.session()
            return proxies
        except Exception as e:
            time.sleep(2)
            return None

    # 判断domain
    def check_url(self, domain, check_url):
        try:
            domain = domain.lower()
            if len(domain) >20:
                if domain.split('.')[0][:20] in check_url:
                    return True
            if domain in check_url:
                # 判断开头是否是.
                indx = check_url.find(domain)
                if indx == 0:
                    try:
                        f = check_url[indx + len(domain)]
                        return False
                    except Exception:
                        return True
                else:
                    if check_url[indx - 1] == '.':
                        try:
                            f = check_url[indx + len(domain)]
                            if f == ':':
                                return True
                            return False
                        except Exception:
                            return True
                    else:
                        return False
            else:
                return False
        except Exception as e:
            log.logger.debug(e)
            return  False

    # 查找关键词
    def find_word(self, seg_list):
        global words
        """
        # 匹配敏感侧
        :param seg_list:
        :return:
        """
        title_sensi = ""

        for w in words:
            if str(w) in seg_list:
                title_sensi += w + "|"
        if title_sensi != "":
            return title_sensi
        else:
            return "无结果"


    def requests_handler(self, url1):

        url = "https://www.baidu.com/s"

        querystring = {"wd": f"site:{url1}"}
        payload = ""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
        }
        try:
            proxies = {
                "http": "http://user-sp68470966:maiyuan312@gate.dc.visitxiangtan.com:20000",
                "https": "http://user-sp68470966:maiyuan312@gate.dc.visitxiangtan.com:20000",
            }

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
        # self.get_proxy()
        while not domain_list.empty():
            domain = domain_list.get()
            r = self.requests_handler(domain)

            html = etree.HTML(r.text)
            if html == None:
                domain_list.put(domain)
                continue

            # 数据量
            h3_list = html.xpath('//h3[@class="c-title t t tts-title"]')
            if len(h3_list) == 0:
                h3_list = html.xpath('//h3[@class="t"]')

            if len(h3_list) == 0:
                query_result = domain + "," + str(len(h3_list)) + ","
                log.logger.info(domain)
                query_result += "无结果,"
                result_queue.put(query_result)
                log.logger.debug(f'{str(datetime.datetime.now())[:19]} 队列剩余{domain_list.qsize()} {domain}  域名解析完毕 {len(h3_list)}  已过滤')
                continue

            f = False
            sna_str = ''

            query_result_title = ''
            findword = ''
            query_result = domain + "," + str(len(h3_list)) + ","
            for d in h3_list:
                try:
                    # 先判断在不在里面 如果在再深入对比
                    snapshot = d.xpath('.//div[@class="f13 c-gap-top-xsmall se_st_footer user-avatar"]/a//text()')
                    for y in paichu_list:
                        if y in ''.join(snapshot):
                            log.logger.debuge(f'{str(datetime.datetime.now())[:19]} 队列剩余{domain_list.qsize()} {"".join(snapshot)} 域名在不合格文件中 pass')
                            continue

                    title = str(d.xpath('./a/text()')[0]).replace(",", " ").replace("\n", "")
                    source_url = self.get_domain_url(d.xpath('./a/@href')[0])
                    findword += title
                    query_result_title += title + ',' + source_url + ','
                    f = True
                except Exception as e:
                    log.logger.error(f'出错了 {e}')
                    continue

            if f == False:
                query_result += "无结果,"
                result_queue.put(query_result)
                log.logger.debug(f' 队列剩余{domain_list.qsize()} 此域名为：{domain} 查找到的域名为：{sna_str} 实际没有收录  已过滤 ')
                continue

            if int(count) >= self.count:
                log.logger.debug(f'队列剩余{domain_list.qsize()} {domain} 域名解析完毕 搜索数{len(h3_list)}')
                query_result = query_result + self.find_word(findword) + ',' + query_result_title
                result_queue.put(query_result)

                ym_list.append(domain)

        # log.logger.debug(f'退出线程  {domain_list.empty()}')


def save_data():
    while True:
        while not result_queue.empty():
            result = result_queue.get()
            try:
                with open(data_file, 'a+', encoding='utf-8-sig') as fw:
                    fw.write(str(result))
                    fw.write('\n')

                # log.logger.debug(f'结果队列剩余：{result_queue.qsize()}')
            except Exception:
                pass
        time.sleep(5)


if __name__ == '__main__':
    result_queue = Queue()
    proxy_queue = Queue()
    domain_list = Queue()

    # 初始化域名  存入队列
    file_name = "urls.txt"
    get_domain(file_name)

    # # 开启线程代理
    # t = threading.Thread(target=get_proxies)
    # t.start()

    # 开启任务
    thread_list = []
    for i in range(1):
        thread_list.append(threading.Thread(target=save_data))
    for t in thread_list:
        t.start()


    thread_list = []
    for i in range(eval(config['task_num'])):
    # for i in range(1):
        thread_list.append(threading.Thread(target=BaiDu().index))
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()

    log.logger.info('所有任务已完成')