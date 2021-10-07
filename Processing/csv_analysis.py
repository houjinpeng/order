# -*- encoding=utf8 -*-

import csv
import time


def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
        else:
            return False

def simil_data(infos):
    """
    相似数据
    """
    b = []
    d = []
    e = []
    for l in infos:
        t = ""
        for x in l:
            if x not in t:
                t += x
        e.append(t)
    
    for c in "".join(e):
        if check_contain_chinese(c) and c not in b:
            b.append(c)
            
    key_word = ""
    for c in b:
        num = 0
        for o in e:
            if c in o:
                num += 1
        
        if num >= 2:
            key_word = key_word + c
        else:
            continue
    
    if key_word:
        print(infos)
        # print("e", e)
        # print("b", b)
        print("关键字: ", key_word, e)
        print()
        with open("result.txt", 'a+', encoding='gbk') as f:
            f.write(str(key_word))
            f.write(" | ")
            f.write(str(infos))
            f.write("\n")
            f.write("\n")


with open('history-2021-04-25.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i == 0:
            continue
        info = list(set(row))
        info.remove('')
        temp = []
        for t in info:
            # 判断是否全是数字
            if len(t) < 2:
                continue
            if t.isdigit():
                continue
            if t.replace('.', '').isalpha():
                continue
            if ".com" in t or ".cn" in t:
                continue
            temp.append(t)

        if len(temp) >= 2:
            simil_data(temp)
