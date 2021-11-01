import json
import time
from email_tools import get_email_code,get_email
import requests
from selenium import webdriver
from slideVerfication import SlideVerificationCode



class Regiset():
    def __init__(self):
        self.url = 'https://account.sogou.com/home/signin?redirect_type=reg_email&ru=http://zhanzhang.sogou.com&client_id=1119'

    def save_account(self,emali,password):
        with open('搜狗站长账号.txt','a',encoding='utf-8') as fw:
            fw.write(f'{emali}----{password}\n')

    def main(self):
        #打开浏览器
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')  # # 浏览器不提供可视化页面
        chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速,GPU加速可能会导致Chrome出现黑屏，且CPU占用
        # chrome = webdriver.Chrome(chrome_options=chrome_options)
        chrome = webdriver.Chrome()
        while True:
            try:
                chrome.get(self.url)
                time.sleep(2)
                email = get_email()
                email = json.loads(email.text)
                # print(email['data']['fullMailAddress'])
                zhanghao = email['data']['fullMailAddress']
                password = 'qwer1234'

                #输入邮箱
                chrome.find_element_by_xpath('//*[@id="app"]/div/div[3]/div/div[1]/div[3]/div/label/input').send_keys(zhanghao)
                #输入密码
                chrome.find_element_by_xpath('//*[@id="app"]/div/div[3]/div/div[1]/div[4]/div/label/input').send_keys(password)
                time.sleep(1)
                #点击获取验证码
                chrome.find_element_by_xpath('//*[@id="app"]/div/div[3]/div/div[1]/div[5]/div/button').click()
                time.sleep(3)
                #过验证码他图片
                sli = SlideVerificationCode()
                # 切换到验证码所在的iframe
                chrome.switch_to.frame(chrome.find_element_by_xpath('//*[@id="tcaptcha_iframe"]'))
                # 定位滑块图片
                slider_ele = chrome.find_element_by_xpath('//*[@id="slideBlock"]')
                # 定位验证码背景图
                background_ele = chrome.find_element_by_xpath('//*[@id="slideBg"]')
                distance = sli.get_element_slide_distance(slider_ele, background_ele)
                # print("滑动的距离为：", distance)
                # 根据页面图片缩放比调整滑动距离
                distance = distance * 280 / 680+10
                # 6.3模拟滑动鼠标
                btn = chrome.find_element_by_xpath('//*[@id="tcaptcha_drag_thumb"]')
                is_pass = sli.slide_verification(chrome, btn, distance)

                if is_pass == True:
                    # 获取验证码  输入验证码
                    code = get_email_code(email['data']['id'])
                    chrome.find_element_by_xpath('//*[@id="app"]/div/div[3]/div/div[1]/div[5]/div/label/input').send_keys(code)
                    #点击同意
                    chrome.find_element_by_xpath('//*[@id="app"]/div/div[3]/div/div[1]/div[6]/label/span[1]/input').click()
                    time.sleep(1)
                    #点击注册
                    # try:
                    #     if chrome.find_element_by_xpath('//*[@id="app"]/div/div[3]/div/div[1]/div[7]/button').get_attribute('disabled') == 'true':
                    #         continue
                    # except Exception as e:
                    #     continue

                    chrome.find_element_by_xpath('//*[@id="app"]/div/div[3]/div/div[1]/div[7]/button').click()
                    time.sleep(1)
                    if chrome.current_url == 'https://zhanzhang.sogou.com/':
                        print(f'注册成功 账号：{zhanghao} 密码：{password}')
                        print('=='*20)
                        self.save_account(zhanghao,password)

            except Exception as e:
                print(e)


if __name__ == '__main__':
    Regiset().main()