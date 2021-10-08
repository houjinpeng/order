import requests
import threading,queue
import time
from lxml import etree
import os
import re
try:
    with open('url.txt','r',encoding='utf-8') as fr:
        data = fr.readlines()
except Exception:
    data = []


# s = requests.session()

data_file = "./标题.csv"

# 写文件头
def write_hand():
    if os.path.exists(data_file):
        return
    with open(data_file, 'a',encoding='utf-8-sig') as file:
        file.write("id,地址,店铺名称,注册时间,运营天数,简介,销量,库存")
        file.write("\n")


write_hand()

def set_proxes():

    print('更换代理')
    s =  requests.session()
    ip = proxy_queue.get()
    proxies = {
        'http': f'http:{ip}',
        'https': f'http:{ip}'
    }
    s.proxies = proxies

    return s

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

def save_outurl(url):
    with open('outurl.txt','a',encoding='utf-8') as fw:
        fw.write(url+'\n')


def requests_handler(url,s):
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
            # 'User-Agent': UserAgent().chrome,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            # 'cookie':'gr_user_id=229c9ea0-79e0-4522-80a4-544744aba97f; t%5Ftuiguang1=bb%5F17; UM_distinctid=17c408dfd96407-0d6754a748bb2d-a7d173c-1fa400-17c408dfd972cc; _qddaz=QD.s8kovf.8jcnti.ku9nmbwp; tencentSig=9966901248; t%5Ftuiguang=jm%2Ecn; ASPSESSIONIDACTCQBQB=DFNKPGIALINGBPBPILPGICAO; IESESSION=alive; skinName=deepblue; Juming%2Ecom=t%5Fagent%5Ftuiguang=1&new%5Fbanban%5Fzhu=1; ASPSESSIONIDCCRCSAQB=NCDFKIHAGDCIBLCMLNLEGIFM; pgv_pvi=518071633231161623; fang%5Fcc%5Fgj=ok3; t%5Flaiyuan=263117%2Ejm%2Ecn; Hm_lvt_f94e107103e3c39e0665d52b6d4a93e7=1633239934,1633239935,1633239936,1633253894; Hm_lpvt_f94e107103e3c39e0665d52b6d4a93e7=1633253894; CNZZDATA3432862=cnzz_eid%3D36636905-1633167339-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1633244721; _qdda=3-1.3ljkun; _qddab=3-snyaxs.kub176er; _qddamta_4009972996=3-0; qqcrm-ta-set-uid-success&518071633231161623=1; first-set-uid-time=1633253894597'
        }

        try:
            response = s.get(url, headers=headers, timeout=5)
        except Exception as e:
            print(e)
            return None
        if response.text == '<script>window.location.href=\'/index.htm?\'+window.location.search.substring(1);</script>':
            return requests_handler(url,s)

        return response

def save_data(id,url,title,regist_time,yunxing_time,jianjie,sales,kucun):
    with open(data_file, 'a', encoding='utf-8-sig') as file:
        file.write(f'{id},{url},{title},{regist_time},{yunxing_time},{jianjie},{sales},{kucun}')
        file.write("\n")


def get_title():
    s = requests.session()
    while not url_queue.empty():
        url = url_queue.get()
        resp = requests_handler(url,s)
        if resp == None:
            url_queue.put(url)
            s = set_proxes()

            continue

        id = url.split('//')[1].split('.')[0]
        # if resp.text == '<script>window.location.href=\'/index.htm?\'+window.location.search.substring(1);</script>':
        #     title = '未开通店铺'
        #     save_data(id, url, title, '', '', '', '', '')
        #     save_outurl(url)
        #     print(url_queue.qsize(), id, url, title, '', '', '', '', '')
        #     continue
        #解析
        e = etree.HTML(resp.text)

        try:
            title = e.xpath('//title/text()')[0]
        except Exception as eroor:
            title = '未开通店铺'
            save_data(id, url, title, '', '', '', '', '')
            print(url_queue.qsize(),id, url, title, '', '', '', '', '')
            continue



        if title == '聚名网-到期域名查询抢注-域名注册-老域名买卖交易平台' or 'ERROR' in title:
            title = '未开通店铺'
            save_data(id, url, title, '', '', '', '', '')
            save_outurl(url)
            print(url_queue.qsize(), id, url, title, '', '', '', '', '')
            continue


        try:
            regist_time = e.xpath('//*[@id="container"]/div[1]/div[1]/div/ul/li[4]/text()')[0].replace('注册时间：','')
            yunxing_time = re.findall('\d+',e.xpath('//*[@id="container"]/div[1]/div[1]/div/ul/li[5]/text()')[0])[0]
        except Exception:
            regist_time = ''
            yunxing_time = ''
        try:
            jianjie = e.xpath('//div[@class="right"]//p/text()')[0].replace('\n','').replace(',','，')
        except Exception as e:
            jianjie = ''
        try:
            sales = e.xpath('//*[@id="container"]/div[1]/div[1]/div/ul/li[2]/a/text()')[0]
        except Exception as error:
            # print(error)
            sales = 0
        try:
            kucun = e.xpath('//font[@color="red"]/text()')[0][1:-1]
        except Exception:
            kucun = 0
        save_data(id,url,title.replace(',','，'),regist_time.replace(',','，'),yunxing_time,jianjie,sales,kucun)
        save_outurl(url)
        print(url_queue.qsize(),id,url,title,regist_time,yunxing_time,jianjie,sales,kucun)

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    proxy_queue = queue.Queue()
    url_queue = queue.Queue()

    d_list1 = [url.strip() for url in data]

    with open('outurl.txt', 'r', encoding='utf-8') as fr:
        data1 = fr.readlines()
    d_list2 = [url.strip() for url in data1]

    dif = set(d_list1).difference(set(d_list2))


    for d in dif:
        url_queue.put(d.strip())
    t = threading.Thread(target=get_proxies)
    t.start()
    t = []

    for i in range(100):
        t.append(threading.Thread(target=get_title))
    for i in t:
        i.start()
    for i in t:
        i.join()
    print('全部结束')
    # get_title()




