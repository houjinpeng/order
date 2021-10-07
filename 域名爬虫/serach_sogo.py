import logging,random,time,re,requests,threading
from lxml import etree
from urllib.parse import quote
from fake_useragent import UserAgent
from queue import Queue
cookie_queue = Queue()
words_queue = Queue()


logging.basicConfig(level = logging.INFO,format = '%(asctime)s -line:%(lineno)d - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_words():
    with open('conf/words.txt','r',encoding='utf-8') as fr:
        data = fr.readlines()
    for d in data:
        if d.strip() != '':
            words_queue.put(d.strip())

session_list = []
def get_cookies():
    global session_list
    urlList = ['https://v.sogou.com/']

    headers = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Connection': "keep-alive",
        'Host': "v.sogou.com",
        'Referer': "https://mingyi.sogou.com/",
        'sec-ch-ua-mobile': "?0",
        'Sec-Fetch-Dest': "document",
        'Sec-Fetch-Mode': "navigate",
        'Sec-Fetch-Site': "same-site",
        'Sec-Fetch-User': "?1",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",

    }
    while True:
        if cookie_queue.qsize() >2:
            time.sleep(1)
            continue
        s = requests.session()
        s.get(random.choice(urlList), headers=headers)
        try:
            cookie_dict = s.cookies._cookies['.sogou.com']['/']
            cookie_tmp = ''
            for key, value in cookie_dict.items():
                if key=='IPLOC':
                    continue
                cookie_tmp += key + '=' + value.value + ';'
            if cookie_tmp[:-1] in session_list:
                continue
            print(f'添加cookie 当前cookie数：{cookie_queue.qsize()}')
            cookie_queue.put(cookie_tmp[:-1])
            session_list.append(cookie_tmp[:-1])
        except Exception:
            time.sleep(1)
            pass

class SoGou():
    def __init__(self):
        self.ua = UserAgent().chrome

    def check_reg(self,ym):
        url = 'http://panda.www.net.cn/cgi-bin/check.cgi?area_domain=' +ym
        try:
            r = requests.get(url,headers={'user-agent':UserAgent().chrome})
            if '亲~人太多，被挤爆了' in r.text:
                logger.info('亲~人太多，被挤爆了 等会在来 ')
                return self.check_reg(ym)
            else:
                if 'Domain name is available' in r.text:
                    return True
                else:
                    return False
        except Exception as e:
            logger.info(e)

    def extract_domain(self,ym_str):
        domain_str = ''.join(ym_str)
        if 'http' in domain_str:
            domain_str = re.compile(r'(htt.*)').search(domain_str).group()
            ym = re.search(r"(?<=http[s]://)[.\w-]*(:\d{,8})?((?=/)|(?!/))", domain_str).group()
        else:
            pattern = re.compile(r'(.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+.?')
            try:
                ym = pattern.search(domain_str).group()
                ym = ym.split('/')[0].strip()
            except Exception:
                ym = ''
        if len(ym.split('.')) <= 1:
            return None
        else:
            return '.'.join(ym.split('.')[-2:])


    def set_cookie(self):
        try:
            old = self.cookie
            self.ua = UserAgent().chrome
            self.s = requests.session()
            self.cookie = cookie_queue.get()
            print(f'切换cookie 剩余cookie：{cookie_queue.qsize()}')
            time.sleep(random.randint(1, 5))
        except Exception as e:
            time.sleep(2)
            return self.set_cookie()

    def requests_handler(self, url, count):
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.ua,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'www.sogou.com',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'cookie': self.cookie
        }

        try:
            response = self.s.get(url, headers=headers, timeout=2)
        except Exception as e:
            print(f'此ip请求失败 ')
            return self.requests_handler(url, count + 1)
        html_doc = response.text.encode(response.encoding).decode('utf-8')
        if "seccodeImage" in html_doc and "请输入图中的验证码" in html_doc:
            # print(f"出现验证码 {self.cookie}")

            if count > 2:
                # time.sleep(random.random())
                self.set_cookie()
                # self.get_sunid(self.cookie)
                return self.requests_handler(url, 0)

            return self.requests_handler(url, count + 1)
        else:
            return response

    def check_ym(self,ym):
        try:
            r = requests.get('http://'+ym,headers={'user-agent':UserAgent().chrome},timeout=3)
            if r.status_code == 404:
                return True
            else:
                return False
        except Exception as e:
            return True

    def index(self):
        global ym_list
        ym_list = []
        self.cookie = cookie_queue.get()
        self.s = requests.session()
        while not words_queue.empty():
            try:
                lock.acquire()  # 加锁
                word = words_queue.get()
                lock.release()  # 释放锁
            except Exception:
                break
            url = f'https://www.sogou.com/web?query={quote(word)}&_ast={str(time.time())[:10]}&_asf=www.sogou.com&cid=&s_from=result_up&ie=utf8'
            while True:
                r = self.requests_handler(url,0)
                html = etree.HTML(r.text.replace(",", "").replace("\n", "").replace("\r", ""))
                div_list = html.xpath('//div[@class="vrwrap"]')
                f = False
                if div_list:
                    for d in div_list:
                        try:
                            # 先判断在不在里面 如果在再深入对比
                            snapshot = d.xpath('./div[@class="citeurl"]//text()')
                            if snapshot == []:
                                snapshot = d.xpath('.//cite[contains(@id,"cacheresult_info")]//text()')
                            if snapshot == []:
                                continue
                            parse_domain_str = self.extract_domain(snapshot) #获取到的域名
                            if parse_domain_str in ym_list:
                                continue
                            if  parse_domain_str == None or  parse_domain_str.find('.') == -1 or parse_domain_str[-1] == '.' or parse_domain_str[-1] == '-' or parse_domain_str.find(' ') != -1:
                                continue
                            logger.info(f'关键词{word}  域名：{parse_domain_str}')
                            f = self.check_ym(parse_domain_str)
                            ym_list.append(parse_domain_str)
                            if f == True:
                                if self.check_reg(parse_domain_str):
                                    logger.info(f'关键词{word} 未注册：{parse_domain_str}')
                                    with open(file_name,'a',encoding='utf-8') as fw:
                                        fw.write(parse_domain_str+'\n')

                        except Exception as e:
                            continue

                url = re.findall('id="sogou_next" href=\"(.*?)"',r.text)
                if url == []:
                    break
                url = 'https://www.sogou.com/web'+url[0]


        print(f'退出线程  {domain_list.empty()}')


if __name__ == '__main__':
    proxy_queue = Queue()
    domain_list = Queue()
    lock = threading.Lock()

    # 初始化域名  存入队列
    file_name = "./conf/ym.txt"
    # get_domain(file_name)
    get_words()
    cookie_t = []
    for i in range(1):
        cookie_t.append(threading.Thread(target=get_cookies))
    for t in cookie_t:
        t.start()

    # 开启任务
    thread_list = []
    for i in range(1):
        thread_list.append(threading.Thread(target=SoGou().index))
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()

