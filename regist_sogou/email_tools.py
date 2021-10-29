import requests
import json
import re
email_url = "https://www.suiyongsuiqi.com/api/zh/getRandomMail"
email_code_url = "https://www.suiyongsuiqi.com/api/zh/getMail2"
s = requests.Session()
requests.packages.urllib3.disable_warnings()

headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-length': '25',
    'content-type': 'application/json',
    'origin': 'https://www.suiyongsuiqi.com',
    'referer': 'https://www.suiyongsuiqi.com/zh/mail/',
    'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}
proxies = {
    "http": "http://user-sp68470966:maiyuan312@gate.dc.visitxiangtan.com:20000",
    "https": "http://user-sp68470966:maiyuan312@gate.dc.visitxiangtan.com:20000",
}


def get_email():
    try:
        data = {"suffix": "suiyongsuiqi"}
        response = s.post(email_url, headers=headers, json=data, verify=False, proxies=proxies)
        return response
    except Exception as e:
        return get_email()


def get_email_code(id):
    try:
        global s
        data = {"mails": [0,id], "ids": [0]}
        response = s.post(email_code_url, headers=headers, json=data, verify=False, proxies=proxies)
        code = re.findall('<h1>(\d+?)</h1>',response.text)[0]
        s = requests.Session()
        return code
    except Exception as e:
        return get_email_code(id)


if __name__ == '__main__':
    email_data = get_email()
    data = json.loads(email_data.text)
    print(data['data']['fullMailAddress'])
    print('发送验证码')
    code = get_email_code(data['data']['id'])
    print(code)