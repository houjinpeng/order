
import random
import threading
import time
from lxml import etree
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import configparser



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
    option.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(executable_path='chromedriver.exe',chrome_options=option)
    return driver

def move():
    driver = get_chrome()
    url =f'http://127.0.0.1:5001/get_token_page'
    driver.get(url)
    while True:
        try:
            # 获取滑块
            button = driver.find_element_by_xpath('//*[@id="nc_1__scale_text"]')
            # 滑动滑块
            ActionChains(driver).click_and_hold(button).perform()
            #获取滑块轨迹
            # locus = get_slide_locus(500)
            ActionChains(driver).move_by_offset(xoffset=100, yoffset=random.randint(-5, 5)).perform()
            ActionChains(driver).move_by_offset(xoffset=30, yoffset=random.randint(-5, 5)).perform()
            ActionChains(driver).move_by_offset(xoffset=170, yoffset=random.randint(-5, 5)).perform()
            time.sleep(1)

        except Exception as e:
            driver.get(url)
            time.sleep(2)


if __name__ == '__main__':
    t = []
    for i in range(10):
        t.append(threading.Thread(target=move))
    for j in t:
        j.start()
    for j in t:
        j.join()
