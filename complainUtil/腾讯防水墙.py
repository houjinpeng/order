# @Time : 2021/5/6 9:46 
# @Author : HH
# @File : 腾讯防水墙.js.py
# @Software: PyCharm
# @explain:
import execjs
import base64
import json
import random
import re
from aes import AEScoder
import cv2
import numpy as np
import os
import requests
import time
headers = {
    'Accept': "*/*",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Connection': "keep-alive",
    'Host': "t.captcha.qq.com",
    'Referer': "https://urlsec.qq.com/",
    'sec-ch-ua-mobile': "?0",
    'Sec-Fetch-Dest': "script",
    'Sec-Fetch-Mode': "no-cors",
    'Sec-Fetch-Site': "same-site",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    }

s = requests.session()
def _init_slider():
    """
    初始化图片验证码
    :return:
    """
    data_dict = {}
    url = 'https://t.captcha.qq.com/cap_union_prehandle?aid=2046626881&captype=4&curenv=inner&protocol=https&clientype=2&disturblevel=1&apptype=1&noheader=1&color=&showtype=point&fb=1&theme=&lang=zh-CN&ua=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzg5LjAuNDM4OS45MCBTYWZhcmkvNTM3LjM2&enableDarkMode=0&grayscale=1&cap_cd=&uid=&wxLang=&entry_url=https%3A%2F%2Furlsec.qq.com%2Freport.html&subsid=1&callback=_aq_106620&sess='
    r = s.get(url, headers=headers)
    # print(r.text)
    data = re.findall("\((.*?)\)", r.text)[0]
    data = (json.loads(data))
    data_dict['sess'] = data['sess']
    data_dict['sid'] = data['sid']
    frametime = int(time.time()) * 1000
    sess_url = f'https://t.captcha.qq.com/cap_union_new_show?aid=2046626881&captype=4&curenv=inner&protocol=https&clientype=2&disturblevel=1&apptype=1&noheader=1&color=&showtype=point&fb=1&theme=&lang=2052&ua=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzg5LjAuNDM4OS45MCBTYWZhcmkvNTM3LjM2&enableDarkMode=0&grayscale=1&sess={data_dict["sess"]}&fwidth=0&sid={data_dict["sid"]}&wxLang=&tcScale=1&uid=&cap_cd=&rnd=839520&TCapIframeLoadTime=21&prehandleLoadTime=69&createIframeStart={frametime}&subsid=2'

    sess_r = s.get(sess_url, headers=headers)
    # print(sess_r.text)
    data_dict['sess'] = re.findall('sess:"(.*?)",', sess_r.text)[0]
    data_dict['nonce'] = re.findall('nonce:"(.*?)",', sess_r.text)[0]
    data_dict['pow_answer'] = re.findall('prefix:"(.*?)"', sess_r.text)[0]
    app_data= re.findall('dcFileName:"(.*?)",', sess_r.text)[0]
    data_dict['data_app'] = app_data.split('&')[0].split('=')[-1]
    data_dict['t'] = app_data.split('&')[1]

    cdnPic1 = re.findall('cdnPic1:"(.*?)",', sess_r.text)[0]
    cdnPic2 = re.findall('cdnPic2:"(.*?)",', sess_r.text)[0]

    # 请求图片url
    imgurl1 = f'https://t.captcha.qq.com{cdnPic1}?aid=2046626881&sess={data_dict["sess"]}&sid={data_dict["sid"]}&img_index=1'
    r = s.get(imgurl1, headers=headers)
    with open('1.png', 'wb') as fw:
        fw.write(r.content)

    # 请求图片url
    imgurl2 = f'https://t.captcha.qq.com{cdnPic2}?aid=2046626881&sess={data_dict["sess"]}&sid={data_dict["sid"]}&img_index=2'
    r = s.get(imgurl2, headers=headers)
    with open('2.png', 'wb') as fw:
        fw.write(r.content)
    # print(data_dict)
    return data_dict

