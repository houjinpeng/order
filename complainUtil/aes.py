from Cryptodome.Cipher import AES
import base64

d = [[1, 0, 11], [5, 0, 22], [10, 0, 35], [14, 0, 53], [23, 0, 65], [33, -1, 80], [47, -1, 92], [65, -1, 103], [85, -1, 119], [104, -1, 133], [121, -1, 148], [142, -1, 161], [162, -1, 177], [192, -1, 195], [226, -1, 209], [249, -1, 227], [273, 0, 242], [298, 0, 257], [325, 1, 272], [352, 1, 290], [395, 1, 308], [428, 1, 322], [429, 0, 340], [430, 0, 354], [431, 0, 370], [432, 0, 382], [433, 0, 395], [434, 1, 407], [435, 1, 419], [436, 1, 437], [437, 1, 454], [438, 1, 470], [439, 1, 481], [440, 2, 492], [441, 2, 503], [442, 3, 521], [443, 3, 535], [444, 3, 548], [445, 3, 560], [446, 3, 571], [447, 3, 589], [448, 2, 607], [449, 2, 624], [450, 2, 636], [451, 2, 648], [452, 2, 662], [453, 2, 679], [454, 2, 694], [455, 2, 708], [456, 3, 723], [457, 3, 739], [458, 3, 752], [459, 3, 764], [460, 3, 782], [461, 3, 797], [462, 3, 813], [463, 3, 827], [464, 3, 842], [465, 3, 856], [465, 3, 867], [464, 3, 883], [463, 3, 894]]



class AEScoder():
    def __init__(self):
        self.__encryptKey = "0123456789abcdef"
        self.__key = base64.b64decode(self.__encryptKey)

    # AES加密
    def encrypt(self, data):
        cryptor = AES.new(b'0123456789abcdef',AES.MODE_CBC,b'0123456789abcdef')
        encrData = cryptor.encrypt(base64.b64decode(str(d))).decode()
        # encrData = cryptor.encrypt(data)

        # encrData = base64.b64encode(encrData)
        return encrData

    # AES解密
    def decrypt(self, encrData):
        # encrData = base64.b64decode(encrData)
        # unpad = lambda s: s[0:-s[len(s)-1]]
        unpad = lambda s: s[0:-s[-1]]
        cipher = AES.new(self.__key, AES.MODE_ECB)
        decrData = unpad(cipher.decrypt(encrData))
        return decrData.decode('utf-8')

# AEScoder().encrypt(str(d))