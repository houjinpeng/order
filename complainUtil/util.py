# @Time : 2021/4/22 9:30
# @Author : HH
# @File : util.py
# @Software: PyCharm
# @explain: 腾讯安全投诉中心自动化投诉脚本 https://urlsec.qq.com/report.html


import re
from slideVerfication import SlideVerificationCode
import threading,queue
import random
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
domain_done = list()
domain_init = list()

reason_init = list()

pattern = re.compile(
    r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
    r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
    r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
    r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
)

import configparser
'''读写配置文件'''
config = configparser.ConfigParser()
# 文件路径
logFile = r"./conf/setting.cfg"
config.read(logFile, encoding="utf-8")
config = config.defaults()
task = config.get('task')
def init_task_txt():
    global domain_done
    global domain_init
    global reason_init
    #初始化域名任务
    #处理完成的
    with open("./taskdata/urls_out.txt", "r", encoding="UTF-8") as f:
        rows = f.readlines()
        for row in rows:
            row = row.replace("\t", "").replace("\n", "").replace(" ", "")
            flag = True if pattern.match(row) else False
            if not flag:
                continue
            domain_done.append(row)

    #未处理url
    with open("./taskdata/urls.txt", "r", encoding="UTF-8") as f:
        rows = f.readlines()
        for row in rows:
            row = row.replace("\t", "").replace("\n", "").replace(" ", "")
            flag = True if pattern.match(row) else False
            if not flag:
                continue
            if row not in domain_done:
                domain_init.append(row)

    with open('./taskdata/liyou.txt','r',encoding='UTF-8') as f:
        rows = f.readlines()
        for row in rows:
            reason_init.append(row.strip())

    print(f'共有{len(domain_init)}条任务需要处理')
    return domain_init,reason_init

def build_email():
    email = ''
    for i in range(10):
        email += str(random.randint(1,10))
    return email[:11]+'@qq.com'


class Complain():
    def __init__(self,q):
        self.domain_init, self.reason_init = init_task_txt()
        self.q = q
    def get_chrome(self):
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])  # webdriver防检测
        option.add_argument("--no-sandbox")
        option.add_argument("--disable-dev-usage")
        # option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        # chrome_driver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        # driver = webdriver.Chrome(chrome_driver, chrome_options=option)
        desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        option.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=option)

    def open_url(self):
        self.driver.get('https://urlsec.qq.com/report.html')

    def send_data(self,url,reason,email):
        try:
            #往验证框中输入信息
            self.driver.find_element_by_id('url').clear()
            self.driver.find_element_by_id('url').send_keys(url)
            time.sleep(1)
            self.driver.find_element_by_id('reason').clear()
            self.driver.find_element_by_id('reason').send_keys(reason)
            time.sleep(1)
            self.driver.find_element_by_id('email').clear()
            self.driver.find_element_by_id('email').send_keys(email)
            time.sleep(1)

        except Exception as e:
            print('输入信息失败   %s'%e)

    def switch_frame_and_click(self):
        try:
            #切换fram并点击验证码
            self.driver.switch_to.frame(0)
            self.driver.find_element_by_id('tcaptcha_trigger_text_init').click()
            time.sleep(1)
            self.driver.switch_to.default_content()
            self.driver.switch_to_frame('tcaptcha_iframe')
        except Exception as e:
            print('切换iframe失败   %s'%e)

    def verif(self):
        # 创建一个滑动验证的对象
        sli = SlideVerificationCode()
        try:
            # 定位滑块图片
            slider_ele = self.driver.find_element_by_xpath('//*[@id="slideBg"]')
            # 定位验证码背景图
            background_ele = self.driver.find_element_by_xpath('//*[@id="slideBlock"]')
        except Exception as e:
            print('获取验证码图片和滑块图片错误   %s'%e)
            return False
        try:
            distance = sli.get_element_slide_distance(slider_ele, background_ele)
            # print("滑动的距离为：", distance)
            # 根据页面图片缩放比调整滑动距离
            distance = distance * 340 / 680 - 31
            #模拟滑动鼠标
            btn =self.driver.find_element_by_xpath('//*[@id="tcaptcha_drag_thumb"]')
            return sli.slide_verification(self.driver, btn, distance)
        except Exception as e:
            return False

    def click_button(self):
        try:
            self.driver.switch_to.default_content()
            self.driver.find_element_by_id('do').click()
            time.sleep(1)
            alert = self.driver.switch_to_alert()
            time.sleep(1)
            alert.dismiss()
            return True
        except Exception as e:
            print('提交失败   %s'%e)
            return False

    def save_succeed(self,url):
        #保存到成功的url文本中
        with open('./taskdata/urls_out.txt','a',encoding='utf-8') as fw:
            fw.write(url+'\n')

    def do(self,url):
        email = build_email()
        reason = random.choice(self.reason_init)
        self.send_data(url, reason, email)
        self.switch_frame_and_click()
        if self.verif():
            if self.click_button():
                self.save_succeed(url)
                print('%s 投诉完成' % url)

            return
        self.driver.switch_to.default_content()
        return self.do(url)

    def main(self):
        self.get_chrome()
        self.open_url()
        while not self.q.empty():
            url = self.q.get()
            self.do(url)
            print(f'剩余 {len(self.domain_init)}个')
            print('=='*20)
            time.sleep(1)



if __name__ == '__main__':
    q = queue.Queue()
    # Complain().run()
    domain_init,reason_init = init_task_txt()

    for url in domain_init:
        q.put(url)


    def startpro():
        t = []
        for i in range(int(3)):
            t.append(threading.Thread(target=Complain(q).main))
        for i in t:
            i.start()
    # init_task_txt()
    # build_email()
    startpro()