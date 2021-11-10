from Cryptodome.Cipher import AES
import os
import base64
from binascii import b2a_hex, a2b_hex

# 如果text不足16位的倍数就用空格补足为16位
def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')


 # 加密函数
def encrypt(text):
    text = add_to_16(text)
    cryptos = AES.new(key, mode, iv)
    cipher_text = cryptos.encrypt(text)
    e = b2a_hex(cipher_text)
    print("加密:", e)
    return e
# 因为AES加密后的字符串不一定是ascii字符集的，输出保存可能存在问题，所以这里转为16进制字符串

 # 解密后，去掉补足的空格用strip() 去掉
def decrypt(text):
    cryptos = AES.new(key, mode, iv)
    #t =  add_to_16(a2b_hex(text).decode())
    plain_text = cryptos.decrypt(a2b_hex(text))
    return bytes.decode(plain_text).rstrip('\0')


if __name__ == '__main__':
    key = '0123456789abcdef'.encode('utf-8')
    mode = AES.MODE_CBC
    iv = b'0123456789abcdef'
    t = '12345678'
    a = "0xc8wOQ3ztcsC9UeJFKfsFTnTzm71ZvAa0LYvqgoFU2Z0W2mtCTWZ1sjUdL4KuxBBytRC8Uo9jV4ksPxUGlJxoouEC2C0aWbKpULKCJGDwXymVMlkqkII6K YDS6Wl0HuXWY4MpLrQXAnkzq3xN/X6eI73910c60xVjFDeNPA8rKarM3ZXaH058ruR5USIZpDddPsJBOa6wPhJVCd0gIQK0 hm5h3seTo6CRoHwcTv6/ry9RPtJh3HRE8o9C7N89PehbP4Rjd2VPxQWEZO4nZe8vvSfSZj3GLTsOFtEmPUJeBGc1fL8t0DnCrpKpIV41s0B8Lm8hBiC7sAVM/kZIDJjtJe5TLdFFkF87TZ9H7oMDGjUhkawN5TRkgzKeUo5mmJWIRHBIRCoA5 VlTp tANOpGsW07Dd  k6kMBZ10e5c3xfOwAK5OUwLpoXbnuQ7vA/jSqvCeK aLCFb1vv5SXxdxfOPQdrAcOM1POdBuQgWOUWqmgP8hsMJZn9AZulBYcHAasUO1fLmwd0amnbhFtoP1B28hN6fL9mt6zZ5H2MVqrdcSynoS0WDIv8Ytsg44Goq0CpGeQXkpWMtBOkHif/mlz1dma4WCXO4NZrJw21W6My7/uxPE31AxB2F1 lSgdcPBTMYmk3xfm4Olw8hDH1AxB2F1 lSBLufJKX4XBsCjXpqQoUgazozy/M/QinHr2KNPhqhPyLYkzkYoItcbtJLthJHtATWZucxu6mmn3LBsqImL/h2ivmgQQw0JPr DOBwNLgPcuLb4ClY0wtO68RtF21XHRQjTK2wkaC/R5qDQ8ENySzW9p5UqseW2wYl/Aj2eTQx91eBkh26sQBbevV5uNOK5r8605bVd6XvEmJQOqgsgo0SUXnlbmmTFd0Suy2iAtQho5lS0 PMQPRFHg7TqxDHWUTXZZQ6JSslpZ0qGwDRs67HYH1AxB2F1 lSZkzkDjSFFXe/srlQrd/zIuC2QDKv6TQQnp3Rv6I/X1ujFT81Om4WWE6B Wnr6hYo LypRQOXpbzWuF3u3s0HQbTTAf3cFnhoUjIMMGzzBF2p42UvaboPdbVa4SvOrBnhdTI54PKy7EEI1efDIL3z4ORs/ps3 ZcD8NrfeXeMylRTfVfmiU TowFxa4 CCM488Q8k62gLvoMd8tlKmVau8d L6rTPec5wj/In2DVimKVuy8ssXJTj41 NjIRv2YWZ7FFMbYtg00K3NOz3rOmv0L/2 4f1YBlJbtFJPuZoN8abJFA3WSvrD2nraO3BrGMjkGDUv/JTjiBLrhuRpnV0tkuuG5GmdXS2RUhUezr2KmYzNBKop6/KrYHQ/xvRDjxywvefs9JcKR/C95 z0lwpH8L3n7PSXCkfwvefs9JcKR9ZaVRAiTAd0fsAGekT2SKRWfNiNh4dF8xkw5iYsP35S5xy18H7X iEh2qaNnpa6UemunKr9EPGU wT Y7tOs 1"
    # a = "0xc8wOQ3ztdZxUiAJwKW031AxB2F1+lSgdcPBTMYmk3xfm4Olw8hDH1AxB2F1+lS9h8eNftLBZY0ZIMynlKOZpiViERwSEQqAOflZU6frQDTqRrFtOw3fvpOpDAWddHuXN8XzsACuTlMC6aF257kO7wP40qrwnivmiwhW9b7+Ul8XcXzj0HawHDjNTznQbkItVBRioRjBYUc0tGVYnXYs4GFw15dFFlt1no1IRCOcqZhM2xnRob1kuL6l0dEIlN/SjZBveLQBbLb3/tsa9YnfycBL4msp3tuvRy3vz99mIEm2R9ktxVv8xVjkqAsXLShnlh6XkqoXTbdPSvMKN9I0MW8MngaWtcC5SP0bkd82EcaK+pZKda1aKxLy+EyZIy+AI3IBEKxEwjCoQtAu0GwVwafrxwHoBmhxT5K53PVIzpgCSa38pTWLmDDyPRX9iKWgHjRjMwz++pnyrf7bP5HChLFbY2NmRnSQyXZw8UpMvRgINaEbxkEolBD71WXyBXzSmD0hgomwuDJ+PVdK47LkH1sDMsfhtb38fRxkBXm4EIrBn/HFmkECPxwFTiSTVK8ypTsy7jUaBLngN6bASZC0xRaylkxKa+TUrmz+2SnXKHsAOf6plKw1GoZkgyLTAWfgHMwuhVWPz0/YCM78XnKrD2fYvmzX5kwVU+XBOwZ1c/VTfHonQ/FHinEEFv8kPxIRJK5yrNbWthzZ3Gwbu+2IaM7ZrxJM4aHZgpfvJDqrGBVrmyDekQxpMocgLy5a2My6HmLjfgUC1guj/UxfelxgUW6J92V37GFbZeysCBdT3VzptZ3dqORxte4TOTKlu1fWTNv1WVwp0FhISokAShXxRecbY8DTacFXMau9wTL9jEGMlwHNkqJS2SE6/7CUYmu8VwYRfvHsm4/TL3U62q+6sFI3PKSuAk2OUHuaqco0WWFy/Bxq0YF7X1AxB2F1+lSZkzkDjSFFXe/srlQrd/zIuC2QDKv6TQQnp3Rv6I/X1ujFT81Om4WWE6B+Wnr6hYo+LypRQOXpbzWuF3u3s0HQWV8vXLF6sh7UjIMMGzzBF2p42UvaboPdbVa4SvOrBnhFPwZpmtiGlvIoN8221fGRpoRNaM5dzaxniuLNAHSxBrToJckSEW3WuZoP5VMQUm4iMIN0B8XSYju9zWUIRL5CSWnb8B/lnNS2SeblkKTMCpzbZIVjJzNwz2yEejD0l0VryBjR+w1G8kZMOorChvzHK8JwCVPZQ+PuMKt0qaDVVS+6a1lg2Z0EB7WLzummJVgniuLNAHSxBqeK4s0AdLEGhE1LQHzQ20+PNCGkNsmpI880IaQ2yakjzzQhpDbJqSPPNCGkNsmpI8RNS0B80NtPoXgXNZnRIWiBR8ql0WaQbki7xRFHjC/ZOATQCKMBlMjS64bkaZ1dLZHIf8uaw/TAKf0Q3n1+8F50l2flj69ZxbDdzDhvv9XYs59t+WAks0Iw3cw4b7/V2KrRwHKwkW08h0sTjWn9UC61B0F6XpAtleuUAu0DanuQPGeessnJag0S1zd4YITYqcRNS0B80NtPoXgXNZnRIWi88raKZ4mvWxgpS6kKkhuVGClLqQqSG5UItrxpnhorPlRVLDtOS3jh7+K9Q+LeKG7C7l0cueWLZXOGTQxhVjmYKtHAcrCRbTy8ChrjgZrFr9epl9XBg1Mh/GeessnJag0DeJfUjTElApo3nebOugSEBfN1jiiLZELkD9F/+rGl/poUSBkmu5KId6cWGTOEtVAnxKb8SL5gPurDfFfASa882ahTsAp1tTZvP+UZEtb60Bvro+JE/RFfNMFLUCznPE+HsSvTBxUyMi2PklHAs06BYpcSRHD3d6kj2Gz6R04yQWawcbmRx+urA=="
    # a = 'qY0PirHsr0zFBHdg6IlMgmWgGuvuJxPB5dgHRlJ2Vl4mcdyocqXKC9I9sz9hZf7OXjtOCpFFS1V6WumvnaxE4cybZbypsIgUUN%2BmAnuRhavzsvlQ1Gs3K7ajEhnwP6cGrfAyDx1rDsNIylSOcXsrP8mze2ZwWDqgpl0w1YamJnlHIVR5YHBmhdV5pMnGGUpmPtprgyqWQpwklXH%2FHTxrWSyXJvzBAx4Mu31ocbjJnxVU69dlAOMg0NQW51GdsFpG4mGSkQpBpl2y68NmxftVFLOk64fdkFoRLetcef7pim8oVhMZkE5ivsOPgtc9gYV0rS0GMIJn3HmdktjHeK7VFd1XnLUyNsi6%2Fv%2FTE1o0eltEltehIlpkniFNB2glvk696hzTvrWQLGosGW0GxpAmQ6RcLfv4upwsZfTgn9oPjqeKz33q61KcqwS7nySl%2BFwbAo16akKFIGs6M8vzP0Ipx69ijT4aoT8i2JM5GKCLXG7SS7YSR7QE1mbnMbuppp9ywbKiJi%2F4dor5oEEMNCT6%2FgzgcDS4D3Li2%2BApWNMLTuvEbRdtVx0UI0ytsJGgv0eag0PBDcks1vbTAZi59%2BLQlqCVrypIneRYJDsFaiRAsMY3Z%2FMRy8LuDqueaEP%2FLrkIHBP9inuOp6kxnlN5kKGEbH1AxB2F1%2BlSgdcPBTMYmk3xfm4Olw8hDH1AxB2F1%2BlSNBNxvPVA0RMsGcV9tjDR%2FQ9r%2FWi9i8GpJxSIoGK9X1eWQ4R4HrWwT1CfAW6xwbWnAJ3gs%2FafM%2BTL3hIxOijRO58xD365fpExpRqNn2WwAH7ZXcbuhfWB9iN9LgG4NtbvRYMi%2Fxi2yDjgairQKkZ5Bae5Z24%2Fhe4zq8F53CsOTOwQ0qNfSAjKBGn6GFqimoM8%2Bpk31%2Bm0e4ZhgLNYhW2xbDaipOXPSBjweRIeDNsRXubVjVRXdL96%2Fn1AxB2F1%2BlSZkzkDjSFFXe%2FsrlQrd%2FzIuC2QDKv6TQQnp3Rv6I%2FX1ujFT81Om4WWE6B%2BWnr6hYo%2BLypRQOXpbzWuF3u3s0HQdvH3VRbkFpPUjIMMGzzBF2p42UvaboPdbVa4SvOrBnh8uujOUf7ErJps3MNb8Ag3b4%2BliU5EU0Hvj6WJTkRTQdLXN3hghNipzzQhpDbJqSPniuLNAHSxBrDAxftORNINcMDF%2B05E0g16%2B2M57E9TEpu0Uk%2B5mg3xq75k1vQgXkkuXyvRfIbzHe5fK9F8hvMd50eHkNRgz71%2Bpwa67bC15Hsfckop5%2BZkWlzRb0Pd5T0qFuboh1Xws6H36%2FEWkO59rGE4kvzlR7u1PvfsM6BIPN0Pdzwr%2BmtOzumB8bVdKWUu323uoss1x6mDS%2FjexhuC1aruIVmdMKn%2FDTn6Bd4XOVwxa3KOc%2B08sPRu5URVqYZQNcKPJwFgTTOfbflgJLNCFlpVECJMB3R%2BwAZ6RPZIpHC95%2Bz0lwpH1pcixr8nULots5pPf6EBCn%2FPrVa3wwudb4%2BliU5EU0HSHnJNJrVbdnNGBtgLSNr5a%2FktEEyTDU%2BniuLNAHSxBoRNS0B80NtPsMDF%2B05E0g1wwMX7TkTSDX50ft4KBUnkvlBHSqBTzYJbtFJPuZoN8bt3PrBbKnl1WClLqQqSG5U4FBYdfPdXyFHIf8uaw%2FTADWCPqVijJtTgdD%2FG9EOPHKrRwHKwkW08h0sTjWn9UC6SBx2MDGXtmpIHHYwMZe2amahTsAp1tTZS1zd4YITYqc80IaQ2yakjxfN1jiiLZEL8ZuJZtB%2BLvDhzhZg%2B5Mo8YHQ%2FxvRDjxyq0cBysJFtPIdLE41p%2FVAuq57xRH%2BODXgPHiPjmbOXTr2yBAkNDAk9Qhq%2BUUSKpil7WC4KbJ47K1%2BpAnh5gW5Vw%3D%3D'
    # a = '{"mousemove":[[265,148,2273707],[-14,5,12],[-19,8,16],[-16,7,17],[-18,7,15],[-17,6,18],[-7,2,17],[-11,3,16],[-9,1,17],[-6,0,17],[-6,0,15],[-7,0,17],[-7,1,16],[-11,0,17],[-10,0,17],[-8,0,20],[-6,0,15],[-4,0,15],[-5,0,17],[-5,0,17],[-3,0,17],[-2,0,34],[-3,0,32],[-2,0,17],[-6,0,18],[-1,0,15],[-1,0,36],[-2,0,16],[-1,0,15],[-2,0,16],[-1,0,20],[-1,0,32],[-1,0,15],[-2,2,17],[-2,1,18],[-3,2,15],[-2,3,16],[-2,1,17],[-1,1,33],[4,0,217],[2,0,18],[4,0,15],[1,0,19],[3,0,16],[2,0,16],[3,0,17],[4,0,17],[2,0,16],[2,0,17],[2,0,16],[2,0,18],[3,0,15],[2,0,16],[2,0,17],[3,0,33],[3,0,37],[2,0,16],[2,0,15],[2,0,16],[2,0,17],[2,0,16],[2,0,17],[1,0,17],[2,0,17],[3,0,16],[1,0,18],[2,0,16],[1,0,50],[1,0,18],[1,0,18],[1,0,14],[1,0,19],[1,1,15],[1,0,33],[1,0,16],[1,0,18],[1,0,32],[1,0,89],[1,0,29],[1,0,15],[1,0,18],[1,0,17],[1,0,15],[-1,-1,352],[-1,0,32],[0,-1,18],[-1,0,17],[-1,0,682],[-1,0,16],[0,-1,84],[-1,0,33],[1,0,518],[1,0,16],[1,0,33],[2,0,33],[-1,-1,618]],"keyUpCnt":0,"keyUpValue":[],"mouseUpValue":[{"t":2279,"x":120,"y":195}],"mouseUpCnt":1,"mouseDownValue":[],"mouseDownCnt":0,"orientation":[],"bSimutor":0,"focusBlur":{"in":[],"out":[],"t":[]},"fVersion":31,"charSet":"UTF-8","resizeCnt":0,"errors":[],"screenInfo":"1920-1080-1040-24-*-*-*","elapsed":0,"ft":"qf_7P_n_H","coordinate":[10,9,0.5],"clientType":"2","trycnt":1,"refreshcnt":3,"slideValue":[[45,198,127],[2,0,15],[4,0,16],[1,0,19],[3,0,16],[2,0,16],[3,0,17],[4,0,17],[2,0,16],[2,0,16],[2,0,16],[2,0,18],[3,0,16],[2,0,16],[2,0,16],[3,0,34],[3,0,36],[2,0,16],[2,0,15],[2,0,16],[2,0,17],[2,0,16],[2,0,17],[1,0,18],[2,0,16],[3,0,18],[1,0,16],[2,0,17],[1,0,50],[1,0,17],[1,0,18],[1,0,15],[1,0,19],[1,1,15],[1,0,33],[1,0,16],[1,0,18],[1,0,31],[1,0,89],[1,0,29],[1,0,16],[1,0,18],[1,0,16],[1,0,16],[-1,-1,351],[-1,0,33],[0,-1,18],[-1,0,17],[-1,0,682],[-1,0,16],[0,-1,84],[-1,0,34],[1,0,517],[1,0,15],[1,0,33],[2,0,34],[-1,-1,617],[0,0,5]],"dragobj":0}'
    e = encrypt(t)  # 加密
    c = b2a_hex(bytes(a.encode('utf-8')))

    d = decrypt(c) # 解密
    print("解密:", d)