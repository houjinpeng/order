import datetime
import json
import sqlite3
import requests
import html as html_model
from export_excel import write_excel
from util import now_time

host = '127.0.0.1'
user = 'root'
passwd = '123456'
port = 3306
db = 'test'
class Export:

    def __init__(self):
        self.header = {}

    def query_all_links(self, start=None, num=None):
        con = sqlite3.connect("spider.db")
        cursor = con.cursor()
        # con = pymysql.connect(host=host, user=user, passwd=passwd, port=port, db=db)
        # cursor = con.cursor()
        if all([start, num]):
            start -= 1
            cursor.execute("select * from urls LIMIT %d, %d" % (start, num))
        else:
            cursor.execute("select * from urls")
        data = cursor.fetchall()

        cursor.close()
        con.close()

        return data

    def sensitive(self):
        words = []
        with open("敏感词.txt", encoding="UTF-8-sig") as f:
            rows = f.readlines()
            for row in rows:
                row = row.replace("\n", "")
                words.append(row)

        words = [x for x in words if x]
        return words

    def main(self):
        # page_check = input("是否开始快照检测 (y/n) 回车默认 n")
        # if page_check == 'y':
        #     page_check = True
        #     print("快照开启设置为: 启动")
        # else:
        #     page_check = False
        #     print("快照开启设置为: 关闭")

        page_check = False
        raw_data = self.query_all_links()
        if not raw_data:
            print(now_time(), "无需要导出的域名")
        nums = len(raw_data)

        start = int(input(f"总共{nums}条域名信息,开始位置 (1-{nums - 1})"))

        end = int(input(f"总共{nums}条域名信息,结束位置 ({start}-{nums})"))

        diff_num = end - start + 1

        raw_data = self.query_all_links(start, diff_num)

        res = []

        # 读取敏感词
        sensitive = self.sensitive()
        print(now_time(), "进行数据整理")
        for idx, item in enumerate(raw_data):
            print("总共", len(raw_data), "目前: ", idx)
            link, info, detail = item
            info = json.loads(info)
            detail = json.loads(detail)

            row_data = {}

            row_data['ym'] = link
            if isinstance(detail, list):
                detail = {'code': 1, 'data': detail}
            if detail == False:
                continue
            if info['code'] == -1 or detail['code'] == -1:
                row_data['code'] = -1

                res.append(row_data)
                continue

            row_data['code'] = 1
            row_data['title'] = html_model.unescape(info['data']['bt'])
            row_data['date_list'] = detail['data']

            # 记录数, 快照数
            row_data['record'] = info['data']['jls']

            # 检测语言
            langs = [x['yy'] for x in detail['data']]
            row_data['lang'] = '中文' if '中文' in langs else '其他'

            #年龄
            row_data['nl'] = info['data']['nl']

            # 主要语言
            row_data['yy'] = info['data']['yy']

            #最老记录
            row_data['sj_min'] = info['data']['sj_min']

            #最新记录
            row_data['sj_max'] = info['data']['sj_max']

            #域名年龄
            now_year = datetime.datetime.today().year
            if info['data']['sj_min']:
                min_year = int(info['data']['sj_min'][ :4])

                row_data['ym_nl'] = now_year - min_year
            else:
                row_data['ym_nl'] = '无法计算'

            # 敏感词检测
            title_word = '无'
            for page in detail['data']:

                for w in sensitive:
                    if w in row_data['title']:
                        title_word = w
                    if w in html_model.unescape(page['bt']):
                        title_word = w

            if not page_check:
                row_data['title_sensitive'] = title_word
                row_data['page_sensitive'] = '未进行页面敏感词检测'

                res.append(row_data)
                continue

            # 页面敏感词检测
            page_word = '无'
            import copy
            data_list = copy.copy(detail['data'])
            for page in data_list:
                jm = page['jm']
                try:
                    html = requests.get(f'http://47.56.160.68:81/api.php?dy=y&jm={jm}')
                    if html.status_code != 200:
                        print("请求异常,状态码:", html.status_code)
                        data_list.append(page)

                    html = html.text
                    for w in sensitive:
                        if w in html:
                            page_word = w
                            break

                    if page_word != '无':
                        break

                except Exception as e:
                    print(now_time(), "请求出错,重新请求")
                    data_list.append(page)


            row_data['title_sensitive'] = title_word
            row_data['page_sensitive'] = page_word

            res.append(row_data)
        print(now_time(), "数据整理完毕,准备写入EXCEL")

        write_excel(res)
        print(now_time(), "excel表格导出完毕!")


if __name__ == '__main__':
    Export().main()
