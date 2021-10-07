import base64

from Cryptodome.Cipher import AES
from binascii import b2a_hex, a2b_hex


class PrpCrypt(object):
    # 密钥（key）, 密斯偏移量（iv） CBC模式加密 备注：保证key和iv必须是16位
    def __init__(self, key):
        self.key = key.encode('utf-8')
        self.mode = AES.MODE_CBC
        self.iv = ("0123456789abcdef").encode('utf-8')

    def encrypt(self, text):
        text = text.encode('utf-8')
        cryptor = AES.new(self.key, self.mode, self.iv)
        length = 16
        count = len(text)
        if count < length:
            add = (length - count)
            text = text + ('\0' * add).encode('utf-8')
        elif count > length:
            add = (length - (count % length))
            text = text + ('\0' * add).encode('utf-8')
        self.ciphertext = cryptor.encrypt(text)
        return b2a_hex(self.ciphertext)

    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return bytes.decode(plain_text).rstrip('\0')


a = '[[1, 0, 15], [4, 0, 32], [9, 0, 50], [14, 0, 65], [20, 0, 76], [30, 0, 89], [46, 0, 104], [56, 0, 122], [68, -1, 133], [87, -1, 150], [106, 1, 168], [128, 1, 184], [159, 2, 199], [192, 2, 214], [224, 2, 229], [266, 2, 240], [302, 2, 258], [339, 2, 271], [367, 2, 282], [399, 2, 296], [448, 1, 311], [494, 1, 327], [495, 1, 344], [496, 1, 357], [493, 1, 373], [492, 1, 389], [491, 1, 402], [490, 1, 418], [493, 2, 431]]'

dic = {"mouseclick": [{"t": 9, "x": 277, "y": 147}], "keyvalue": [], "user_Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36", "resolutionx": 1920, "resolutiony": 1080, "winSize": [300, 232], "url": "https://captcha.guard.qcloud.com/cap_union_new_show", "refer": "https://cloud.oppo.com/login.html", "begintime": 1546828509, "endtime": 1546828520, "platform": 1, "os": "other", "keyboards": 0, "flash": 1, "pluginNum": 50, "index": 1, "ptcz": "", "tokenid": 2785582500, "a": 2785582500, "btokenid": 'null', "tokents": 1487589456, "ips": {"in": ["192.168.50.125"]}, "colorDepth": 24, "cookieEnabled": 'true', "timezone": 8, "wDelta": 0,
       "mousemove": [[268, 149, 8343], [-8, 2, 12], [-9, 4, 18], [-7, 3, 16], [-8, 4, 16], [-4, 2, 16], [-5, 4, 18], [-6, 2, 16], [-6, 3, 17], [-5, 1, 16], [-7, 1, 19], [-1, 0, 15], [-5, 0, 17], [-4, 1, 15], [-5, 0, 18], [-7, 1, 16], [-11, 2, 18], [-20, 0, 17], [-12, 1, 16], [-14, 1, 16], [-12, 2, 17], [-10, 1, 19], [-11, 1, 14], [-12, 2, 18], [-11, 1, 16], [-5, 1, 16], [-6, 0, 17], [-1, 0, 18], [-2, 0, 16], [-1, 0, 16], [-1, 0, 34], [-4, 0, 16], [-5, 0, 17], [-2, -1, 17], [-1, 0, 18], [-1, 0, 48], [0, 1, 150], [0, 2, 17], [0, 1, 49], [2, 0, 200], [1, 0, 16], [2, 1, 18], [1, 0, 16], [3, 1, 19], [1, 0, 14], [3, 0, 19], [1, 0, 15], [3, 0, 16], [1, 0, 34], [2, 1, 18], [3, 1, 18], [2, 0, 14], [2, 0, 17], [2, 0, 17], [2, 0, 17], [3, 1, 26], [7, 1, 41], [2, 1, 15], [2, 0, 19], [2, 0, 15], [3, 0, 34], [1, 1, 15], [3, 1, 17], [2, 0, 18], [2, 0, 32], [3, 1, 34], [1, 0, 33], [1, 0, 133], [1, 0, 17], [1, 0, 16], [1, 1, 17], [1, 0, 18], [1, 0, 16], [1, 0, 268], [0, 1, 15], [2, 0, 33], [1, 0, 50]],
       "keyUpCnt": 0, "keyUpValue": [], "mouseUpValue": [{"t": 11, "x": 111, "y": 204}], "mouseUpCnt": 1, "mouseDownValue": [], "mouseDownCnt": 0, "orientation": [], "bSimutor": 0, "focusBlur": {"in": [], "out": [], "t": []}, "fVersion": 31, "charSet": "UTF-8", "resizeCnt": 0, "errors": [], "screenInfo": "1920-1080-1040-24-*-*-*", "elapsed": 1000, "ft": "qf_7P_n_H", "coordinate": [10, 9, 0.5], "clientType": "2", "trycnt": 1, "refreshcnt": 1, "slideValue": [[41, 192, 116], [1, 0, 15], [2, 1, 18], [1, 0, 16], [3, 1, 20], [1, 0, 13], [3, 0, 19], [1, 0, 14], [3, 0, 17], [1, 0, 34], [2, 1, 18], [3, 1, 17], [2, 0, 15], [2, 0, 17], [2, 0, 17], [2, 0, 16], [3, 1, 27], [7, 1, 41], [2, 1, 15], [2, 0, 18], [2, 0, 16], [3, 0, 34], [1, 1, 15], [3, 1, 17], [2, 0, 18], [2, 0, 32], [3, 1, 33], [1, 0, 34], [1, 0, 133], [1, 0, 17], [1, 0, 16], [1, 1, 18], [1, 0, 17], [1, 0, 16], [1, 0, 268], [0, 1, 14], [2, 0, 35], [1, 0, 49], [0, 0, 63]], "dragobj": 0}

import json

dic = json.dumps(dic)
if __name__ == '__main__':
    # pc = PrpCrypt('0123456789abcdef')
    # # e = pc.encrypt(str(a))
    # e = pc.encrypt(dic)
    # d = pc.decrypt(e)
    # print("加密:", e)
    # print("解密:", eval(d), '\n', type(eval(d)))


    str1 = "TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzg5LjAuNDM4OS45MCBTYWZhcmkvNTM3LjM2"
    str2 = '0123456789abcdef'
    str3 = '0123456789abcdef'
    mode = AES.MODE_CBC
    cryptor = AES.new(str2.encode("utf8"), mode, str3.encode("utf8"))
    plain_text = cryptor.decrypt(base64.b64decode(str1)).decode()