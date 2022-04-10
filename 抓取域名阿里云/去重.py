import time
with open('url.txt','r',encoding='utf-8') as fr:
    data = fr.readlines()

data = [d.strip() for d in data]
print(f'总数据{len(data)}个')
print(f'去重后的数据：{len(set(data))}个')

time.sleep(100)