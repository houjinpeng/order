import requests,re,json
from lxml import etree
email_address_url='http://24mail.chacuo.net/'
session = requests.Session()
r = session.get(email_address_url)
doc = etree.HTML(r.text)
email_address = doc.xpath("//input[@id='converts']/@value")
email_address_net = email_address[0]+'@chacuo.net'

data = {'data':email_address[0],'type':'set','arg':'d=chacuo.nef_f='}
r= session.post(email_address_url,data=data)
data={'data':email_address[0],'type':'refresh','arg':''}
refresh=session.post(email_address_url,data=data)
content = json.loads(refresh.text)
mid = content['data'][0]['list'][0]['MID']

data = {'data':email_address[0],'type':'mailinfo','arg':'f='+str(mid)}
mailinfo = session.post(email_address_url,data=data)
code = mailinfo.text
code = re.findall(r'>(\d+)<', str(code))#验证码
print(code[0])