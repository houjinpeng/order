# @Time : 2021/4/30 8:42 
# @Author : HH
# @File : 数美滑块验证码.py 
# @Software: PyCharm
# @explain:
"""
数美滑块验证码破解验证
"""

import base64
import json
import random
import re
import time
from io import BytesIO
from urllib.parse import quote

import cv2
import numpy as np
import requests
from pyDes import des, ECB

CAPTCHA_DISPLAY_WIDTH = 310
CAPTCHA_DISPLAY_HEIGHT = 155

p = {}


def risk(act, rid):
    sm = int(time.time() * 1000)

    url = "https://captcha.fengkongcloud.com/ca/v1/fverify?" \
          "organization=RlokQwRlVjUrTUlkIqOg&appId=default&channel=miniProgram&lang=zh-cn&" \
          "rversion=1.0.1&sdkver=1.1.1&rid=" + str(rid) + "&act=" + str(
        act) + "&ostype=weapp&data={}&callback=sm_" + str(sm)

    headers = {
        "Host": "captcha.fengkongcloud.com",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501",
        # 'User-Agent': 'Mozilla/5.0 (Windows NT {0}.0; Win64; x64) AppleWebKit/{1} (KHTML, like Gecko) Chrome/89.0.{2}.82 Safari/{3}'.format(
        #     str(random.randint(5, 10)), str(random.uniform(500, 600))[:6],
        #     str(random.randint(4000, 4999)), str(random.uniform(500, 600))[:6]
        # ),
        "content-type": "application/json",
        "Referer": "https://servicewechat.com/wxb296433268a1c654/21/page-frame.html",
        "Accept-Encoding": "gzip, deflate, br"
    }

    resp = requests.get(url=url, headers=headers)
    print(resp.text)
    return resp.text
    # return resp.text
    # if resp.text.find("REJECT")<0:
    #
    #     data = self.fe_api(rid)
    #     global end
    #     end = False
    #
    #     return data
    # else:
    #     return "{'code': 0, 'success': False, 'data': {'passed': False, 'message': '滑块匹配不成功！'}}"


def get_random_ge(distance):
    """
    生成随机的轨迹
    {
        "d":0.85,"m":"","c":"总耗时","w":372,"h":186,"os":"weapp","cs":0,"wd":0,"sm":1
    }
    """
    length = random.choice(np.arange(8, 12))
    avge = int(distance / length)

    difference = int(distance - avge * length)

    tracks = [avge] * length
    randomFlag = 0
    for i in range(length):
        if randomFlag:
            tracks[random.randint(0, length - 1)] += randomFlag
            randomFlag = 0
        if random.choice([False, True]):
            if tracks[i] > 1:
                randomFlag = random.randint(1, tracks[i])
            else:
                randomFlag = random.randint(tracks[i], 1)

            tracks[i] -= randomFlag
    if randomFlag:
        tracks[random.randint(0, length - 1)] += randomFlag
    luck = random.randint(0, length - 1)
    # 补全损失值
    tracks[luck] = tracks[luck] + difference

    tracksList = []
    tracksList.append([0, 0, 0])
    moveCount = 101
    for index in range(len(tracks)):
        if index != 0:
            tracks[index] = tracks[index] + tracks[index - 1]
            tracksList.append([tracks[index], 0, 0 + moveCount])
        else:
            tracksList.append([tracks[index], 0, 0 + moveCount])
        moveCount += 100

    data = {
        "d": distance / 372,
        "m": tracksList,
        "c": tracksList[-1][-1] + 56,
        "w": 372,
        "h": 186,
        "os": "weapp",
        "cs": 0,
        "wd": 0,
        "sm": 1
    }

    return data


def des_encrypt(KEY, s):
    """
    DES 加密
    :param s: 原始字符串
    :return: 7EOyuZ7kb3MZps/Gtq2uRymiMUC0T1e5IwtmDbfyiFQ=
    """
    k = des(KEY, ECB)
    length = 8
    count = len(s)
    if count < length:
        add = (length - count)
        text = s + ("\0" * add)
    elif count > length:
        add = (length - (count % length))
        text = s + ("\0" * add)
    en = k.encrypt(text)
    return base64.b64encode(en).decode()


def des_decrypt(secret_key, s):
    """
    DES 解密
    :param secret_key:
    :param s:
    :return:
    """
    k = des(secret_key, ECB)
    data = k.decrypt(s)
    return data


