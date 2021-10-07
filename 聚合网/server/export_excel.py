# -*- coding:utf-8 -*-
import html
import xlwt
import time
import csv

result_name = "history" + '-' + str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
headers = ['域名', '语言', '标题总数量', '标题敏感词', '域名年龄',
           "快照时间-1", '标题-1',
           ]
for i in range(2, 20):
    headers.append(f"快照时间-{i}")
    headers.append(f"标题-{i}")


# 设置表格样式
def set_style(name, height, bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

def set_header():
    '''
    设置标题
    '''
    
    global headers
    global result_name
    detail_f = open('./taskdata/' + result_name + '.csv', 'a+', newline='', encoding='utf-8')
    csv_f = csv.DictWriter(detail_f, headers)
    csv_f.writeheader()
    
    filename = './taskdata/' + result_name + '.csv'
    with open(filename, 'a+', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            if reader.line_num == 1 and '域名' in row and '语言' in row:
                return True
            else:
                print("标题不存在, 新建标题")
                # csv_f = csv.DictWriter(reader, headers)
                # csv_f.writeheader()
                

def write_excel(rows):
    # filename = './taskdata/' + result_name + '.csv'
    # with open(filename, 'r+') as f:
    #      reader = csv.reader(f)
    #      if not set_header(reader):
    #         print("导出失败")
    #         return False
    set_header()
    global headers

    row_mount = 1
    # 标题数
    title_nums = []
    for row in rows:
        
        detail_f = open('./taskdata/' + result_name + '.csv', 'a', newline='', encoding='utf-8')
        # 域名  百度评价   时间
        csv_f = csv.DictWriter(detail_f, headers)
        
        d = dict()
        d["域名"] = row['ym']
        d["标题总数量"] = row['record']
        d["标题敏感词"] = row['title_sensitive']
        d["域名年龄"] = row['ym_nl']
        

    #     if row['code'] == -1:
    #         sheet1.write(row_mount, 0, ym)
    #         row_mount += 1
    #         continue
    #     # 标题数量
    #     mb_row = row_mount + len(row['date_list']) - 1

    #     # 写入域名
    #     # sheet1.write_merge(row_mount, mb_row, 0, 0, ym)
    #     sheet1.write(row_mount, 0, ym)

    #     # 写入记录数, 快照数, 标题总数量
    #     sheet1.write(row_mount, 2, row['record'])

    #     # 标题敏感词
    #     sheet1.write(row_mount, 3, row['title_sensitive'])

    #     # # 页面敏感词
    #     # sheet1.write(row_mount, 4, row['page_sensitive'])

    #     # 域名年龄
    #     sheet1.write(row_mount, 4, row['ym_nl'])

    #     # # 最老记录
    #     # sheet1.write(row_mount, 6, row['sj_min'])

    #     # # 最新记录
    #     # sheet1.write(row_mount, 7, row['sj_max'])

        # 主要语言
        # # # # 标题中只要是存在一条中文就算中文   全是英文语言就是英文，识别不出来按其它
        lang = []
        for date_list in row['date_list']:
            lang.append(date_list['yy'])

        if "中文" in lang:
            # sheet1.write_merge(row_mount, mb_row, 1, 1, "中文")
            # sheet1.write(row_mount, 1, "中文")
            d["语言"] = "中文"

        elif "中文" not in lang:
            lang_y = list(set(lang))
            if "英文" in lang and len(lang_y) == 1:
                # sheet1.write_merge(row_mount, mb_row, 1, 1, "英文")
                # sheet1.write(row_mount, 1, "英文")
                d["语言"] = "英文"
            else:
                # lang_y.remove("英文")
                # sheet1.write_merge(row_mount, mb_row, 1, 1, lang_y.pop())
                # sheet1.write(row_mount, 1, "其他")
                d["语言"] = "其他"

        # 各个标题数量添加列表, 找出最大的标题数量
        title_nums.append(len(row['date_list']))

        # 根据时间进行排序
        for j in range(len(row['date_list']) - 1, 0, -1):
            for i in range(j):
                if row['date_list'][i]['timestamp'] < row['date_list'][i + 1]['timestamp']:
                    row['date_list'][i + 1], row['date_list'][i] = row['date_list'][i], row['date_list'][i + 1]

        # # 根据标题数量, 重新写入第一行
        for t in range(1, max(title_nums) + 1):
            if f'快照时间-{t}' in headers and f'标题-{t}':
                continue
            else:
                headers.append(f'快照时间-{t}')
                headers.append(f'标题-{t}')
            # csv_f.writeheader()

        for i in range(1, len(row['date_list']) + 1):
            # 写入存档时间
            data = row['date_list'].pop(0)
            d[f"快照时间-{i}"] = data.get('timestamp')[:4]
            d[f"标题-{i}"] = html.unescape(data.get('bt').replace("\n", ""))
        csv_f.writerow(d)
        
        
       

    #     # # 写入网站标题
    #     # sheet1.write_merge(row_mount, mb_row, 1, 1, row['title'])
    #     # # 检测语言
    #     # sheet1.write_merge(row_mount, mb_row, 5, 5, row['lang'])
    #     # # 使用年龄
    #     # sheet1.write_merge(row_mount, mb_row, 6, 6, row['nl'])
    #     # # 主要语言
    #     # sheet1.write_merge(row_mount, mb_row, 7, 7, row['yy'])
    #     # # 最老记录
    #     # sheet1.write_merge(row_mount, mb_row, 8, 8, row['sj_min'])
    #     # # 最新记录
    #     # sheet1.write_merge(row_mount, mb_row, 9, 9, row['sj_max'])
    #     # # 标题敏感词
    #     # sheet1.write_merge(row_mount, mb_row, 11, 11, row['title_sensitive'])
    #     # # 页面敏感词
    #     # sheet1.write_merge(row_mount, mb_row, 12, 12, row['page_sensitive'])
    # f.save(f'{int(time.time())}.xls')
    
    detail_f.close()
