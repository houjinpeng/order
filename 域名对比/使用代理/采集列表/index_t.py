# @Time : 2021/5/11 8:14 
# @Author : HH
# @File : index.py 
# @Software: PyCharm
# @explain:
# 41000 qq10086
# re_mm=cda83e9e3f5ff880a42&re_yx=ainimama%40163.com&re_yzm=cbem
# re_mm=cda83e9e3f5ff880a42&re_yx=ainibaba%40163.com&re_yzm=cbem
import time
from longin import Login
import configparser
import requests
from lxml import etree
import html
import json
import threading, queue

url = 'http://7a08c112cda6a063.juming.com:9696/ykj/'


class Juming():
    def __init__(self):
        open("./urls.txt", 'w').close()
        self.l = []
        # 筛选url
        self.ipQ = queue.Queue()
        self.page_q = queue.Queue()
        self.lock = threading.Lock()
        self.screen_url = 'http://7a08c112cda6a063.juming.com:9696/ykj/get_list'
        '''读写配置文件'''
        config = configparser.ConfigParser()
        # 文件路径
        logFile = r"./conf/setting.cfg"
        config.read(logFile, encoding="utf-8")
        self.config = config.defaults()
        self.task_num = self.config['task_num']
        self.s = Login('re_mm=3b95c4dce56481ca634&re_yx=41000&re_yzm=').index()
        # self.s = requests.session()

        self.headers = {
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Content-Length': "67",
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
            'Origin': "http://7a08c112cda6a063.juming.com:9696",
            'Referer': "http://7a08c112cda6a063.juming.com:9696/ykj/",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'X-Requested-With': "XMLHttpRequest",
            # 'cookie':'gr_user_id=689ea111-d505-4b82-92f6-737cc01162da; UM_distinctid=179c16c07fa2bc-07936ed58b1e1f-5771031-1fa400-179c16c07fca11; Hm_lvt_f94e107103e3c39e0665d52b6d4a93e7=1622447753; _uab_collina=162244775779338878005264; PHPSESSID=ehssqvhjrplmmn5jl3epg8dfmf; a801967fdbbbba8c_gr_session_id=9106c5f0-d12e-4ff6-ae1f-ccf8ed31a0e0; a801967fdbbbba8c_gr_session_id_9106c5f0-d12e-4ff6-ae1f-ccf8ed31a0e0=true; Juming_uid=41000; Juming_isapp=0; Juming_zhu=c92b61c9fc601815d36eeb9483e215a2; Juming_jf=cf4a9aa1d2e1a1187b5bed5829de86b0; Juming_qy=e34e5293670c74655223576471a7ffc1'
        }

    def save_out_ym(self, ym):
        try:
            with open('./conf/out_ym.txt', 'a', encoding='utf-8') as fw:
                fw.write(ym + '\n')
        except Exception:
            pass

    def save_domain(self, yu):
        # self.lock.acquire()
        with open('urls.txt', 'a', encoding='utf-8') as fw:
            fw.write(yu + '\n')
            fw.flush()
        # self.lock.release()

    def request_heandler(self, url, headers, method='get', page=1, s=requests.session()):

        if method == 'post':
            data = dict(self.config)
            kl = []
            for k, v in data.items():
                if k=='count' or k== 'time_num':
                    kl.append(k)
                if v == '0' or 'xq' in k or 'task' in k:
                    kl.append(k)
            [data.pop(k) for k in kl]
            data_str = ''
            for k, v in data.items():
                data_str = data_str + k + '=' + v + '&'
            data_str += f'psize=1000&page={page}'
            print(data_str)
            try:
                r = self.s.post(url, data=data_str, headers=headers, timeout=3)
                if r.status_code != 200:
                    return self.request_heandler(url, headers, method, page)
                elif '请求过于频繁'in json.loads(r.text)['html']:
                    return self.request_heandler(url, headers, method, page)
                # r = requests.post(url, data=data, headers=headers,timeout=3)
                return r
            except Exception:
                return self.request_heandler(url, headers, method, page)
        else:
            try:
                r = s.get(url, headers=headers, timeout=3)
                # r = self.s.get(url, headers=headers,timeout=3,proxies=proxies)
                return r
            except Exception:
                return self.request_heandler(url, headers, method, page)

    def parse_page(self, resp):
        html_str = json.loads(resp.text)['html']
        text = html.unescape(html_str)
        e = etree.HTML(text)
        nowpage = e.xpath("//strong[@class='pagenow']/text()")[0].split('，')[1].split('/')[1].replace('页', '')
        all_ym = e.xpath("//strong/text()")[0]
        # nowpage = 5
        print(f'本次共查询出{all_ym}条记录  共{nowpage}页')
        for i in  range(1, int(nowpage) + 1):
            self.page_q.put(i)


    def parse_domain_list(self, resp):
        html_str = json.loads(resp.text)['html']
        text = html.unescape(html_str)
        e = etree.HTML(text)
        all_data = e.xpath("//tr[contains(@id,'ymlist')]")
        # 解析列表
        ym_str = ''
        for data in all_data:
            try:
                ym = data.xpath(".//a[contains(@class,'a_ym')]/text()")[0]
            except Exception as e:
                print(1)
                continue
            ym_str += ym+'\n'
        self.save_domain(ym_str)

    # 2分钟检测一次前三页数据
    def check_domain(self):
        while True:
            for i in range(1, 3):
                r = self.request_heandler(self.screen_url, self.headers, method='post', page=1)
                self.parse_domain_list(r)
            time.sleep(20)

    def index(self):
        r = self.request_heandler(self.screen_url, self.headers, method='post')
        # 解析
        self.parse_page(r)
        t = []
        for i in range(5):
            t.append(threading.Thread(target=self.index_t))
        for j in t:
            j.start()
        for j in t:
            j.join()



    def main(self):
        check_t = threading.Thread(target=self.check_domain)
        check_t.start()

    def index_t(self):
        while not self.page_q.empty():
            i = self.page_q.get()
            # 发送请求
            r = self.request_heandler(self.screen_url, self.headers, method='post', page=i)
            self.parse_domain_list(r)


if __name__ == '__main__':

    Juming().index()
