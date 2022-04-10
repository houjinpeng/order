import threading,queue
import time
import requests
import json
import re

url = "https://domainapi.aliyun.com/onsale/search?fetchSearchTotal=true&token=tdomain-aliyun-com:K5nO1XSMcNdt6ckLWcwdz7EgKMJkFyHC&" \
      "currentPage={}" \
      "&pageSize=200" \
      "&suffix={}" \
      "&searchIntro=false&keywordAsPrefix=false&keywordAsSuffix=false&exKeywordAsPrefix=false&exKeywordAsSuffix=false&exKeywordAsPrefix2=false&exKeywordAsSuffix2=false&callback=jQuery111305720677395599363_1647934618402&_=1647934618407" \
      "&minPrice={}" \
      "&maxPrice={}" \
      "&minDomainAvailDay={}" \
      "&maxDomainAvailDay={}"

headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'cookie': 'cna=qdzKGblpvQACAQG9jV2oLIoe; login_aliyunid_pk=1273981073708433; aliyun_site=CN; currentRegionId=cn-hongkong; aliyun_choice=CN; JSESSIONID=ZL766781-VLUY32NC5N68OCN9RYWQ3-RJ1ZP11L-428E; _s0=eNrz4A12DQ729PeL9%2FV3cfUxiK3OTLFSivIxNzMztzDUDfMJjTQ28nM29TOz8Hf2swyKDA801g3yMowKMDT00TUxsnBV0kkusTI0MzG3NDYxM7QwNjDVSUxGEjAxMtXJrbAytDAwqI0CAHaiHJI%3D; tfstk=cJi1BO41m1f1tXLVbA9ebu3m2yUPZ8X7hFNiCqkALtFyWxD1iojzN7OjosE4HJ1..; l=eBI1q8hcgJNU7-JMKO5CFurza77TrIRbzsPzaNbMiInca6tFBepVBNCn57iMvdtjgtfcleKrzU4ZdRFy-pzKgTMSZD2qaj_kbxJw-; isg=BJCQWXE3xio6i5lz0EgG-u3QYd7iWXSj3fyRXYphkOujxTJvM2h9M94znY0lFSx7; JSESSIONID=5H666591-VLUYU91Q56L5S41ACW282-VMPRT11L-BDKE; _s0=eNrz4A12DQ729PeL9%2FV3cfUxiK3OTLFSivIxNzMztzDUDfMJjTQ28nM29TOz8Hf2swyKDA801g3yMowKMDT00TUxsnBV0kkusTI0MzG3NDYxM7QwNjDVSUyGCViampibG%2BvkVlgZWhgY1EYBAHcjHJs%3D',
    'pragma': 'no-cache',
    'referer': 'https://mi.aliyun.com/',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
}

domain_list = []
class crawl_domain():

    def save_doamin(self):
        while True:
            try:
                domain = domain_queue.get(timeout=500)
            except Exception as e:
                return
            with open('url.txt','a',encoding='utf-8') as fw:
                fw.write(domain+'\n')
            # print(domain)

    def work(self,suffix):
        # for price in self.price_list:
        f = True
        min = min_price
        max = 10
        add_price = 10
        while f:
            if max > max_price:
                return
            for page in range(1, 26):
                print(f'后缀为：{suffix} 抓取价格为：{min}-{max} 第{page}页')
                url_c = url.format(page, suffix, min, max,minDomainAvailDay,maxDomainAvailDay)
                try:
                    response = requests.request("GET", url_c, headers=headers)
                    data = json.loads(re.findall('jQuery111305720677395599363_1647934618402\((.*?)\);', response.text)[0])
                    if page == 1 and data.get('data') == None and max > max_price:
                        f = False
                        break
                    if data.get('data') == None:
                        min = max + 1
                        max = max + add_price
                        print('换下个价格')
                        break
                    if data['data']['searchTotal']> 5000:
                        max = int(max*0.9)
                        if min >= max:
                            min = max-5
                        print(f"总数量:{data['data']['searchTotal']}   超过5000 缩小搜索范围 搜索价格缩小为：{max}")
                        break

                    if page == 25 and data.get('data') != None:
                        min = max + 1
                        max = max + add_price

                    for domain in data.get('data')['pageResult']['data']:
                        d = domain['domainName']
                        if d not in domain_list:
                            domain_queue.put(d)
                            domain_list.append(d)

                except Exception as e:
                    print(e)

    def index(self):
        t = []


        for suffix in suffix_list:
            t.append(threading.Thread(target=self.work,args=(suffix,)))
        for i in t:
            i.start()

        s = threading.Thread(target=self.save_doamin)
        s.start()
        for i in t:
            i.join()




if __name__ == '__main__':
    #最大金额 最小金额
    min_price = 1
    max_price = 300
    #可用天数
    minDomainAvailDay = 180
    maxDomainAvailDay = 500
    # 'xin', 'com.cn', 'net', 'com.cn', 'vip', 'top', 'cc', 'shop', 'club', 'wang'   可选
    #后缀
    # 'com.cn', 'com',
    suffix_list = ['com.cn', 'com','cn']
    domain_queue = queue.Queue()

    crawl_domain().index()
    print('抓取完成')
    print(f'抓取域名个数：{len(domain_list)}')
    time.sleep(60*60)
