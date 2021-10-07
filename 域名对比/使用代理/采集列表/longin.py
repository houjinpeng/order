# @Time : 2021/5/15 16:18 
# @Author : HH
# @File : longin.py 
# @Software: PyCharm
# @explain:
import time

from verif_code import verif_api
import requests
import json



class Login():
    def __init__(self,data):
        self.data = data
        self.code_url = 'http://7a08c112cda6a063.juming.com/xcode'
        self.login_url = 'http://7a08c112cda6a063.juming.com/user_zh/p_login'
        self.s = requests.session()
        self.headers = {
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Content-Length': "67",
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
            'Host': "7a08c112cda6a063.juming.com:9696",
            'Origin': "http://7a08c112cda6a063.juming.com:9696",
            'Referer': "http://7a08c112cda6a063.juming.com:9696/ykj/",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
            'X-Requested-With': "XMLHttpRequest",
        }
        self.headers1 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
            'Host': "7a08c112cda6a063.juming.com:9696",
            'Upgrade-Insecure-Requests':'1',
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        }


    def get_code(self,file_path):
        r = self.s.get(self.code_url,headers=self.headers1)
        with open(file_path,'wb') as fw:
            fw.write(r.content)
        print('验证码下载完毕')

    def index(self):
        img_path = './code.jpg'
        self.get_code(img_path)

        result = verif_api(uname='15211731111', pwd='esb104', img=img_path, typeid=3)
        # result = '1234'
        data = self.data+result[0]
        r = self.s.post(self.login_url,data=data,headers=self.headers)
        a = json.loads(r.text)
        if a['msg'] =='登陆成功!':
            print('登录成功')
            return self.s
        else:
            print(a)
            time.sleep(1)
            return self.index()
if __name__ == '__main__':
    Login('re_mm=3b95c4dce56481ca634&re_yx=41000&re_yzm=').index()