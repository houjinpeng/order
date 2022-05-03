import time

import requests
import os
import threading,queue
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(levelname)s - %(lineno)d - %(message)s')
logger = logging.getLogger(__name__)


class ICPChaicp():
    def __init__(self):
        self.s = requests.session()

    def save_domain(self):
        while True:
            if save_queue.empty():
                time.sleep(1)
            icp_list = save_queue.get()
            try:
                with open('备案.csv', 'a', encoding='utf-8') as fw:
                    fw.write(','.join(icp_list))
                    fw.write('\n')
            except Exception as e:
                pass

    def save_out_domain(self):
        while True:
            if out_queue.empty():
                time.sleep(1)
            domain = out_queue.get()
            try:
                with open('out.txt', 'a', encoding='utf-8') as fw:
                    fw.write(domain)
                    fw.write('\n')
            except Exception as e:
                pass

    def get_csrf(self,domain):
        try:
            url = "http://www.chaicp.com/frontend_tools/getCsrf"

            payload = f"ym={domain}\r\n"
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Content-Length': '12',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'www.chaicp.com',
                'Origin': 'http://www.chaicp.com',
                'Pragma': 'no-cache',
                'Referer': 'http://www.chaicp.com/icp/baidu.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }

            response = self.s.request("POST", url, headers=headers, data=payload).json()
            return response
        except Exception as e:
            self.s = requests.session()
            return self.get_csrf(domain)

    def get_icp(self,domain,token,response,authenticate,sessionid):
        try:
            url = "http://www.chaicp.com/frontend_tools/getIcp"

            payload = {'url': domain,
                       'token': token,
                       'csrf': response['data'],
                       'authenticate': authenticate,
                       'sessionid': sessionid}

            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'www.chaicp.com',
                'Origin': 'http://www.chaicp.com',
                'Pragma': 'no-cache',
                'Referer': 'http://www.chaicp.com/icp/baidu.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }

            response = self.s.request("POST", url, headers=headers, data=payload).json()
            if response['code'] == 1:
                return response
            token = self.get_token()
            if token == '请更新token池':
                return None
            csrf = self.get_csrf(domain)
            return self.get_icp(domain,token['token'],csrf,token['auth'],token['session'])

        except Exception as e:
            print(e)
            return self.get_icp(domain,token,response,authenticate,sessionid)

    def get_token(self):
        try:
            url='http://127.0.0.1:5001/get_token'
            r = requests.get(url).json()
            return r
        except Exception as e:
            time.sleep(5)
            return self.get_token()



    def index(self):
        while not domain_quque.empty():
            domain = domain_quque.get()

            csrf = self.get_csrf(domain)
            data = self.get_icp(domain,'',csrf,'','')
            if data == None:
                domain_quque.put(domain)
                continue

            # 域名, 主办单位名称, 单位性质, 网站备案 / 许可证号, 网站名称, 网站首页网址, 审核时间
            if data['msg'] == '未备案':
                logger.info(f'剩余任务：{domain_quque.qsize()}  {domain} 未备案')
                out_queue.put(domain)
                continue
            else:


                data = [domain,data['data']['mc'],data['data']['lx'],data['data']['bah'],data['data']['bam'],data['data']['sy'],data['data']['sj']]
                data = ['' if d == None else d for d in data]
                out_queue.put(domain)
                save_queue.put(data)
                logger.info(f'剩余任务：{domain_quque.qsize()}  {domain} 保存备案')



if __name__ == '__main__':
    save_queue = queue.Queue()
    out_queue = queue.Queue()
    domain_quque = queue.Queue()

    if os.path.exists('备案.csv') == False:
        with open('备案.csv','a',encoding='utf-8') as fw:
            fw.write('域名,主办单位名称,单位性质,网站备案/许可证号,网站名称,网站首页网址,审核时间'+'\n')
        fw.close()
    try:
        with open('out.txt', 'r', encoding='utf-8') as fr:
            out_list = fr.readlines()
    except Exception :
        out_list = []

    out_list = [i.strip() for i in out_list]

    with open('历史存在.txt', 'r', encoding='utf-8') as fr:
        domain_list = fr.readlines()

    for ym in domain_list:
        if ym.strip() in out_list:
            continue
        domain_quque.put(ym.strip())

    threading.Thread(target=ICPChaicp().save_domain).start()
    threading.Thread(target=ICPChaicp().save_out_domain).start()

    t = []
    for i in range(50):
        t.append(threading.Thread(target= ICPChaicp().index))
    for j in t:
        j.start()
    for j in t:
        j.join()
    logger.info('全部完成')