#先登录
import requests
import re
import json
from tool.longin import Login

s, msg = Login().login('104038','qq123123')
cookie = 'PHPSESSID='+s.cookies._cookies['7a08c112cda6a063.juming.com']['/']['PHPSESSID'].value
id = '85201112'
#获取价格
payload = f"id%5B%5D={id}"
headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Accept-Encoding': 'gzip, deflate',
  'Accept-Language': 'zh-CN,zh;q=0.9',
  'Cache-Control': 'no-cache',
  'Connection': 'keep-alive',
  'Content-Length': '17',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': cookie,
  'Host': '7a08c112cda6a063.juming.com:9696',
  'Origin': 'http://7a08c112cda6a063.juming.com:9696',
  'Pragma': 'no-cache',
  'Referer': 'http://7a08c112cda6a063.juming.com:9696/ykj/39963828/',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.3'
}
url = "http://7a08c112cda6a063.juming.com:9696/ykj/shopcar"
response = requests.request("POST", url, headers=headers, data=payload)
token = re.findall("var token='(.*?)'", response.text)[0]
id = re.findall('"id":"(\d+?)"', response.text)[0]
jq = re.findall('"qian":"(\d+?)"', response.text)[0]

print(f'价格为:{jq}   token：{token}  id为：{id}')
###########################################################################

#获取token
url = "http://7a08c112cda6a063.juming.com:9696/main/if_mmbh?r=1"

payload={}
headers = {
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Accept-Encoding': 'gzip, deflate',
  'Accept-Language': 'zh-CN,zh;q=0.9',
  'Cache-Control': 'no-cache',
  'Connection': 'keep-alive',
  'Cookie': cookie,
  'Host': '7a08c112cda6a063.juming.com:9696',
  'Pragma': 'no-cache',
  'Referer': 'http://7a08c112cda6a063.juming.com:9696/ykj/shopcar',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
  'X-Requested-With': 'XMLHttpReques'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(json.loads(response.text))
if json.loads(response.text)['code'] != 1:
#######################################################
    #获取验证码
    url = "http://7a08c112cda6a063.juming.com:9696/xcode?1648645870411"

    headers = {
      'Cookie': cookie,
      'Content-Type': 'text/plain'
    }

    response = requests.request("GET", url, headers=headers,)
    with open('code.png', 'wb') as fw:
        fw.write(response.content)
    #############################################################################


    #解除保护
    url = "http://7a08c112cda6a063.juming.com:9696/user_baohu/close_baohu"

    payload={'csrf_token': token,
    'mmbhda': '爱慧慧',
    'pass': 'qq123123',
    're_yzm':input('输入验证码')
             }

    headers = {
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'Accept-Encoding': 'gzip, deflate',
      'Accept-Language': 'zh-CN,zh;q=0.9',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'Cookie': cookie,
      'Host': '7a08c112cda6a063.juming.com:9696',
      'Origin': 'http://7a08c112cda6a063.juming.com:9696',
      'Pragma': 'no-cache',
      'Referer': 'http://7a08c112cda6a063.juming.com:9696/ykj/shopcar',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
      'X-Requested-With': 'XMLHttpReques'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(json.loads(response.text))

####################################################
# 下单


url = "http://7a08c112cda6a063.juming.com:9696/ykj/buy"

payload = f"id={id}&jg={jq}&hdbj=&t=&csrf_token={token}"
headers = {
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Accept-Encoding': 'gzip, deflate',
  'Accept-Language': 'zh-CN,zh;q=0.9',
  'Cache-Control': 'no-cache',
  'Connection': 'keep-alive',
  'Content-Length': str(len(payload)),
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Cookie': cookie,
  'Host': '7a08c112cda6a063.juming.com:9696',
  'Origin': 'http://7a08c112cda6a063.juming.com:9696',
  'Pragma': 'no-cache',
  'Referer': 'http://7a08c112cda6a063.juming.com:9696/ykj/shopcar',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
  'X-Requested-With': 'XMLHttpRequest'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(json.loads(response.text))
print(1)