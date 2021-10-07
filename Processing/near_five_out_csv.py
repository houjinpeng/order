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
import jieba

seq_list = jieba.cut('',cut_all=False)

timeList = eval(config.get('timelist'))
def get_equal_rate(str1, str2):
   return difflib.SequenceMatcher(None, str1, str2).quick_ratio()

# print(get_equal_rate('武汉朝唐科技官方网站','武汉朝唐科技有限公司'))
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
                # else:
                #     self.filename = i
            break
        try:
            with open('./out/near-' + self.filename, 'r', encoding='utf-8') as fr:
                r = fr.readline()
            if '域名' not  in r :
                with open('./out/near-' + self.filename, 'a', encoding='utf-8') as fw:
                    fw.write("域名,语言,近5年建站,历史统一度,标题总数量,标题敏感词,域名年龄,快照时间-1,标题-1,快照时间-2,标题-2,快照时间-3,标题-3,快照时间-4,标题-4,快照时间-5,标题-5,快照时间-6,标题-6,快照时间-7,标题-7,快照时间-8,标题-8,快照时间-9,标题-9,快照时间-10,标题-10,快照时间-11,标题-11,快照时间-12,标题-12,快照时间-13,标题-13,快照时间-14,标题-14,快照时间-15,标题-15,快照时间-16,标题-16,快照时间-17,标题-17,快照时间-18,标题-18,快照时间-19,标题-19"+'\n')

        except Exception :
            with open('./out/near-' + self.filename, 'a', encoding='utf-8') as fw:
                fw.write("域名,语言,近5年建站,历史统一度,标题总数量,标题敏感词,域名年龄,快照时间-1,标题-1,快照时间-2,标题-2,快照时间-3,标题-3,快照时间-4,标题-4,快照时间-5,标题-5,快照时间-6,标题-6,快照时间-7,标题-7,快照时间-8,标题-8,快照时间-9,标题-9,快照时间-10,标题-10,快照时间-11,标题-11,快照时间-12,标题-12,快照时间-13,标题-13,快照时间-14,标题-14,快照时间-15,标题-15,快照时间-16,标题-16,快照时间-17,标题-17,快照时间-18,标题-18,快照时间-19,标题-19"+'\n')

        self.f = open('./out/near-' + self.filename, 'a', encoding='utf-8')

    def openCsv(self):
        f = csv.reader(open(self.filename, 'r', encoding='utf-8'))
        return f

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
        diff = 0
        title_count = 0
        # for t in range(len(timeList)):
        #     for i in range(t+1,len(timeList)):
        #         if data[timeList[t]+1] != '' or data[timeList[i]+1] != '':
        #             d = get_equal_rate(data[timeList[t] + 1], data[timeList[i] + 1])
        #             diff += d
        #             title_count += 1
        #         else:
        #             break
        #     break


        try:
            for t in timeList:
                if data[t + 1] == '':
                    break
                elif data[t + 1] != '' and data[t + 3] != '':
                    d = get_equal_rate(data[t + 1],data[t+3])
                    diff += d
                    title_count += 1
                else:
                    break
        except Exception as e:
            print(e)

        try:
            xsd = diff/title_count
        except Exception as e:
            xsd = 0
        return f'{int(xsd*100)}%'

    def save_data(self,data):
        self.f.write(','.join(data)+'\n')


        # try:
        #     with open('./out/near-' + self.filename, 'a', encoding='utf-8') as fw:
        #         fw.write(','.join(data)+'\n')
        # except Exception as e:
        #     pass

    def index(self):
        csv = self.openCsv()
        for data in csv:
            if self.y != 'continuous':
                # 根据年份来判断是否符合标准
                if data[0] == '域名':
                    continue
                d = self.nearFive(data)

                rate = self.equalRate(data)

                data.insert(3, rate)
                data.insert(2, d)
                print(data)
                data = [i.replace(',', '，') for i in data]
                self.save_data(data)

        self.f.close()

if __name__ == '__main__':

    OutCsv(1).index()
    # OutCsv(sys.argv[1]).index()