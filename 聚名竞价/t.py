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

url = "http://www.chaicp.com/frontend_tools/getIcp"

payload={'url': 'baidu.com',
'token': '',
'csrf': response['data'],
'authenticate': '',
'sessionid': ''}
files=[

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