def get_distance(fg, bg):
    """
    计算滑动距离
    """
    target = cv2.imdecode(np.asarray(bytearray(fg.read()), dtype=np.uint8), 0)
    template = cv2.imdecode(np.asarray(bytearray(bg.read()), dtype=np.uint8), 0)
    result = cv2.matchTemplate(target, template, cv2.TM_CCORR_NORMED)
    _, distance = np.unravel_index(result.argmax(), result.shape)
    return distance


def conf_captcha(organization):
    """
    获取验证码设置
    """
    url = 'https://captcha.fengkongcloud.com/ca/v1/conf'

    args = {
        'organization': organization,
        'model': 'slide',
        'sdkver': '1.1.3',
        'rversion': '1.0.3',
        'appId': 'default',
        'lang': 'zh-cn',
        'channel': 'DEFAULT',
        'callback': 'sm_{}'.format(int(time.time() * 1000))
    }

    r = requests.get(url, params=args, verify=False)
    resp = json.loads(re.search(r'{}\((.*)\)'.format(args['callback']), r.text).group(1))
    return resp


def register_captcha(organization):
    """
    注册验证码
    """
    url = 'https://captcha.fengkongcloud.com/ca/v1/register'

    args = {
        'organization': organization,
        'channel': 'YingYongBao',
        'lang': 'zh-cn',
        'model': 'slide',
        'appId': 'default',
        'sdkver': '1.1.3',
        'data': '{}',
        'rversion': '1.0.3',
        'callback': 'sm_{}'.format(int(time.time() * 1000))
    }

    r = requests.get(url, params=args, verify=False)
    resp = json.loads(re.search(r'{}\((.*)\)'.format(args['callback']), r.text).group(1))

    return resp


def verify_captcha(rid, act):
    """
    提交验证
    """

    sm = int(time.time() * 1000)
    # url = 'https://captcha.fengkongcloud.com/ca/v2/fverify'
    url = "https://captcha.fengkongcloud.com/ca/v1/fverify?" \
          "organization=RlokQwRlVjUrTUlkIqOg&appId=default&channel=miniProgram&lang=zh-cn&" \
          "rversion=1.0.1&sdkver=1.1.1&rid=" + str(rid) + "&uv=" + str(
        act) + "&ostype=weapp&data={}&callback=sm_" + str(sm)

    headers = {
        "Host": "captcha.fengkongcloud.com",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501",
        # 'User-Agent': 'Mozilla/5.0 (Windows NT {0}.0; Win64; x64) AppleWebKit/{1} (KHTML, like Gecko) Chrome/89.0.{2}.82 Safari/{3}'.format(
        #     str(random.randint(5, 10)), str(random.uniform(500, 600))[:6],
        #     str(random.randint(4000, 4999)), str(random.uniform(500, 600))[:6]
        # ),
        "content-type": "application/json",
        "Referer": "https://servicewechat.com/wxb296433268a1c654/21/page-frame.html",
        "Accept-Encoding": "gzip, deflate, br"
    }

    resp = requests.get(url=url, headers=headers)
    print(resp.text)
    return resp


def get_verify(organization):
    """
    进行验证
    """
    resp = register_captcha(organization)

    rid = resp['detail']['rid']
    key = resp['detail']['k']

    domain = resp['detail']['domains'][0]
    fg_uri = resp['detail']['fg']
    bg_uri = resp['detail']['bg']

    fg_url = ''.join(['http://', domain, fg_uri])
    bg_url = ''.join(['http://', domain, bg_uri])

    r = requests.get(fg_url, verify=False)
    fg = BytesIO(r.content)

    r = requests.get(bg_url, verify=False)
    bg = BytesIO(r.content)

    distance = get_distance(fg, bg)
    distance = int(distance * (372 / 600))
    print(distance)

    k = des_decrypt("sshummei", base64.b64decode(key))[:8].decode()
    ge = get_random_ge(distance)
    paramData = des_encrypt(k, json.dumps(ge))
    act = quote(paramData, safe='')
    risk1 = risk(act, rid)


def test():
    # 表示小红书
    organization = 'RlokQwRlVjUrTUlkIqOg'

    # rid是验证过程中响应的标示，r是最后提交验证返回的响应
    get_verify(organization)

    # riskLevel为PASS说明验证通过
    # if r['riskLevel'] == 'PASS':
    #     # 这里需要向小红书提交rid
    #     # 具体可抓包查看，接口：/api/sns/v1/system_service/slide_captcha_check
    #     pass


if __name__ == '__main__':
    test()
