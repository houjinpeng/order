# coding:utf-8
from pyquery import PyQuery as pq
from threading import Thread
import concurrent.futures
import configparser
import requests
import time

import json
import csv

'''读写配置文件'''
config = configparser.ConfigParser()
# 文件路径
logFile = r"./conf/juming.cfg"
config.read(logFile, encoding="utf-8")
config = config.defaults()
task = config.get('task')
ip = config.get('ip')

# 重试次数
pr_retry = config.get('pr_retry')




def fail_domain(data):
    if data.get('domain') != None:
        with open("./taskdata/fail_url.txt", "a+", encoding="UTF-8-sig") as f:
            f.write(f"{data.get('domain')}\n")


class juming:
    def __init__(self):
        self.session = requests.Session()
        self.result = dict()

    def reslut(self,result):
        global write_cnt
        global failed_cnt
        global i
        print(i)
        i += 1
        if result:
            if result['succeed']:
                result.pop('succeed')
                write_cnt += 1
                print(f'{time.strftime("%Y-%m-%d %H:%M:%S")} (Juming{task.capitalize()})成功完成域名: {write_cnt} {result}')
            else:
                failed_cnt += 1
                fail_domain(result)
                print('失败 %s' % result)
                if failed_cnt % 100 == 0:
                    # print(f"失败: ----------------------   {result}")
                    print(f'{time.strftime("%Y-%m-%d %H:%M:%S")} (Juming{task.capitalize()}) 失败: {failed_cnt}')

    def query_domain(self, items, retry: int = 0):
        '''
        查询域名
        :return:
        '''
        while True:
            try:
                task = items.split('-')[-1]
                params = (
                    ('target', task),
                )
                # 获取 token
                # time.sleep(1)
                try:
                    flask_result = requests.get(f'http://{ip}:5001/juming', params=params, timeout=3)
                except Exception:
                    return
                if flask_result.status_code == 200:
                    self.flask_result = flask_result.json()
                else:
                    print('状态码   %s'%flask_result.status_code)
                # 判断接口是否有 domain 跟 token
                if self.flask_result.get('domain') == '' and self.flask_result.get('token') == '':
                    time.sleep(10)
                    continue


                if self.flask_result.get('nums') == '' or self.flask_result.get('nums') == None:
                    if retry < 5:
                        return self.query_domain(items, retry + 1)
                    else:
                        # return self.query_domain(items, retry + 1)
                        self.result['succeed'] = False
                        self.result['msg'] = "domain | token 获取失败"
                        print("domain | token 获取失败")
                        self.reslut(self.result)

                        # return self.result

                self.result['domain'] = self.flask_result.get('domain')
                params = (
                    ('target', task),
                    ('token', self.flask_result.get('token')),
                    ('domain', self.flask_result.get('domain')),
                )

                data = {
                    'info': self.query_info(),
                    'detail': self.query_detail(),
                }

                if data.get("info") != False or data.get("detail") != False:
                    requests.post(f'http://{ip}:5001/return', json=data, params=params)
                    self.result['succeed'] = True
                    # return self.result
                else:
                    self.result['succeed'] = False
                    print('这里错了1 %s '%data)
                    # return self.result

            except Exception as ex:
                if retry < 5:
                    return self.query_domain(items, retry + 1)
                else:
                    self.result['succeed'] = False
                    self.result['msg'] = f"domain_info {ex}"
                    # print(f"query_domain {ex}")
                    # return self.result

    def query_info(self, retry: int = 0):
        '''
        获取 info 参数
        :param retry:
        :return:
        '''
        try:
            data = {
                'ym': self.flask_result.get('domain'),
                'token': self.flask_result.get('token')
            }
            url = f"http://47.56.160.68:1000{self.flask_result.get('nums')}/api.php"
            response = self.session.post(url=url, data=data, verify=False, timeout=3)
            domain_status = response.json().get('code')
            if domain_status != 1:
                if retry < 2:
                    return self.query_info(retry + 1)
                else:
                    return False
            return response.json()
        except:
            if retry < 2:
                return self.query_info(retry + 1)
            else:
                return False

    def query_detail(self, retry: int = 0):
        '''
        获取 detail 参数
        :param retry:
        :return:
        '''
        try:

            headers = {
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Proxy-Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'http://47.56.160.68:81',
                'Host': '47.56.160.68:81',
            }

            data = {
                'ym': self.flask_result.get('domain'),
                'xq': 'y',
                'page': '1',
                'limit': '20',
                'token': self.flask_result.get('token'),
                'group': '1',
                'nian': ''
            }
            response_detail = self.session.post('http://47.56.160.68:81/api.php', data=data, verify=False,
                                                headers=headers, timeout=3)
            # print(f"{self.flask_result.get('domain')} {response_detail.json()}")
            self.data = {
                'ym': self.flask_result.get('domain'),
                'xq': 'y',
                'token': self.flask_result.get('token'),
                'group': '1',
                'page': '1',
                'limit': '20',
                'nian': ''
            }
            self.data_sj = []
            # with concurrent.futures.ThreadPoolExecutor(max_workers=len(response_detail.json().get('data'))) as executor:
            #     futures = [executor.submit(self.query_domain_histoy, item) for item in response_detail.json().get('data')]
            self.query_domain_histoy()
            r = response_detail.json()
            if self.data_sj != []:
                results = {
                    "count": r.get('count'),
                    "data": self.data_sj,
                    "code": r.get('code'),
                    "msg": r.get('msg'),
                }
            else:
                results = {
                    "count": r.get('count'),
                    "data": response_detail.json().get('data'),
                    "code": r.get('code'),
                    "msg": r.get('msg'),
                }
            if r.get('code') != 1:
                if retry < 2:
                    return self.query_detail(retry + 1)
                else:
                    return False
            print(results)
            return results
        except:
            if retry < 2:
                return self.query_detail(retry + 1)
            else:
                return False

    def query_domain_histoy(self):
        headers = {
            'Host': '47.56.160.68:81',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://47.56.160.68:81',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
        }
        # self.data['sj'] = datas.get('timestamp')
        try:
            response_detail_sj = self.session.post('http://47.56.160.68:81/api.php', data=self.data, verify=False,
                                               headers=headers, timeout=3)
        except Exception as e:
            return
        for i in response_detail_sj.json().get('data'):
            self.data_sj.append(i)


if __name__ == '__main__':

    failed_cnt = 0  # 查询失败数
    write_cnt = 0  # 查询成功数

    i = 0
    # 多线程, 根据配置文件运行爬虫
    def run(task, retry: int = 0):
        try:
            global failed_cnt
            global write_cnt
            global i
            data_list = list()
            # 获取总共需查询多少域名
            domain_lists = requests.get(f'http://{ip}:5001')
            html = pq(domain_lists.text)
            domain_lists.close()
            task_list = ''
            perform = ""  # 已处理域名数量
            thread_num = ''
            if task == "history":
                thread_num = config.get('history_task_num')
                # 未完成域名总数量
                task_list = html('tr[id=history] td:nth-child(5)').text()
                perform = html('tr[id=history] td:nth-child(6)').text()
            if int(task_list) == 0:
                time.sleep(2)
                return
            # 需要处理的域名数量
            hand = abs(int(task_list) - int(perform))
            data_list = [i for i in range(hand)]
            t_list = []
            for i in range(int(thread_num)):
                t_list.append(Thread(target=juming().query_domain,args=( f"{i}-{task}",)))
            for t in t_list:
                t.start()
            for t in t_list:
                t.join()


        except Exception as ex:
            time.sleep(3)
            return

    run('history')
