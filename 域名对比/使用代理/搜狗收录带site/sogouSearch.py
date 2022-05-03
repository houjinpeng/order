import datetime
import re
import time
import requests
from lxml import etree
from queue import Queue
from fake_useragent import UserAgent
import threading
import configparser
from logger import Logger
log = Logger('ym.log', level='debug')

'''读写配置文件'''
config = configparser.ConfigParser()
# 文件路径
logFile = r"./conf/setting.cfg"
config.read(logFile, encoding="utf-8")
config = config.defaults()
count = 1
domain_list_tmp = []
ym_list = []
ym_file = './conf/ym.txt'
paichu_file = './conf/pc.txt'
paichu_list = []

try:
    with open(ym_file, 'r') as fr:
        dl = fr.readlines()
    for ym in dl:
        ym_list.append(ym.split(',')[0].strip())
    with open(paichu_file, 'r') as fr:
        dl = fr.readlines()
    for ym in dl:
        paichu_list.append(ym.strip())
except Exception :
    pass


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

def get_domain(file_path):
    # while True:
    with open(file_path, 'r') as f:
        print(str(datetime.datetime.now()))
        all_data = f.readlines()
        for line in all_data:
            domain = line.strip()
            if domain == '':
                continue
            domain_list.put(domain)
        f.close()
        print(str(datetime.datetime.now()))


class SoGou():
    def __init__(self):
        global count
        self.flag = False
        self.count = count
        self.i = 0

    def check_url(self,domain,check_url):
        domain = domain.lower()
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
                        return False
                    except Exception:
                        return True
                else:
                    return False
        else:
            return False

    def extract_domain(self,ym_str):
        if '-' in ''.join(ym_str).lower().strip()[:10]:
            if ''.join(ym_str).lower().find('-')+1 == '':
                snapshot = ''.join(ym_str).lower().split('-')[1]
            else:
                snapshot = ''.join(ym_str).lower().split('/')[0].strip()

            if 'htt' in snapshot:
                snapshot = snapshot.split('/')[2].strip()
            else:
                snapshot = snapshot.split('/')[0].strip()
        else:
            snapshot = ''.join(ym_str).lower().split('/')[0].strip()

        return snapshot

    def set_cookie(self):
        try:
            headers = {
                'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                'Accept-Encoding': "gzip, deflate, br",
                'Accept-Language': "zh-CN,zh;q=0.9",
                'Connection': "keep-alive",
                'Referer': "https://www.sogou.com/",
                'sec-ch-ua-mobile': "?0",
                'Sec-Fetch-Dest': "document",
                'Sec-Fetch-Mode': "navigate",
                'Sec-Fetch-Site': "same-site",
                'Sec-Fetch-User': "?1",
                'Upgrade-Insecure-Requests': "1",
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
            }
            self.s = requests.session()
            ip = proxy_queue.get()
            proxies = {
                'http':f'http:{ip}',
                'https':f'https:{ip}'
            }
            self.s.proxies = proxies
            self.s.get('https://v.sogou.com/',headers=headers,timeout=3)

        except Exception as e:
            time.sleep(1)
            # log.logger.error(e)
            self.set_cookie()

    def requests_handler(self, domain):
        url = f'https://www.sogou.com/web?query=site%3A{domain}&_ast={str(time.time())[:10]}'
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'www.sogou.com',
        }

        try:
            response = self.s.get(url, headers=headers, timeout=2)
        except Exception as e:
            # log.logger.error(e)
            self.set_cookie()
            domain_list.put(domain)
            return None
        if response.status_code != 200:
            self.set_cookie()
            domain_list.put(domain)
            return None
            # return self.requests_handler(domain)

        if "seccodeImage" in response.text and "请输入图中的验证码" in response.text:
            self.set_cookie()
            domain_list.put(domain)
            return None

        else:
            return response

    def index(self):
        global ym_list
        self.s = requests.session()
        while not domain_list.empty():
            try:
                lock.acquire()  # 加锁
                domain = domain_list.get()
                lock.release()  # 释放锁
            except Exception as e:
                log.logger.error(e)
                break
            if domain in ym_list :
                log.logger.debug(f'队列剩余{domain_list.qsize()} {domain} 域名解析完毕已被收录 跳过')
                continue
            r = self.requests_handler(domain)
            if r == None:
                continue
            html = etree.HTML(r.text)
            # 数据量
            try:
                # 查询收录数量
                count_str = html.xpath('//p[@class="num-tips"]/text()')
                if count_str:
                    count = str("".join(re.findall(r'\d+', count_str[0])))
                else:
                    count = "0"
            except:
                log.logger.error('收录数查询出错')
                count_str = 0
                count = "0"
            if count == '0':
                log.logger.debug(f' 队列剩余{domain_list.qsize()} {domain}  域名解析完毕 {count_str}  已过滤')
                continue

            div_list = html.xpath('//div[@class="vrwrap"]')
            f = False
            sna_str = ''
            if div_list:
                for d in div_list:
                    try:
                        # 先判断在不在里面 如果在再深入对比
                        snapshot = d.xpath('./div[@class="citeurl"]//text()')
                        if snapshot == []:
                            snapshot = d.xpath('.//cite[contains(@id,"cacheresult_info")]//text()')
                        p = False
                        for y in paichu_list:
                            if y in ''.join(snapshot):
                                p = True
                                continue
                        if p == True:
                            log.logger.debug(f'队列剩余{domain_list.qsize()} {"".join(snapshot)} 域名在不合格文件中 pass')
                            continue

                        if len(domain.split('-')) >= 3:
                            parse_domain_str = ''.join(snapshot)
                            sna_str += parse_domain_str + ','
                            domain_s = '-'.join(domain.lower().split('-')[:2])
                            if domain_s in parse_domain_str:
                                f = True
                                break
                            else:
                                continue

                        else:
                            parse_domain_str = self.extract_domain(snapshot)
                            f = self.check_url(domain, parse_domain_str)
                            if f == False:
                                sna_str += parse_domain_str + ','
                                continue
                            else:
                                break
                    except Exception as e:
                        continue
            if f == False:
                log.logger.debug(f' 队列剩余{domain_list.qsize()} 此域名为：{domain} 查找到的域名为：{sna_str} 实际没有收录  已过滤 ')
                # log.logger.debug(f'{str(datetime.datetime.now())[:19]}  队列剩余{domain_list.qsize()} {domain} 实际没有收录  已过滤')
                continue
            if int(count) >= self.count:
                log.logger.debug(f'队列剩余{domain_list.qsize()} {domain} 域名解析完毕 搜索数{count}')
                with open(ym_file, 'a', encoding='utf-8') as f:
                    f.write(domain +','+str(count)+ '\n')
                ym_list.append(domain)

        log.logger.debug(f'退出线程  {domain_list.empty()}')

if __name__ == '__main__':
    proxy_queue = Queue()
    domain_list = Queue()
    lock = threading.Lock()

    # 初始化域名  存入队列
    file_name = "urls.txt"
    get_domain(file_name)
    #开启线程代理
    t = threading.Thread(target=get_proxies)
    t.start()


    # # 开启任务
    thread_list = []
    for i in range(eval(config['task_num'])):
        thread_list.append(threading.Thread(target=SoGou().index))
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()