def _get_slide_distance(bg1,bg2):
    # 读取进行色度图片，转换为numpy中的数组类型数据，
    slider_pic = cv2.imread(bg1, 0)
    background_pic = cv2.imread(bg2, 0)
    # 获取缺口图数组的形状 -->缺口图的宽和高
    width, height = slider_pic.shape[::-1]
    # 将处理之后的图片另存
    slider01 = "slider01.jpg"
    background_01 = "background01.jpg"
    cv2.imwrite(background_01, background_pic)
    cv2.imwrite(slider01, slider_pic)
    # 读取另存的滑块图
    slider_pic = cv2.imread(slider01)
    # 进行色彩转换
    slider_pic = cv2.cvtColor(slider_pic, cv2.COLOR_BGR2GRAY)
    # 获取色差的绝对值
    slider_pic = abs(255 - slider_pic)
    # 保存图片
    cv2.imwrite(slider01, slider_pic)
    # 读取滑块
    slider_pic = cv2.imread(slider01)
    # 读取背景图
    background_pic = cv2.imread(background_01)
    # 比较两张图的重叠区域
    result = cv2.matchTemplate(slider_pic, background_pic, cv2.TM_CCOEFF_NORMED)
    # 通过数组运算，获取图片的缺口位置
    top, left = np.unravel_index(result.argmax(), result.shape)
    # 背景图中的图片缺口坐标位置
    # print("当前滑块的缺口位置：", (left, top, left + width, top + height))
    # 判读是否需求保存识别过程中的截图文件

    # 删除识别过程中保存的临时文件
    os.remove(slider01)
    os.remove(background_01)
    os.remove(bg1)
    os.remove(bg2)
    print(left)
    return left

def _generate_trace(distance, start_time):
    """
    生成轨迹
    :param distance:
    :param start_time:
    :return:
    """
    back = random.randint(2, 6)
    distance += back
    # 初速度
    v = 0
    # 位移/轨迹列表，列表内的一个元素代表0.02s的位移
    tracks_list = []
    # 当前的位移
    current = 0
    while current < distance - 13:
        # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
        a = random.randint(10000, 12000)  # 加速运动
        # 初速度
        v0 = v
        t = random.randint(9, 18)
        s = v0 * t / 1000 + 0.5 * a * ((t / 1000) ** 2)
        # 当前的位置
        current += s
        # 速度已经达到v,该速度作为下次的初速度
        v = v0 + a * t / 1000
        # 添加到轨迹列表
        if current < distance:
            tracks_list.append(round(current))
    # 减速慢慢滑
    if round(current) < distance:
        for i in range(round(current) + 1, distance + 1):
            tracks_list.append(i)
    else:
        for i in range(tracks_list[-1] + 1, distance + 1):
            tracks_list.append(i)
    # 回退
    for _ in range(back):
        current -= 1
        tracks_list.append(round(current))
    tracks_list.append(round(current) - 1)
    if tracks_list[-1] != distance - back:
        tracks_list.append(distance - back)
    # 生成时间戳列表
    timestamp_list = []
    timestamp = int(time.time() * 1000)
    for i in range(len(tracks_list)):
        t = random.randint(11, 18)
        timestamp += t
        timestamp_list.append(timestamp)
        i += 1
    y_list = []
    zy = 0
    for j in range(len(tracks_list)):
        y = random.choice(
            [0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
             0, -1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, -1, 0, 0])
        zy += y
        y_list.append(zy)
        j += 1
    trace = []
    for index, x in enumerate(tracks_list):
        trace.append([x, y_list[index], timestamp_list[index] - start_time])
    return trace

def _encrypt_trace(trace, distance):
    """
    加密轨迹
    :param trace: 轨迹
    :param distance: 距离
    :return:
    """
    # 对 k 值进行 base64 解码
    # text = base64.b64decode(trace)
    # t = base64.b64decode('0123456789abcdef')
    # 对解码后的 k 值进行 DES 解密（密钥: sshummei）, 取前8位作为下一次加密的密钥
    # new_key = AEScoder().encrypt(trace)
    # print(new_key)
    # 构造待加密数据
    # data = {
    #     # 滑动距离 / 300
    #     "d": distance / 300,
    #     # 轨迹
    #     "m": trace,
    #     # 滑动所用时间
    #     "c": trace[-1][-1],
    #     # 验证码图片尺寸, 宽
    #     "w": 300,
    #     # 验证码图片尺寸, 高
    #     'h': 150,
    #     # 设备
    #     'os': 'web_pc',
    #     # 是否 webdriver
    #     "cs": 0,
    #     "wd": 0,
    #     'sm': -1
    # }
    # 最后加密 DES
    return trace,distance

