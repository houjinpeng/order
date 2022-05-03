import datetime
import logging
import time
import requests
import json
import difflib


class JvCha():

    def __init__(self):
        # with open('../conf/敏感词.txt', 'r', encoding='utf-8') as fr:
        with open('./conf/敏感词.txt', 'r', encoding='utf-8') as fr:
            data = fr.readlines()
        self.word_list = []
        for d in data:
            self.word_list.append(d.strip())

    def get_token(self, domain_list):
        domain_token = []
        url = 'http://127.0.0.1:5001/get_token'
        r = requests.get(url)
        if json.loads(r.text) == '请更新token池':
            try:

                time.sleep(5)
            except Exception as e:
                logging.Logger.error('没有token了  请手动访问 http://127.0.0.1:5001/get_token_page 滑动验证码')
                time.sleep(10)
            return self.get_token(domain_list)
        token = json.loads(r.text)
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': '47.56.160.68:81',
            'Pragma': 'no-cache',
            'Proxy-Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'Origin': 'http://47.56.160.68:81',
            'Referer': 'http://47.56.160.68:81/piliang/',
            'X-Requested-With': 'XMLHttpRequest',
        }

        api = "http://47.56.160.68:81/api.php?sckey=y"
        data = {"ym": "\n".join(domain_list),
                "authenticate": token["auth"],
                "token": token['token'],
                "sessionid": token['session']
                }
        try:
            res = requests.post(url=api, data=data, headers=headers)
            res = res.json()
            if res['code'] != 1:
                print("错误: ", res['msg'])

                return self.get_token(domain_list)

            for item in res['data']:
                domain_token.append(item)
            return domain_token
        except Exception as e:
            print("[209]", e)
            return self.get_token(domain_list)

    def get_history(self, domain):
        try:

            headers = {
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Proxy-Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'http://47.56.160.68:81',
                'Host': '47.56.160.68:81',
            }

            data = {
                'ym': domain['ym'],
                'xq': 'y',
                'page': '1',
                'limit': '20',
                'token': domain['token'],
                'group': '1',
                'nian': ''
            }
            response_detail = requests.post('http://47.56.160.68:10015/api.php', data=data, verify=False,
                                            headers=headers, timeout=3)
            r = response_detail.json()

            results = {
                "count": r.get('count'),
                "data": r.get('data'),
                "code": r.get('code'),
                "msg": r.get('msg'),
            }

            # print(results)
            return results
        except:
            print('错误')
            return False

    def get_age(self, domain):
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Proxy-Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://47.56.160.68:81',
            'Host': '47.56.160.68:81',
        }
        data = {
            'ym': domain['ym'],
            'token': domain['token'],
            'qg': ''
        }
        try:
            response_detail = requests.post('http://47.56.160.68:10280/api.php', data=data, verify=False,
                                            headers=headers, timeout=3)
            results = response_detail.json()
            try:
                return results['data']['nl']
            except Exception as e:
                return 0
        except Exception as e:
            return self.get_age(domain)

    # 对比敏感词
    def check_mingan(self, history_data):
        '''
        :param history_data: 历史json
        :param mg_word: 敏感词列表
        :return: 返回是否有敏感词
        '''
        try:
            if history_data['data'] == None:
                return "无"
        except Exception as e:
            return "无"
        title_list = [title['bt'] for title in history_data['data']]

        for word in self.word_list:
            for title in title_list:
                if word in title:
                    return word
        return "无"

    def get_lianxu_cundang_time(self, history_data,year_num=0):
        '''
        获取连续年份时间
        :param history_data: 历史json
        :param year_num: 区间num
        :return: 最大连续时间
        '''
        num = 0
        old_year = 0
        max_lianxu_years = 1
        now_year = datetime.datetime.now().year
        try:
            for data in history_data['data']:
                year = int(data['timestamp'][:4])
                if year_num != 0:
                    if now_year - year_num > year:
                        continue
                if year + 1 == old_year:
                    num += 1
                    if num > max_lianxu_years:
                        max_lianxu_years += 1

                else:
                    num = 1
                old_year = year
            return max_lianxu_years
        except Exception as e:
            return max_lianxu_years

    def get_five_year_num(self, history_data):
        '''
        :param history_data: 历史json
        :return:  返回五年内建站次数
        '''
        try:
            now_year = datetime.datetime.now().year
            num = 0
            for data in history_data['data']:
                year = int(data['timestamp'][:4])
                if now_year - 5 <= year:
                    num += 1
            return num
        except Exception as e:
            return 0

    def get_zh_title_num(self, history_data):
        '''
        :param history_data: json 历史
        :return: 返回中文标题数量
        '''
        num = 0
        try:
            for data in history_data['data']:
                if data['yy'] == '中文':
                    num += 1
            return num
        except Exception as e:
            return 0

    def get_tongyidu(self,history_data):
        num = 1
        if history_data['data'] == None:
            return '0%'
        xiangsidu = 0
        for i in range(len(history_data['data'])):
            for j in range(i+1,len(history_data['data'])):
                num += 1
                xiangsidu += difflib.SequenceMatcher(None, history_data['data'][i], history_data['data'][j]).quick_ratio()

        xiangsidu = int(xiangsidu*100/num)
        return str(xiangsidu)+'%'

    def test(self):
        ds = ['baidu1.com', 'baidu1.com', 'baidu2.com', 'baidu3.com', 'baidu4.com']
        resp = self.get_token(ds)
        history_data = self.get_history(resp[0])

        print('敏感词：', self.check_mingan(history_data))
        print('中文标题数量：', self.get_zh_title_num(history_data))
        print('总建站年龄：', self.get_age(resp[0]))

        # 4.计算标题中所识别到的中文并计算统一度。 没写

        # 通过抓取聚查中的存档时间并计算近5年中所包含的年数数量。
        print('通过抓取聚查中的存档时间并计算近5年中所包含的年数数量：', self.get_five_year_num(history_data))

        # 获取最大连续时间
        print('获取最大连续时间：', self.get_lianxu_cundang_time(history_data))
        #相似度
        print('获取统一度：', self.get_tongyidu(history_data))


        # 计算存档时间里近5年内的连续的年份时间。
        print('5年内的连续的年份时间：', self.get_lianxu_cundang_time(history_data,year_num=5))

        #当前网址  http://www.jucha.com/lishi/
        print('当前网址','http://www.jucha.com/lishi/'+resp[0]['ym'])
        print(1)


if __name__ == '__main__':
    ds = ['baidu1.com', 'baidu1.com', 'baidu2.com', 'baidu3.com', 'baidu4.com']

    JvCha().test()
    # for domain in ['baidu.com','baidu.com','baidu.com','baidu.com']:
    # get_history(ds)
