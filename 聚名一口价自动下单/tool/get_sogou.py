import requests
import re
from lxml import etree
import threading, queue
import time

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


class GetSougouRecord():

    def __init__(self):
        threading.Thread(target=get_proxies).start()
        ip = proxy_queue.get()
        self.proxies = {
            'http': f'http://{ip}',
            'https': f'http://{ip}'
        }

    def set_proxies(self):
        ip = proxy_queue.get()
        self.proxies = {
            'http': f'http://{ip}',
            'https': f'http://{ip}'
        }

    def request_hearders(self,url):
        try:

            # proxies = {
            #     "http": "http://user-sp68470966:maiyuan312@gate.dc.visitxiangtan.com:20000",
            #     "https": "http://user-sp68470966:maiyuan312@gate.dc.visitxiangtan.com:20000",
            # }
            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'}
            r = requests.get(url,headers=headers,timeout=5,proxies=self.proxies)
            if '需要您协助验证' in r.text:
                self.set_proxies()
                return self.request_hearders(url)
            return r
        except :
            self.set_proxies()
            return self.request_hearders(url)


    def check_sogou(self,domain,record_count,time_str):
        url = f'https://www.sogou.com/web?query=site%3A{domain}'
        r = self.request_hearders(url)
        e = etree.HTML(r.text)
        is_kuaizhao = False
        try:
            if record_count == '':
                return True
            # 查询收录数
            record = re.findall('搜狗已为您找到约(.*?)条相关结果', r.text)[0].replace(',', '')
            if record == '0':
                return False
            # 查询
            all_domain = e.xpath('//div[contains(@class,"citeurl")]')
            fuhe_count = 0
            for domain_obj in all_domain:
                if domain in ''.join(domain_obj.xpath('.//text()')):
                    fuhe_count += 1
                    #判断是否包好快照字符串
                    if time_str == '':
                        is_kuaizhao = True
                    else:
                        for t in time_str.split(','):
                            if t in ''.join(domain_obj.xpath('.//text()')):
                                is_kuaizhao = True


            #判断设置大于条数  如果大于5
            n = re.findall('(\d+)',record_count)[0]

            if int(n) > 5:
                if fuhe_count >= 5 and eval(str(record) + record_count):
                   pass

                else:
                    return False

            else:

                if eval(str(fuhe_count) + record_count):
                   pass
                else:
                    return False


            return is_kuaizhao

        except:
            return False


if __name__ == '__main__':
    s = '>=50'
    tim_str = '小时,1天,2天'
    r = GetSougouRecord().check_sogou('aksqamu.com',s,tim_str)
    print(r)
    r = GetSougouRecord().check_sogou('worrywater.com',s,tim_str)
    print(r)