def get_kes(app_data,t):
    kes_url = f'https://t.captcha.qq.com/tdc.js?app_data={app_data}&{t}'
    kes_r = s.get(kes_url, headers=headers)
    kes = re.findall("apply\(Date, b\)};window.*?=(.*?);", kes_r.text)[0]
    print('kes: '+kes)
    return kes
# apply(Date, b)};window.DfflhNBYeRbBjBWlYeeCJJaVQVWfPhUb='TPSvW0UJxEBC9ux5UxhZT65HKZHPHW+Q0fAzYgzpQx0b7qQv2m06gK46ai2CKUP2aBqQkuaFvRrSg0RYMhvTtxq4OpT05DvyR6JPpa5Zp6zTu3a3rXeoO2L0r5SQ7oojF2hGzlhTLFyLUDlY5QqdFBXQ9C/cezgpbv6cpC6OsBdNg2yivE9hYcnP98EuidXXxYnEIZiSKJnmrfKsjGBmOWIXG25E+tml67yOaFcEhhU=';
'BEDSDWeEiFkXbChgYEkiUWPNJGmXRcjf'
def index():
    data_dict = _init_slider() #获取验证码和一些参数
    distance = _get_slide_distance('./1.png','./2.png') #计算滑动距离
    start_time = int(time.time() * 1000)
    trace = _generate_trace(distance, start_time)  #生成轨迹
    # st = _encrypt_trace(trace, distance)
    # print(st)
    print(data_dict,trace)
    kes = get_kes(data_dict['data_app'],data_dict['t'])
    data = {
        'aid': '2046626881',
        'captype': '4',
        'curenv': 'inner',
        'protocol': 'https',
        'clientype': '2',
        'disturblevel': '1',
        'apptype': '1',
        'noheader': '1',
        'color': '',
        'showtype': 'point',
        'fb': '1',
        'theme': '',
        'lang': '2052',
        'ua': 'TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzk1LjAuNDYzOC41NCBTYWZhcmkvNTM3LjM2',
        'enableDarkMode': '0',
        'aged': '0',
        'enableAged': '0',
        'grayscale': '1',
        'sess': data_dict['sess'],
        'fwidth': '0',
        'sid': data_dict['sid'],
        'wxLang': '',
        'tcScale': '1',
        'uid': '',
        'cap_cd': '',
        'rnd': '138680',
        'TCapIframeLoadTime': '5',
        'prehandleLoadTime': '182',
        'createIframeStart': int(time.time()*1000),
        'subsid': '2',
        'cdata': 0,
        'ans': '340,40;',
        'vsig': '',
        'websig': '',
        'subcapclass': '',
        'pow_answer': data_dict['pow_answer'],
        'pow_calc_time': 12,
        'collect': "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",
        'tlg': 2188,
        'fpinfo': '',
        'eks': kes,
        'nonce': data_dict['nonce'],
        'vlg': '0_0_1',
    }
#     data= {
#     "rnd": "705274",
#     "TCapIframeLoadTime": "170",
#     "prehandleLoadTime": "245",
#     "subsid": "2",
#     "cdata": 0,
#     "ans": "468,50;",
#     "tlg": 2636,
#     "fpinfo": "",
#     "nonce": "eda1152f11f1daf0",
#     "vlg": "0_0_1"
# }

    po_url = 'https://t.captcha.qq.com/cap_union_new_verify'
    r = requests.post(po_url,headers=headers,data=data)
    print(r.text)



if __name__ == '__main__':
    index()
    # 轨迹还需要加上最后一条 js 生成的, 不知道具体什么意思
    # trace.append([0, 0, u_challenge(cap_challenge)])
    '''
"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"    加密时需要这么多参数一起加密
    ""sd":{"od":"AYUBCYC","clientType":"","coordinate":[10,62,0.5],"trycnt":2,"refreshcnt":0,"slideValue":轨迹,"dragobj":1,"ft":"qf_7P_n_H"}}"
    '''
    # pass
    '''
    
    {
        "sd": {
            "od": "C",
            "clientType": "",
            "coordinate": [
                10,
                64,
                0.5
            ],
            "trycnt": 3,
            "refreshcnt": 0,
            "slideValue":[] ,
            "dragobj": 1,
            "ft": "qf_7P_n_H"
        }
    }
    '''

