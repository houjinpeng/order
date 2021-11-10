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
    print(data_dict)
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
        'cdata': '0',
        'ans': '340,40;',
        'vsig': '',
        'websig': '',
        'subcapclass': '',
        'pow_answer': '97b29991be388159#694',
        'pow_calc_time': '12',
        'collect': 'qY0PirHsr0wa/LD8SdHrLTLj7 d0DPLe4m1ppMSiDyggrMEfgdhDDXy4cYfozp/Vk0NUL0FpxsDXjAl4IYkh/Y/FGvjfRkbdeEcewCXSgOcdTv5atoAZrIori6ffKmS6oUpWP834PhPjDuXnWfhxSGehydCAI8vIUmCtNoUEh6ppOldX675eVQLX3GjntBjPrQoRnM0sdg /Ns8BM0AFCj3A2hTYy/ZsUfSHpcbQF4YjyOtAo3F5UWbbmOg3YUnUQ0Tez33DvNqY71Bx3Rsh1L2YqYunCkCKaZUzFzeiBSCHBc9TfOUf2MhwaCXTpyZCyBjR5ysCaE1tT4KZBxYgS6lnPR5tNWOomlKKXelufJwFjZIvGArDbn8vrkhWU7n8h4N14PQAxi3W2DJ3C5ef0jIf42Sa6DSaH8v7KVU5FW3FBHdg6IlMgo9e/ds5TCDeLLhcBAa9SxxCTzkdssuGHIiVhvgY4vYKF1pzf0KvuqRXtut9GsLrRIzHeyWxPuMTyoW Hx72eeQfcodyLu1cWVN4SHXRmh8jj8Aj/7spW Yppy97hglMKJlZB5UmMcREdqMVAzpdD4K2IG51oFQ0FOzHVkWKNT86s9PBN8/y9aaxenIcGePFMQ1Bl2495PpFkXDPgICZ3g00vwFYmiADBNI7Sw hAPIHfNWfEJ1KkA7qQDG/fAi9YGfm0pjwa522ow827rA45c Uq0uIz/QP5pq1Ynt51Ovx98OEudEyb4l9QMQdhdfpUn1AxB2F1 lSSAbBxn2twOFVSpnBwZTFICWTW/1RyDDGvoac3eRfau3B docUd8IYNeeUmaoe9Qn2SeblkKTMCrQjPQBVaEqdwprxClQsAby4ltnnxm9C/TRJ/entKtuQ3d/Cv1aB1iy1va6prVBt Yh2Dp1RN/klTLV3wSS6e9kN11I3GIvT3B1nsuCP /QiN9z79RL9jQRd/2/wANZR7PBaejuBGDzSubWnzqkGS6YXFQXSIQtG1BSjMWCCdmo4ie0LEFGWKRjZkHv5/QOqzIcbH MVGJ Ip/Dor2OsUBfxI7AeoBofmq1UDFLEgoaMFMD0bbCDSs9NSdwChqBKAZiurky84VecTH8JMD6pSTxbvp22XFFDfv MccTrETuBW3sPr82x0EGqgVZcqm9ig6bZZ6EOjWJW1b8FQuuUNpSEJKxmN 2ScoCmT16lWLyPvXrShVjjY Vh9quCtRcWTBvBHHCTCqdEgMt 2COVOuctpNYdBR60pn79B1QIM4n0Wp0krKo1/c/I0QqWADu8MQm8vfaSA6dalHt/LCdEiWh3VEj5HfkgvZ3NMWh1pIgbHLFssS8UjKBJt8uQLmXXM65n31vfvnAluwtr3kUMPctyvuXM6tU 9aQYNS/8lOOIJBg1L/yU44gMqVyrf5IHsHwfDbA1bsLOvyE4rxlebKu pwa67bC15FQaTEz2MOHtwu5dHLnli2VgKSSckgkJK9pwOgBASDbdbAGn8bGZdFN7/whUYLDKhtBc8FlKD2xUPF bg6XDyEMS3QFxdw03KcMoAwtdibKT8FI3PKSuAk2OUHuaqco0WXvmrkUmZnhO/T0yX/pGeFr2hgD1IQZpg4bC86PIct7sfyP4fkqw99MRLeIpahx5xj1wXHKYFx6qwqWtG7G9M2P9L4C7ctBTdBvIVnIMTc9mCxsuGVEHSEl3ZpG4BPPnlAh4Ipg4gBeh0VDhrZfCHJE8IB9qpD6ABvCZzk5llbD9uV1SIcmTcsVkBCuv3Y3dVsTbU58vVR16H1AxB2F1 lSZkzkDjSFFXe/srlQrd/zIuC2QDKv6TQQnp3Rv6I/X1ujFT81Om4WWE6B Wnr6hYo LypRQOXpbzWuF3u3s0HQbTTAf3cFnhoUjIMMGzzBF2p42UvaboPdbVa4SvOrBnhSrh5Ch8T1QZTSoXOu8VVFTSMdK7cjstbjHxzpCWR BMmBcW/kzav8u1dsBY7SanpA4UzUIXse AseaMMTyi01RowTB5ZDmd cKcFekLuVdX9Syc8kra8yc3AMhhdArBpsP9N4DAI7IJHFoa3 RVmgWUEVRlbdu7WwwMX7TkTSDX53q65M5 Kgqa9KsDswKh621KZlVIxhesxkWPmravHd6qp w9Po1Qpk/uSAFTqRNlhZmliZIBCMdTK3NpG HnH64L4Pah8ro0=',
        'tlg': '2188',
        'fpinfo': '',
        'eks': kes,
        'nonce': 'eda1152f11f1daf0',
        'vlg': '0_0_1',
        'vData': 'W4hcQalehU_qy-XCk0hWtkJj-lBL_A6U2M1H9W*BkSBxiEQrPPWgNi33XXPAUNGbuQsNnjSZtCFur0RiqslJ6a89Ors0QTonBPLy67lhyTDFNoFsNz0RmaqxmPhKeuHzuAKqlxUcL9yFjBMA5RsJRiYY',
        'Content-Type': 'text/plain'
    }

    po_url = 'https://t.captcha.qq.com/cap_union_new_verify'
    r = requests.post(po_url,headers=headers,data=data)
    print(r.text)
    v_dict = {"mouseclick":[{"t":2273,"x":269,"y":148}],
              "keyvalue":[],"user_Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
              "resolutionx":1920,
              "resolutiony":1080,
              "winSize":[300,232],
              "url":"https://captcha.guard.qcloud.com/cap_union_new_show",
              "refer":"https://cloud.oppo.com/login.html",
              "begintime":int(time.time()),
              "endtime":int(time.time())+3000,
              "platform":1,
              "os":"other",
              "keyboards":0,
              "flash":1,
              "pluginNum":50,
              "index":1,
              "ptcz":"",
              "tokenid":1596750647,
              "a":1596750647,
              "btokenid":'null',
              "tokents":1546775906,
              "ips":{"in":["192.168.50.125"]},
              "colorDepth":24,
              "cookieEnabled":'true',
              "timezone":8,
              "wDelta":0,
              "mousemove":[[265,148,2273707],[-14,5,12],[-19,8,16],[-16,7,17],[-18,7,15],[-17,6,18],[-7,2,17],[-11,3,16],[-9,1,17],[-6,0,17],[-6,0,15],[-7,0,17],[-7,1,16],[-11,0,17],[-10,0,17],[-8,0,20],[-6,0,15],[-4,0,15],[-5,0,17],[-5,0,17],[-3,0,17],[-2,0,34],[-3,0,32],[-2,0,17],[-6,0,18],[-1,0,15],[-1,0,36],[-2,0,16],[-1,0,15],[-2,0,16],[-1,0,20],[-1,0,32],[-1,0,15],[-2,2,17],[-2,1,18],[-3,2,15],[-2,3,16],[-2,1,17],[-1,1,33],[4,0,217],[2,0,18],[4,0,15],[1,0,19],[3,0,16],[2,0,16],[3,0,17],[4,0,17],[2,0,16],[2,0,17],[2,0,16],[2,0,18],[3,0,15],[2,0,16],[2,0,17],[3,0,33],[3,0,37],[2,0,16],[2,0,15],[2,0,16],[2,0,17],[2,0,16],[2,0,17],[1,0,17],[2,0,17],[3,0,16],[1,0,18],[2,0,16],[1,0,50],[1,0,18],[1,0,18],[1,0,14],[1,0,19],[1,1,15],[1,0,33],[1,0,16],[1,0,18],[1,0,32],[1,0,89],[1,0,29],[1,0,15],[1,0,18],[1,0,17],[1,0,15],[-1,-1,352],[-1,0,32],[0,-1,18],[-1,0,17],[-1,0,682],[-1,0,16],[0,-1,84],[-1,0,33],[1,0,518],[1,0,16],[1,0,33],[2,0,33],[-1,-1,618]],"keyUpCnt":0,"keyUpValue":[],"mouseUpValue":[{"t":2279,"x":120,"y":195}],"mouseUpCnt":1,"mouseDownValue":[],"mouseDownCnt":0,"orientation":[],"bSimutor":0,"focusBlur":{"in":[],"out":[],"t":[]},"fVersion":31,"charSet":"UTF-8","resizeCnt":0,"errors":[],"screenInfo":"1920-1080-1040-24-*-*-*","elapsed":0,"ft":"qf_7P_n_H","coordinate":[10,9,0.5],"clientType":"2","trycnt":1,"refreshcnt":3,"slideValue":[[45,198,127],[2,0,15],[4,0,16],[1,0,19],[3,0,16],[2,0,16],[3,0,17],[4,0,17],[2,0,16],[2,0,16],[2,0,16],[2,0,18],[3,0,16],[2,0,16],[2,0,16],[3,0,34],[3,0,36],[2,0,16],[2,0,15],[2,0,16],[2,0,17],[2,0,16],[2,0,17],[1,0,18],[2,0,16],[3,0,18],[1,0,16],[2,0,17],[1,0,50],[1,0,17],[1,0,18],[1,0,15],[1,0,19],[1,1,15],[1,0,33],[1,0,16],[1,0,18],[1,0,31],[1,0,89],[1,0,29],[1,0,16],[1,0,18],[1,0,16],[1,0,16],[-1,-1,351],[-1,0,33],[0,-1,18],[-1,0,17],[-1,0,682],[-1,0,16],[0,-1,84],[-1,0,34],[1,0,517],[1,0,15],[1,0,33],[2,0,34],[-1,-1,617],[0,0,5]],
              "dragobj":0}

    # print(st)
    # get_kes(data_dict['data_app'],data_dict['t'])


if __name__ == '__main__':
    index()
    # 轨迹还需要加上最后一条 js 生成的, 不知道具体什么意思
    # trace.append([0, 0, u_challenge(cap_challenge)])
    '''
"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"    加密时需要这么多参数一起加密
    ""sd":{"od":"AYUBCYC","clientType":"","coordinate":[10,62,0.5],"trycnt":2,"refreshcnt":0,"slideValue":轨迹,"dragobj":1,"ft":"qf_7P_n_H"}}"
    '''
    # pass