import requests

url = "https://beian.miit.gov.cn/"

payload={}
headers = {
  # 'Cookie': '__jsluid_s=7fd92c6c8e76847921fa9a69ee612e68'
}
proxies = {
            "http": "http://127.0.0.1:7890",
            "https": "http://127.0.0.1:7890",
        }

response = requests.request("GET", url, proxies=proxies,headers=headers, data=payload)

print(response.text)
