import requests
# proxies = {
#     "http": "http://user-sp68470966:maiyuan312@gate.dc.visitxiangtan.com:20000",
#     "https": "http://user-sp68470966:maiyuan312@gate.dc.visitxiangtan.com:20000",
# }
proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}

url = "https://seo.juziseo.com/snapshot/history/"
domain = 'baidu.com'
payload = f"post_hash=0ef479ae851d492123efbcc98ca80917&qr={domain}&qrtype=1&input_time=lastquery&start_time=&end_time=&fav=&history_score=0&lang=&age=0&title_precent=0&site_age=0&stable_count=0&stable_start_year_eq=&stable_start_year=&last_year_eq=&last_year=&site_5_age=0&site_5_stable_count=0&blocked=&gray=&gray_in_html=&site_gray=&baidu_site=0&gword=&has_snap=&per_page="
headers = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'accept-encoding': 'gzip, deflate, br',
  'accept-language': 'zh-CN,zh;q=0.9',
  'cache-control': 'no-cache',
  'content-length': str(len(payload)),
  'content-type': 'application/x-www-form-urlencoded',
  'cookie': 'juzufr=eJzLKCkpsNLXLy8v18sqrcosTs3XS87P1QcAZ9gIkQ%3D%3D; Hm_lvt_f87ce311d1eb4334ea957f57640e9d15=1650942544,1651458445; juz_Session=a56be4bab46m869juo5n3oisi3; juz_user_login=tb5oqZ8twzg%2FccksPbb0SYzGyBIAqTGSD4UbpK8Iy5OppN7hs5EaEyQojliNhgRh4zrX0dtRWpq8EO2vV7QaKx5yQRSCYIfan03IzYNBcgwhFEfFt7i5JNXWGybQ4A2qvclkPWSrQWwfxgSJ4C7%2FTQ%3D%3D; juzsnapshot=N; Hm_lpvt_f87ce311d1eb4334ea957f57640e9d15=1651543478',
  'origin': 'https://seo.juziseo.com',
  'pragma': 'no-cache',
  'referer':'https://seo.juziseo.com/snapshot/history/id-__qr-eJzLKk3MS0vNS6%2FKSMxL10vOzwUAPrwG1A%3D%3D__qrtype-1__input_time-lastquery.html',
  'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
}

response = requests.request("POST", url, headers=headers, data=payload,proxies=proxies,allow_redirects=False,verify=False)

url = response.headers._store['location'][1]

headers = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'accept-encoding': 'gzip, deflate, br',
  'accept-language': 'zh-CN,zh;q=0.9',
  'cache-control': 'no-cache',
  'cookie': 'juzufr=eJzLKCkpsNLXLy8v18sqrcosTs3XS87P1QcAZ9gIkQ%3D%3D; Hm_lvt_f87ce311d1eb4334ea957f57640e9d15=1650942544,1651458445; juz_Session=a56be4bab46m869juo5n3oisi3; juz_user_login=tb5oqZ8twzg%2FccksPbb0SYzGyBIAqTGSD4UbpK8Iy5OppN7hs5EaEyQojliNhgRh4zrX0dtRWpq8EO2vV7QaKx5yQRSCYIfan03IzYNBcgwhFEfFt7i5JNXWGybQ4A2qvclkPWSrQWwfxgSJ4C7%2FTQ%3D%3D; juzsnapshot=N; Hm_lpvt_f87ce311d1eb4334ea957f57640e9d15=1651544979',
  'pragma': 'no-cache',
  'referer': 'https://seo.juziseo.com/snapshot/history/id-__qr-eJzLKk3MS0vNS6%2FKSMxL10vOzwUAPrwG1A%3D%3D__qrtype-1__input_time-lastquery.html',
  'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
  'Content-Type': 'text/plain'
}

r = requests.get(url,headers=headers,proxies=proxies)
print(r.text)
