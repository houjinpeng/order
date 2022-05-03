import os
import time

from tool.JvZi import JvZi
from tool.JvCha import JvCha
from tool.Proxy import Proxy
import threading, queue


# 写头文件

def wirte_hand():
    str = '域名,聚查查灰,总建站年数,中文条数,统一度,近5年历史,近5年连续,最长连续时间（年）,页面,桔子查灰,桔子自检灰,总建站年数,中文条数,统一度,近5年历史,近5年连续,最长连续时间（年）,页面'
    if os.path.exists('深度查灰.csv') == False:
        with open('深度查灰.csv', 'a', encoding='utf-8') as fw:
            fw.write(str + '\n')
        fw.close()


class ShenduChahun():
    def __init__(self):
        self.jvcha = JvCha()
        self.jvzi = JvZi()
        threading.Thread(target=self.save).start()
        threading.Thread(target=self.save_out).start()

    def save_out(self):
        while True:
            if save_out_queue.empty():
                time.sleep(2)
            ym = save_out_queue.get()
            try:
                with open('./conf/out_url.txt', 'a', encoding='utf-8') as fw:
                    fw.write(ym)
                    fw.write('\n')
            except Exception as e:
                pass

    def save(self):
        while True:
            if save_queue.empty():
                time.sleep(2)
            data = save_queue.get()
            data = [str(d) for d in data]
            try:

                with open('深度查灰.csv','a',encoding='utf-8') as fw:
                    fw.write(','.join(data))
                    fw.write('\n')
            except Exception as e:
                pass


    def work(self):
        while not domain_queue.empty():
            domain_token = domain_queue.get()
            print(f'剩余任务：{domain_queue.qsize()} 任务域名：{domain_token["ym"]}')
            result_list = []
            # 聚查
            #域名
            result_list.append(domain_token['ym'])
            #获取聚查网历史数据化
            history_data = self.jvcha.get_history(domain_token)
            #聚查查灰
            result_list.append(self.jvcha.check_mingan(history_data))
            #总建站年数
            result_list.append(self.jvcha.get_age(domain_token))
            #中文条数
            result_list.append(self.jvcha.get_zh_title_num(history_data))
            #统一度
            result_list.append(self.jvcha.get_tongyidu(history_data))
            # 近5年历史
            result_list.append(self.jvcha.get_five_year_num(history_data))
            #近5年连续
            result_list.append(self.jvcha.get_lianxu_cundang_time(history_data,5))
            #最长连续时间
            result_list.append(self.jvcha.get_lianxu_cundang_time(history_data))
            #页面
            result_list.append('http://www.jucha.com/lishi/'+domain_token['ym'])

            #####################################################################################
            resp = self.jvzi.get_detail_html(domain_token['ym'])
            if resp == None:
                domain_queue.put(domain_token)
                print(resp)
                continue
            elif resp == '':
                continue
            # 桔子查灰
            result_list.append(self.jvzi.check_mingan(resp.text))
            #桔子自检灰
            result_list.append(self.jvzi.get_zijian_word(resp.text))
            #总建站年数
            result_list.append(self.jvzi.get_age(resp.text))
            #中文条数
            result_list.append(self.jvzi.get_zh_title_num(resp.text))
            #统一度
            result_list.append(self.jvzi.get_tongyidu(resp.text))
            #近5年历史
            result_list.append(self.jvzi.get_five_year_num(resp.text))
            #近5年连续
            result_list.append(self.jvzi.get_lianxu_five_year_num(resp.text))
            #最长连续时间
            result_list.append(self.jvzi.get_lianxu_cundang_time(resp.text))
            #页面
            result_list.append(resp.url)

            #保存
            save_queue.put(result_list)
            save_out_queue.put(domain_token['ym'])

    def index(self):
        t = []
        for i in range(50):
            t.append(threading.Thread(target=self.work))
        for j in t:
            j.start()
        for j in t:
            j.join()
        print('任务全部完成')

if __name__ == '__main__':
    jvcha = JvCha()
    domain_queue = queue.Queue()
    save_queue = queue.Queue()
    save_out_queue = queue.Queue()
    domain_list = []
    ls = []
    # 初始化
    try:
        with open('./conf/urls.txt', 'r', encoding='utf-8') as fr:
            data = fr.readlines()
        for d in data:
            domain_list.append(d.strip())
    except Exception:
        pass

    try:
        with open('./conf/out_url.txt', 'r', encoding='utf-8') as fr:
            data = fr.readlines()
        out_list = [d.strip() for d in data]
    except Exception as e:
        out_list = []


    #把聚查token初始化
    for domain in domain_list:
        if domain in out_list:
            continue
        if len(ls) >= 2000:
            token_list = jvcha.get_token(ls)
            for token in token_list:
                domain_queue.put(token)
            ls.clear()
            continue
        else:
            ls.append(domain)
    if len(ls) != 0:
        token_list = jvcha.get_token(ls)
        for token in token_list:
            domain_queue.put(token)
        ls.clear()

    #写表格头
    wirte_hand()

    ShenduChahun().index()
