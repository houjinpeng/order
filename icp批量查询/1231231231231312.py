import time
import re
import requests
import json

s = requests.session()
url = "http://www.chaicp.com/frontend_tools/getCsrf"

payload = "ym=baidu.com\r\n"
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

response = s.request("POST", url, headers=headers, data=payload).json()
print(response)
url = "http://www.chaicp.com/frontend_tools/getIcp"

payload = {'url': 'baidu.com',
           'token': '',
           'csrf': response['data'],
           'authenticate': '',
           'sessionid': ''}
files = [

]
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

response = s.request("POST", url, headers=headers, data=payload, files=files).json()

print(response)
###########################################################################################################

###获取验证码

headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'referer': 'http://www.chaicp.com/',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Content-Type': 'text/plain'
}

t = f'CF_APP_1:{int(time.time() * 1000)}:0.2110128067666588',

url = "http://www.chaicp.com/frontend_tools/getCsrf"

payload = "ym=baidu.com\r\n"
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

response = s.request("POST", url, headers=headers, data=payload).json()
print(response)

url = "http://www.chaicp.com/frontend_tools/getIcp"
payload = {
    'url': 'baidu.com',
    # 'token': t,
    'token': input('请输入token:'),
    'csrf': response['data'],
    'authenticate': input('请输入authenticate:'),
    # 'authenticate': d['result']['value'],
    # 'sessionid': d['result']['csessionid']}
    'sessionid':  input('请输入authenticate:')
}
files = [

]
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

response = s.request("POST", url, headers=headers, data=payload, files=files).json()

print(response)


#####################################################################################
for i in range(100):
    for domain in ['taobao.com','maiyuan.com','jd.com']:
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

        response = s.request("POST", url, headers=headers, data=payload).json()
        url = "http://www.chaicp.com/frontend_tools/getIcp"

        payload = {'url': domain,
                   'token': '',
                   'csrf': response['data'],
                   'authenticate': '',
                   'sessionid': ''}
        files = [

        ]
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

        response = s.request("POST", url, headers=headers, data=payload, files=files).json()

        print(response)
