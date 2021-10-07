# @Time : 2021/5/7 8:59 
# @Author : HH
# @File : test.py 
# @Software: PyCharm
# @explain:

import execjs

with open('jjjs.js','r',encoding='utf-8') as fr:
# with open('腾讯防水墙.js','r',encoding='utf-8') as fr:
    data = {
    "aid": "2046626881",
    "captype": "4",
    "curenv": "inner",
    "protocol": "https",
    "clientype": "2",
    "disturblevel": "1",
    "apptype": "1",
    "noheader": "1",
    "color": "",
    "showtype": "point",
    "fb": "1",
    "theme": "",
    "lang": "2052",
    "ua": "TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzg5LjAuNDM4OS45MCBTYWZhcmkvNTM3LjM2",
    "enableDarkMode": "0",
    "grayscale": "1",
    "sess": "s0nlFEuYjH56PhOEodWxwu2_yKnwpPciowFz9P5ntOcOEIeTE7GwYaKtf2-6R5mFCVhrP4BhHWpRrhzJjmMF6tHGQZHoeVuoKsN43fhPH3WcOOCGA60WrwYycnzoecrGhY7sy9k8TRNKbfqrIM7mhWUBM__Dzn3bgo2ZZdA1EvxWPK4mhLey9PSq7rEV_gwxRvw68Vr2jmhEfMmHcp9gvH5n3uDXQ_snEpbYaO4OZq-WTTv3jL6BOJWEKYlBDwYVan",
    "fwidth": "0",
    "sid": "6796260160550518784",
    "wxLang": "",
    "tcScale": "1",
    "uid": "",
    "cap_cd": "",
    "rnd": "740110",
    "TCapIframeLoadTime": "15",
    "prehandleLoadTime": "71",
    "createIframeStart": "1620354690227",
    "subsid": "12",
    "cdata": 0,
    "ans": "342,78;",
    "vsig": "",
    "websig": "",
    "subcapclass": ""
}
    js = fr.read()

ctx = execjs.compile(js)
# ctx.call('ttt',data)
print(ctx.call('ttt', data))