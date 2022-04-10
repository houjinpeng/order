# @Time : 2021/4/22 8:19 
# @Author : HH
# @File : move_mouse.py 
# @Software: PyCharm
# @explain: 模拟鼠标移动
import random
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import configparser
'''读写配置文件'''
config = configparser.ConfigParser()
# 文件路径
logFile = r"./conf/juming.cfg"
config.read(logFile, encoding="utf-8")
config = config.defaults()
tokennum = config.get('tokennum')
ip = config.get('ip')


p = 'C:\Program Files\Google\Chrome\Application'

def get_slide_locus(distance):
    """
    根据移动坐标位置构造移动轨迹,前期移动慢，中期块，后期慢
    :param distance:移动距离
    :type:int
    :return:移动轨迹
    :rtype:list
    """
    remaining_dist = distance
    locus = []
    while remaining_dist > 0:
        ratio = remaining_dist / distance
        if ratio < 0.2:
            # 开始阶段移动较慢
            span = random.randint(170, 190)
        elif ratio > 0.8:
            # 结束阶段移动较慢
            span = random.randint(160, 179)
        else:
            # 中间部分移动快
            span = random.randint(200, 320)
        locus.append(span)
        remaining_dist -= span
    return locus

def get_chrome():
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])  # webdriver防检测
    option.add_argument("--no-sandbox")
    option.add_argument("--disable-dev-usage")
    option.add_argument('--headless')
    option.add_argument('--disable-gpu')
    # option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # chrome_driver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    # driver = webdriver.Chrome(chrome_driver, chrome_options=option)
    desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
    desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
    option.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(executable_path='./chromedriver.exe',chrome_options=option)
    return driver

def move():
    driver = get_chrome()
    url =f'http://{ip}:5001/get_token_page'
    driver.get(url)
    i = 0
    while i <= int(tokennum):
        try:
            time.sleep(2)
            # 获取滑块
            button = driver.find_element_by_xpath('//*[@id="nc_1__scale_text"]')
            # 滑动滑块
            ActionChains(driver).click_and_hold(button).perform()
            #获取滑块轨迹
            # locus = get_slide_locus(500)
            ActionChains(driver).move_by_offset(xoffset=100, yoffset=random.randint(-5, 5)).perform()
            ActionChains(driver).move_by_offset(xoffset=200, yoffset=random.randint(-5, 5)).perform()
            # for l in locus:
            #     print(l)
            #     ActionChains(driver).move_by_offset(xoffset=l, yoffset=random.randint(-5, 5)).perform()
            #
            #     ActionChains(driver).context_click(button)
            i += 1

            print(f'==============={i}===================')
            # ActionChains(driver).release().perform()
        except Exception as e:
            driver.get(url)

if __name__ == '__main__':

    move()