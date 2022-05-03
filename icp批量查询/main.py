import requests
from lxml import etree
import json
import time
import queue,threading
import ddddocr
import logging
import os
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(levelname)s - %(lineno)d - %(message)s')
logger = logging.getLogger(__name__)
ocr = ddddocr.DdddOcr()


save_num = 0
class ICP():
    def __init__(self,code_name):
        self.code_name = code_name
        self.s = requests.session()
        self.search_url = 'http://www.chaicp.com/home_cha/p_piliang'
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'www.chaicp.com',
            'Origin': 'http://www.chaicp.com',
            'Pragma': 'no-cache',
            'Referer': 'http://www.chaicp.com/piliang.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }


    def get_cookie(self):
        try:
            # logger.info('获取cookie')
            payload = "ym=lw-tea.com%0D%0Ady861.com%0D%0Atongchuangzhoucheng.com%0D%0Ajarvis-ai.cn%0D%0Ashunlicc.com%0D%0Aszztkji.com%0D%0Apowerliftglobal.com%0D%0Ampcq6.com%0D%0A1yf21h.cn%0D%0Ainq5th.cn%0D%0Afuyoudzsw.com%0D%0Ahzjnkj.cn%0D%0Apfq8.com%0D%0Aqqdoy.com%0D%0Aoret-cn.cn%0D%0Adl-xdsm.com&code=ccdb"
            r = self.s.post(self.search_url, headers=self.headers, data=payload, timeout=3)
        except Exception as e:
            return self.get_cookie()

    def get_img(self):
        try:
            img_url = f'http://www.chaicp.com/home_cha/getcode/nocache={int(time.time() * 1000)}'
            headers = {
                'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Host': 'www.chaicp.com',
                'Pragma': 'no-cache',
                'Referer': 'http://www.chaicp.com/piliang.html',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
                'Content-Type': 'application/json'
            }
            r = self.s.get(img_url, headers=headers, timeout=10)
            with open(self.code_name, 'wb') as fw:
                fw.write(r.content)
            # logger.info('验证码保存完毕')
            return True
        except Exception as e:
            return None

    def save(self):
        global save_num
        while True:
            if save_queue.empty():
                time.sleep(2)
                continue
            while not save_queue.empty():
                with open('备案.csv', 'a', encoding='utf-8') as fw:
                    icp_list = save_queue.get()
                    fw.write(','.join(icp_list))
                    fw.write('\n')
                    save_num += 1
                    logger.info(f'已保存：{save_num} 保存完毕 {icp_list[0]}')

    def get_data(self, ym_list):
        try:
            f = self.get_img()
            if f == None:
                return None
            with open(self.code_name, 'rb') as f:
                img_bytes = f.read()
            code = ocr.classification(img_bytes)
            os.remove(self.code_name)
            data = {
                'ym': ''.join(ym_list),
                'code': code

            }
            r = self.s.post(self.search_url, headers=self.headers, data=data, timeout=60)

            try:
                if '执行sql错误，请重试' in r.text:
                    logger.info('sql 错误 重试')
                    return self.get_data(ym_list)
                j = json.loads(r.text)
                if j['msg'] == '验证码错误':
                    return self.get_data(ym_list)
                logger.info(j)
            except Exception as e:
                return r
        except Exception as e:
            logger.info(e)
            return self.get_data(ym_list)

    def parse_icp(self, resp):
        e = etree.HTML(resp.text)
        try:
            all_icp = e.xpath('//div[@class="query-con"]//tr')
        except Exception :
            return None
        if len(all_icp) <= 1:
            return None
        for icp in all_icp[1:]:
            icp_list = []

            icp_list.append(icp.xpath('./td')[4].attrib.get('title'))
            icp_list.append(icp.xpath('.//td//text()')[0])
            icp_list.append(icp.xpath('.//td//text()')[1])
            icp_list.append(icp.xpath('.//td//text()')[2])
            icp_list.append(icp.xpath('.//td//text()')[3])
            icp_list.append(icp.xpath('.//td//text()')[4])
            try:
                icp_list.append(icp.xpath('.//td//text()')[5])
            except Exception as error:
                icp_list.append(' ')
            save_queue.put(icp_list)
            # logger.info(f'保存备案数量 {save_queue.qsize()}')
        return True




    def index(self):
        self.get_cookie()
        while not domain_quque.empty():
            ym = domain_quque.get()
            logger.info(f'剩余任务：{domain_quque.qsize()} 放入查询列表')
            resp = self.get_data(ym)
            if resp == None:
                domain_quque.put(ym)
                continue
            f1 = self.parse_icp(resp)
            if f1 == None:
                domain_quque.put(ym)
                continue

            logger.info(f'剩余任务:{domain_quque.qsize()}')




if __name__ == '__main__':
    if os.path.exists('备案.csv') == False:
        with open('备案.csv','a',encoding='utf-8') as fw:
            fw.write('域名,主办单位名称,单位性质,网站备案/许可证号,网站名称,网站首页网址,审核时间'+'\n')
        fw.close()
    with open('备案.csv', 'r', encoding='utf-8') as fr:
        data_str = fr.read()

    save_queue = queue.Queue()
    # threading.Thread(target=ICP('').save).start()
    domain_quque = queue.Queue()
    with open('历史存在.txt', 'r', encoding='utf-8') as fr:
        domain_list = fr.readlines()
    ls = []
    for ym in domain_list:
        if ym.strip() in data_str:
            continue
        ls.append(ym)
        if len(ls) == 100:
            domain_quque.put(ls.copy())
            ls.clear()
    if len(ls)!= 0:
        domain_quque.put(ls.copy())
        ls.clear()
    threading.Thread(target=ICP('').save).start()
    t = []
    for i in range(20):
        t.append(threading.Thread(target=ICP(f'code{i}.png').index))
    for j in t:
        j.start()
    for j in t:
        j.join()
    logger.info('全部完成')
    # ICP().index()
    # ICP('').save()
