import datetime
import logging
import time
import requests
import json
import threading
from lxml import etree
import re
import html
from tool.Proxy import Proxy
import random
proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}


class JvZi():

    def __init__(self):
        # self.proxy = Proxy()
        # threading.Thread(target=self.proxy.work).start()
        #
        # self.proxy_list = []
        # for i in range(30):
        #     self.proxy_list.append(self.proxy.get_proxies())

        with open('../conf/敏感词.txt', 'r', encoding='utf-8') as fr:
        # with open('./conf/敏感词.txt', 'r', encoding='utf-8') as fr:
            data = fr.readlines()
        self.word_list = []
        for d in data:
            self.word_list.append(d.strip())

    #获取总建站年龄
    def get_age(self, html):
        try:
            age = re.findall('(\d+)<span class="text-color-999"> ', html, re.S)[2]
            return age
        except Exception as e:
            return 0

    def get_tongyidu(self, html):
        try:
            tongyidu = re.findall('(\d+)<span class="text-color-999"> ', html, re.S)[1]
            return tongyidu+'%'
        except Exception as e:
            return '0%'

    def get_lianxu_cundang_time(self, html):
        try:
            max_lianxu = re.findall('(\d+)<span class="text-color-999"> ', html, re.S)[3]
            return max_lianxu
        except Exception as e:
            return 0

    # 对比敏感词
    def check_mingan(self, html):
        e = etree.HTML(html)
        all_tr = e.xpath('//table[@class="table table-bordered table-condensed table-striped table-hover"]')
        try:
            all_tr = all_tr[0].xpath('.//tr')
            word_list = []
            for tr in all_tr:
                w = ''.join(tr.xpath('.//div[@class="text-color-999 pull-left "]/text()'))
                if w != '':
                    word_list.append(w)
            for word in self.word_list:
                for title in word_list:
                    if word in title:
                        return word
            return '无'
        except Exception as error:
            return '无'


    # 近五年建站
    def get_five_year_num(self, html):
        try:
            five_year_num = re.findall('(\d+)<span class="text-color-999">/5 年 </span>', html, re.S)[0]
            return five_year_num
        except Exception as e:
            return 0

    # 连续5年建站
    def get_lianxu_five_year_num(self, html):

        try:
            lianxu_five_year_num = re.findall('(\d+)<span class="text-color-999">/5 年 </span>', html, re.S)[1]
            return lianxu_five_year_num
        except Exception as e:
            return 0

    def get_zh_title_num(self, html):
        e = etree.HTML(html)
        all_tr = e.xpath('//table[@class="table table-bordered table-condensed table-striped table-hover"]')
        num = 0
        old_year = 0
        try:
            all_tr = all_tr[0].xpath('.//tr')
            for tr in all_tr[1:]:
                year = ''.join(tr.xpath('.//td[2]/text()'))[:-4]
                if old_year != year:
                    old_year = year
                    w = ''.join(tr.xpath('.//span[@class="label label-success"]/text()'))
                    if w == '中文':
                        num += 1

            return num
        except Exception as error:
            return 0

        # 桔子自检敏感词

    def get_zijian_word(self, html_str):
        try:
            e = etree.HTML(html_str)
            span_all = e.xpath('/html/body/div[2]/div/div/div/div/div[2]/div[2]/div[3]/table/tbody/tr[3]/td/span/text()')
            word = '|'.join(span_all[1:])
            # word = re.findall('敏感词\(去重后\)：(.*?)"', html_str,re.S)[0]
            # word = html.unescape(word).replace(',', '|')
            return word
        except Exception as e:
            return '无'

    def check_proxy(self):
        if len(self.proxy_list) < 20:
            for i in range(30):
                self.proxy_list.append(self.proxy.get_proxies())

    def get_domain_url(self, domain,count=0):
        # self.check_proxy()
        # self.proxies = random.choice(self.proxy_list)
        url = "https://seo.juziseo.com/snapshot/history/"
        payload = f"post_hash=0ef479ae851d492123efbcc98ca80917&qr={domain}&qrtype=1&input_time=lastquery&start_time=&end_time=&fav=&history_score=0&lang=&age=0&title_precent=0&site_age=0&stable_count=0&stable_start_year_eq=&stable_start_year=&last_year_eq=&last_year=&site_5_age=0&site_5_stable_count=0&blocked=&gray=&gray_in_html=&site_gray=&baidu_site=0&gword=&has_snap=&per_page="
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-length': str(len(payload)),
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': 'juzufr=eJzLKCkpsNLXLy8v18sqrcosTs3XS87P1QcAZ9gIkQ%3D%3D; Hm_lvt_f87ce311d1eb4334ea957f57640e9d15=1650942544,1651458445; juz_Session=a56be4bab46m869juo5n3oisi3; juz_user_login=tb5oqZ8twzg%2FccksPbb0SYzGyBIAqTGSD4UbpK8Iy5OppN7hs5EaEyQojliNhgRh4zrX0dtRWpq8EO2vV7QaKx5yQRSCYIfan03IzYNBcgwhFEfFt7i5JNXWGybQ4A2qvclkPWSrQWwfxgSJ4C7%2FTQ%3D%3D; juzsnapshot=N; Hm_lpvt_f87ce311d1eb4334ea957f57640e9d15=1651543478',
            'origin': 'https://seo.juziseo.com',
            'pragma': 'no-cache',
            'referer': 'https://seo.juziseo.com/snapshot/history/id-__qr-eJzLKk3MS0vNS6%2FKSMxL10vOzwUAPrwG1A%3D%3D__qrtype-1__input_time-lastquery.html',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
        }
        try:
            # response = requests.request("POST", url, headers=headers, data=payload, proxies=self.proxies, allow_redirects=False,timeout=4)
            response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False,timeout=4)

            url = response.headers._store['location'][1]

            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'no-cache',
                'cookie': 'juzufr=eJzLKCkpsNLXLy8v18sqrcosTs3XS87P1QcAZ9gIkQ%3D%3D; Hm_lvt_f87ce311d1eb4334ea957f57640e9d15=1650942544,1651458445; juz_Session=a56be4bab46m869juo5n3oisi3; juz_user_login=tb5oqZ8twzg%2FccksPbb0SYzGyBIAqTGSD4UbpK8Iy5OppN7hs5EaEyQojliNhgRh4zrX0dtRWpq8EO2vV7QaKx5yQRSCYIfan03IzYNBcgwhFEfFt7i5JNXWGybQ4A2qvclkPWSrQWwfxgSJ4C7%2FTQ%3D%3D; juzsnapshot=N; Hm_lpvt_f87ce311d1eb4334ea957f57640e9d15=1651544979',
                'pragma': 'no-cache',
                'referer': 'https://seo.juziseo.com/snapshot/history/id-__qr-eJzLKk3MS0vNS6%2FKSMxL10vOzwUAPrwG1A%3D%3D__qrtype-1__input_time-lastquery.html',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
                'Content-Type': 'text/plain'
            }

            # r = requests.get(url, headers=headers, proxies=self.proxies,timeout=4)
            r = requests.get(url, headers=headers,timeout=4)
            e = etree.HTML(r.text)
            try:
                url = e.xpath('//td[@class="text-color-999 anchors_area"]/a/@href')[0]
            except Exception as e:
                return ''
            return 'https://seo.juziseo.com'+url
        except Exception as error:
            # try:
            #     self.proxy_list.remove(self.proxies)
            # except Exception:
            #     pass
            if count > 5:
                return None
            return self.get_domain_url(domain,count+1)

    def get_detail_html(self,domain,count=0):
        try:
            url = self.get_domain_url(domain)
            if url == '':
                return ''
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'no-cache',
                'cookie': 'juzufr=eJzLKCkpsNLXLy8v18sqrcosTs3XS87P1QcAZ9gIkQ%3D%3D; Hm_lvt_f87ce311d1eb4334ea957f57640e9d15=1650942544,1651458445; juz_Session=a56be4bab46m869juo5n3oisi3; juz_user_login=tb5oqZ8twzg%2FccksPbb0SYzGyBIAqTGSD4UbpK8Iy5OppN7hs5EaEyQojliNhgRh4zrX0dtRWpq8EO2vV7QaKx5yQRSCYIfan03IzYNBcgwhFEfFt7i5JNXWGybQ4A2qvclkPWSrQWwfxgSJ4C7%2FTQ%3D%3D; Hm_lpvt_f87ce311d1eb4334ea957f57640e9d15=1651460076; juz_Session=7k5jmnr1pu3ejevncr6mv447v1',
                'pragma': 'no-cache',
                'referer': 'https://seo.juziseo.com/snapshot/list/id-Y21WeVVFMXlXRUpCU0UxRE0waFZRekUzTHpCdmRFczVUMUU5UFE9PQ==.html',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
            }
            # self.check_proxy()
            # self.proxies = random.choice(self.proxy_list)

            # response = requests.get(url, headers=headers, timeout=3, proxies=self.proxies)
            response = requests.get(url, headers=headers, timeout=10)
            return response
        except Exception as e:
            if count > 5:
                return None

            # try:
            #     self.proxy_list.remove(self.proxies)
            # except Exception:
            #     pass
            # print(e)
            return self.get_detail_html(domain,count+1)


    def test(self):
        ds = ['juanfengzhang.com', 'baidu1.com', 'baidu2.com', 'baidu3.com', 'baidu4.com']
        # resp = self.get_token(ds)


        resp = self.get_detail_html(ds[0])

        '''
        1.域名用桔子查询历史并抓取历史中的标题 对比词库是否含有词库。
        2.提取桔子标题中 是中文的标题数量。注意每年只算一条。
        3.提取桔子中的总建站年数参数作为输出总建站年龄。
        4.提取桔子中的内容统一度参数作为统一度输出。
        5.提取桔子中的近5年历史参数作为近5年历史输出。
        6.提取桔子中的最长连续时间参数作为最长连续时间（年）输出。
        7.提取桔子中的近5年连续参数作为近5年连续输出。
        8.投射桔子当前域名的当前网址
        
        '''

        word = self.check_mingan(resp.text)
        print('关键词:',word)
        #   2.提取桔子标题中 是中文的标题数量。注意每年只算一条。
        zh_num = self.get_zh_title_num(resp.text)
        #自检敏感词
        zijian = self.get_zijian_word(resp.text)
        print('中文标题数量：',zh_num)
        # 3.提取桔子中的总建站年数参数作为输出总建站年龄。
        age = self.get_age(resp.text)
        print('建站中年龄:',age)
        # 4.提取桔子中的内容统一度参数作为统一度输出。
        tongyidu = self.get_tongyidu(resp.text)
        print('统一度：',tongyidu)
        #5.提取桔子中的近5年历史参数作为近5年历史输出。
        five_year_num = self.get_five_year_num(resp.text)
        print('近五年历史输出数：',five_year_num)
        # 6.提取桔子中的最长连续时间参数作为最长连续时间（年）输出。
        lianxu_cundang_time = self.get_lianxu_cundang_time(resp.text)
        print('最长连续时间（年）输出:',lianxu_cundang_time)
        # 7.提取桔子中的近5年连续参数作为近5年连续输出。
        lianxu_five_year_num = self.get_lianxu_five_year_num(resp.text)
        print('5年连续输出:',lianxu_five_year_num)
        # 8.投射桔子当前域名的当前网址
        url = resp.url
        print('详情网址：',url)



if __name__ == '__main__':
    ds = ['baidu1.com', 'baidu1.com', 'baidu2.com', 'baidu3.com', 'baidu4.com']

    JvZi().test()
    # for domain in ['baidu.com','baidu.com','baidu.com','baidu.com']:
    # get_history(ds)
