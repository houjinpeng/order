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
    # 解析domain
    def extract_domain(self, ym_str):
        try:
            ym = ym_str[0]
            index = ym_str[0].find(':')
            if index == -1:
                return ym.split('/')[0]
            else:
                try:
                    if isinstance(int(ym_str[0][index + 1]), int):
                        return ym_str[0].split(':')[0]
                except Exception as e:
                    ym_str[0] = ym_str[0][index+1:]
                    return self.extract_domain(ym_str)
        except Exception :
            ym = ''
            return ym
        # pattern = re.compile(r'(.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+.?')
        # domain_str = ''.join(ym_str)
        # try:
        #     ym = pattern.search(domain_str).group()
        #     ym = ym.split('/')[0].strip()
        # except Exception:
        #     ym = ''
        # return ym

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
            'Accept': "*/*",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            'Connection': "keep-alive",
            'Cookie': "WWW_ST=1624067751996",
            'Host': "www.baidu.com",
            'is_pbs': "%E4%BD%A0%E5%A5%BD",
            'is_referer': "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E4%BD%A0%E5%A5%BD&fenlei=256&rsv_pq=d68e237d000e97ec&rsv_t=2308ro2iwEVnzggZoenprp1uScBJPhffZUI3BDbKGrDhZhQUDI2mGgRNSKc&rqlang=cn&rsv_enter=0&rsv_dl=tb&rsv_sug3=12&rsv_sug1=2&rsv_sug7=100&rsv_btype=i&inputT=114794&rsv_sug4=114794",
            'is_xhr': "1",
            'Referer': "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=nihao&fenlei=256&oq=%25E4%25BD%25A0%25E5%25A5%25BD&rsv_pq=f45400fe0070719b&rsv_t=3ccc3%2FkSLGMu1xZjO4PnjoL04WKZ5fTj6pwA4zKMOrJ6I28Wz175YpDPWs4&rqlang=cn&rsv_enter=0&rsv_dl=tb&rsv_btype=t",
            'sec-ch-ua-mobile': "?0",
            'Sec-Fetch-Dest': "empty",
            'Sec-Fetch-Mode': "cors",
            'Sec-Fetch-Site': "same-origin",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
            'X-Requested-With': "XMLHttpRequest",
        }
        try:
            response = requests.request("GET", url, data=payload, headers=headers, params=querystring,proxies=self.ip,timeout=3)
            response.encoding = 'utf-8'
            if '验证码' in response.text:
                self.get_proxy()
                log.logger.error('更换代理')
                return self.requests_handler(url1)

            return response
        except Exception as e:
            self.get_proxy()
            log.logger.error(f'更换代理 {e}')
            return self.requests_handler(url1)

    def index(self):
        global ym_list
        self.get_proxy()
        while not domain_list.empty():
            domain = domain_list.get()
            r = self.requests_handler(domain)
            try:
                html = etree.HTML(r.text)
                if html == None:
                    domain_list.put(domain)
                    continue
            except Exception as e:
                domain_list.put(domain)
                log.logger.debug(f'xpath {e}')
                continue
            # 数据量
            div_list = html.xpath('//div[@class="result c-container new-pmd"]')
            if len(div_list) == 0:
                query_result = domain + "," + str(len(div_list)) + ","
                query_result += "无结果,"
                result_queue.put(query_result)
                log.logger.debug(f'{str(datetime.datetime.now())[:19]} 队列剩余{domain_list.qsize()} {domain}  域名解析完毕 {len(div_list)}  已过滤')
                continue
            # try:
            #     # 查询收录数量
            #     count_str = html.xpath('//span[@class="nums_text"]/text()')
            #     if count_str:
            #         count = str("".join(re.findall(r'\d+', count_str[0])))
            #     else:
            #         count = "0"
            # except Exception as  e:
            #     # log.logger.debug(f'收录数查询出错 {e}')
            #     count = "0"
            # query_result = domain + "," + count + ","
            # if count == '0':
            #     query_result += "无结果,"
            #     result_queue.put(query_result)
            #     log.logger.debug(f'{str(datetime.datetime.now())[:19]} 队列剩余{domain_list.qsize()} {domain}  域名解析完毕 {count_str}  已过滤')
            #     continue

            f = False
            sna_str = ''

            query_result_title = ''
            findword = ''
            query_result = domain + "," + str(len(div_list)) + ","
            for d in div_list:
                try:
                    # 先判断在不在里面 如果在再深入对比
                    snapshot = d.xpath('.//div[@class="f13 c-gap-top-xsmall se_st_footer user-avatar"]/a//text()')
                    if snapshot == []:
                        snapshot = d.xpath('.//div[@class="f13 c-gap-top-small se_st_footer user-avatar"]/a//text()')
                    for y in paichu_list:
                        if y in ''.join(snapshot):
                            log.logger.debuge(f'{str(datetime.datetime.now())[:19]} 队列剩余{domain_list.qsize()} {"".join(snapshot)} 域名在不合格文件中 pass')
                            continue

                    parse_domain_str = self.extract_domain(snapshot)
                    f = self.check_url(domain, parse_domain_str)
                    if f == False:
                        sna_str += parse_domain_str + ','
                        continue
                    else:
                        title = str(d.xpath('./h3/a/text()')[0]).replace(",", " ").replace("\n", "")
                        findword += title
                        query_result_title += title + ',' + parse_domain_str + ','

                except Exception as e:
                    continue

            if f == False:
                query_result += "无结果,"
                result_queue.put(query_result)
                log.logger.debug(f' 队列剩余{domain_list.qsize()} 此域名为：{domain} 查找到的域名为：{sna_str} 实际没有收录  已过滤 ')
                continue

            if int(count) >= self.count:
                log.logger.debug(f'{str(datetime.datetime.now())[:19]}  队列剩余{domain_list.qsize()} {domain} 域名解析完毕 搜索数{count}')
                query_result = query_result + self.find_word(findword) + ',' + query_result_title
                result_queue.put(query_result)

                ym_list.append(domain)

        log.logger.debug(f'退出线程  {domain_list.empty()}')


def save_data():
    while True:
        while not result_queue.empty():
            result = result_queue.get()
            try:
                # lock.acquire()  # 加锁
                with open(data_file, 'a+', encoding='utf-8-sig') as fw:
                    fw.write(str(result))
                    fw.write('\n')
                # lock.release()  # 释放锁

                # log.logger.debug(f'结果队列剩余：{result_queue.qsize()}')
            except Exception:
                pass
        time.sleep(5)


if __name__ == '__main__':
    result_queue = Queue()
    proxy_queue = Queue()
    domain_list = Queue()
    cookie_queue = Queue()

    lock = threading.Lock()

    # 初始化域名  存入队列
    file_name = "urls.txt"
    get_domain(file_name)

    # 开启线程代理
    t = threading.Thread(target=get_proxies)
    t.start()

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
