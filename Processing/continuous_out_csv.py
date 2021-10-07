# -*- coding: UTF-8 -*-
# @Time : 2021/4/26 16:26
# @Author : HH
# @File : near_five_out_csv.py
# @Software: PyCharm
# @explain:导出csv文件   #分析近5年标题
import configparser
'''读写配置文件'''
config = configparser.ConfigParser()
# 文件路径
logFile = r"./setting.cfg"
config.read(logFile, encoding="utf-8")
config = config.defaults()
import difflib
import os
import csv

timeList = eval(config.get('timelist'))

def get_equal_rate(str1, str2):
   return difflib.SequenceMatcher(None, str1, str2).quick_ratio()

class OutCsv():
    def __init__(self,y):
        self.y = y
        self.year = int(config.get('year'))
        self.atyear = int(config.get('atyear'))
        self.title = config.get('title')
        self.unithood = config.get('unithood')
        self.nearfive = config.get('nearfive')
        for item in os.walk('.'):
            for i in item[2]:
                if 'his' in i :
                    self.filename = i
                    break
            break
        try:
            with open('./out/con-' + self.filename, 'r', encoding='utf-8') as fr:
                r = fr.readline()
            if '域名' not  in r :
                with open('./out/con-' + self.filename, 'a', encoding='utf-8') as fw:
                    fw.write("域名,语言,近5年建站,历史统一度,标题总数量,标题敏感词,域名年龄,快照时间-1,标题-1,快照时间-2,标题-2,快照时间-3,标题-3,快照时间-4,标题-4,快照时间-5,标题-5,快照时间-6,标题-6,快照时间-7,标题-7,快照时间-8,标题-8,快照时间-9,标题-9,快照时间-10,标题-10,快照时间-11,标题-11,快照时间-12,标题-12,快照时间-13,标题-13,快照时间-14,标题-14,快照时间-15,标题-15,快照时间-16,标题-16,快照时间-17,标题-17,快照时间-18,标题-18,快照时间-19,标题-19"+'\n')

        except Exception :
            with open('./out/con-' + self.filename, 'a', encoding='utf-8') as fw:
                fw.write("域名,语言,近5年建站,历史统一度,标题总数量,标题敏感词,域名年龄,快照时间-1,标题-1,快照时间-2,标题-2,快照时间-3,标题-3,快照时间-4,标题-4,快照时间-5,标题-5,快照时间-6,标题-6,快照时间-7,标题-7,快照时间-8,标题-8,快照时间-9,标题-9,快照时间-10,标题-10,快照时间-11,标题-11,快照时间-12,标题-12,快照时间-13,标题-13,快照时间-14,标题-14,快照时间-15,标题-15,快照时间-16,标题-16,快照时间-17,标题-17,快照时间-18,标题-18,快照时间-19,标题-19"+'\n')

    def openCsv(self):
        f = csv.reader(open(self.filename, 'r', encoding='utf-8'))
        return f

    def judge(self,data):

        n = 0
        y = 1
        timeIndex = []
        for t in timeList:
            try:
                if y == self.year:
                    break
                elif n == 0:
                    n = int(data[t])
                    timeIndex.append(t)
                elif n-1 == int(data[t]):
                    n = int(data[t])
                    y += 1
                    timeIndex.append(t)
                else:
                    y = 1
                    n = 0
                    timeIndex.clear()
            except Exception as e:
                n = 0
                y = 1

        if len(timeIndex) != self.year:
            return False

        if self.title == 'on':
            #判断时间前面的  如果都不等于 就返回data
            for t in timeIndex:
                try:
                    if data[t+1] == '':
                        return False
                except Exception as e:
                    pass
            return True
        else:
            return True

    def nearFive(self,data):

        i = 0
        for t in timeList:
            try:
                if self.atyear-5 <= int(data[t]) <= self.atyear  :
                    i += 1
            except Exception as e:
                pass
        return f'{str(i)}/5'

    def equalRate(self,data):
        if data[0] == '域名':
            return False
        diff = 0
        title_count = 0
        for t in timeList:
            if data[t + 1] != '' and data[t + 3] != '':
                d = get_equal_rate(data[t + 1],data[t+3])
                diff += d
                title_count += 1
        xsd = diff/title_count
        return f'{int(xsd*100)}%'

    def save_data(self,data):
        try:
            with open('./out/con-' + self.filename, 'a', encoding='utf-8') as fw:
                fw.write(','.join(data)+'\n')
        except Exception as e:
            pass

    def index(self):
        csv = self.openCsv()
        for data in csv:
            if self.y == 'continuous':
                if data[0] == '域名':
                    continue
                d = self.judge(data)
                if d == True:
                    print(data)
                    data.insert(2, '')
                    data.insert(3, '')
                    data = [i.replace(',', '，') for i in data]
                    self.save_data(data)




if __name__ == '__main__':
    OutCsv('continuous').index()

    # OutCsv(sys.argv[1]).index()