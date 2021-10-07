# 557747
# qq123123

# 301111
# hamigua10086
import logging
import time
import datetime
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import hashlib
import requests
from longin import Login
import re
import json
from logging import handlers

# cookie = 'gr_user_id=369b158e-a04d-471e-a6af-91be2682116e; UM_distinctid=17c2a784b74f57-0041c7813c00c-a7d173c-1fa400-17c2a784b75490; _qddaz=QD.oeyvft.ibtdvl.ku3j0sao; laiyuan=7a08c112cda6a063.juming.com; PHPSESSID=87168vpmt4conc8m66s0a5fmpf; Hm_lvt_f94e107103e3c39e0665d52b6d4a93e7=1632907515,1632968010,1632968149,1632968152; Hm_lpvt_f94e107103e3c39e0665d52b6d4a93e7=1632974188; a801967fdbbbba8c_gr_session_id=002e2d35-dfa0-421f-9326-8bfd91dd57cc; a801967fdbbbba8c_gr_session_id_002e2d35-dfa0-421f-9326-8bfd91dd57cc=true; Juming_uid=301111; Juming_isapp=0; Juming_zhu=5a8a35b6277a1f860b564557d98051b5; Juming_jf=1942f3cf22a5313fdf60b60f888aa18b; Juming_qy=5e18c6e710d098bdcb6956af22285eee'
session = requests.session()

doamin_dict = {}
jingjia_dict = {}
# 读取预算

yd = []
old_domain_set = set()
new_domain_set = set()

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '45',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': '7a08c112cda6a063.juming.com:9696',
    'Origin': 'http://7a08c112cda6a063.juming.com:9696',
    'Referer': 'http://7a08c112cda6a063.juming.com:9696/p/9889689/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
headers3 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'cookie': cookie,
    'Host': '7a08c112cda6a063.juming.com:9696',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
}

def get_minute(time_str):
    date_time = ''
    if time_str == '即将结束':
        date_time = datetime.datetime.strptime('01分10秒', '%M分%S秒')
        return date_time
    try:
        date_time = datetime.datetime.strptime(time_str, '%H小时%M分')
    except Exception as error:
        pass
    try:
        date_time = datetime.datetime.strptime(time_str, '%M分%S秒')
    except Exception as error:
        pass
    try:
        date_time = datetime.datetime.strptime(time_str, '%H小时%S秒')
    except Exception as error:
        pass
    if date_time == '':
        return ''
    return date_time
# 读取设置
try:
    with open('./config/setting.ini', 'r', encoding='utf-8') as fr:
        data = fr.read()
    d = json.loads(data)
except Exception:
    d= {"user_id":"301111",
        "password": "hamigua10086",
        "refresh_time": "10",
        "max_price": "1",
        'is_tongyi':'',
        'tongyi1':'',
        'tongyi2':'',
        'is_fenbie':'',
        'guding1':'',
        'guding2':'',
        'buguding1': '',
        'buguding2': '',
        'yincang':'',
        'is_status':'finish'
    }



class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, filename, level='info', when='D', backCount=3,
                 fmt='%(asctime)s - [line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,
                                               encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)

limit = 100
log = Logger('./config/域名竞价.log', level='debug')
password_md5 = ''

try:
    user_id = d['user_id']
    password = d['password']
except Exception :
    user_id = ''
    password = ''
# pyqt5 出价线程
class ChuJiaJob(QtCore.QThread):
    signal = pyqtSignal(dict)

    def __init__(self, data_list,tableWidget):
        super(ChuJiaJob, self).__init__()
        self.data_list = data_list
        self.tableWidget = tableWidget
        self.name = 'chujia_job'


    def request_headler(self, url, headers, method='get', data=None):
        if method == 'post':
            try:
                resp = session.post(url, headers=headers, data=data, timeout=10)
                return resp
            except Exception as e:
                return self.request_headler(url, headers, method, data)
        else:
            try:
                resp = session.get(url, headers=headers, timeout=10)
                if '保密' in resp.text:
                    log.logger.debug('需要重新登陆')
                return resp
            except Exception as e:
                return self.request_headler(url, headers=headers)

    def run(self):
        global headers
        global header3
        token_url = 'http://7a08c112cda6a063.juming.com:9696/user/#/qiang_jj'
        resp = self.request_headler(token_url, headers=headers3)
        token = re.findall("token='(.*?)'",resp.text)[0]

        url = 'http://7a08c112cda6a063.juming.com:9696/p/chujia'
        try:
            data = f'csrf_token={token}&id={self.data_list[0]}&jg={self.data_list[10]}'
            headers['Referer'] = f'http://7a08c112cda6a063.juming.com:9696/p/{self.data_list[0]}/'
            headers['Content-Length'] = str(len(data))
            resp = self.request_headler(url, headers=headers, data=data, method='post')

            if json.loads(resp.text)['msg'] == '出价成功！':
                log.logger.debug(json.loads(resp.text))
                #更改状态
                row_count  = self.tableWidget.rowCount()
                for row in range(row_count):
                    if self.tableWidget.item(row,1).text() == self.data_list[1]:
                        # # 添加数据 状态
                        # new_item = QTableWidgetItem('领先')
                        # new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                        # self.tableWidget.setItem(row, 8, new_item)
                        # new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)
                        #
                        # # 添加数据 领先金额
                        # new_item = QTableWidgetItem(str(self.data_list[10]))
                        # new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                        # self.tableWidget.setItem(row, 3, new_item)
                        # new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)
                        self.data_list[8] = '领先'
                        self.data_list[3] = str(self.data_list[10])
                        self.signal.emit({'row': row, 'data_list': self.data_list})
                        break
            else:
                log.logger.debug(json.loads(resp.text))
        except Exception as e:
            pass


# pyqt5 监控
class TableJob(QtCore.QThread):
    signal = pyqtSignal(list)

    def __init__(self,table):
        self.table = table
        self.name = 'table_job'

        super(TableJob, self).__init__()

    def request_headler(self, url, headers, method='get', data=None):
        if method == 'post':
            try:
                resp = session.post(url, headers=headers, data=data, timeout=10)
                return resp
            except Exception as e:
                return self.request_headler(url, headers, method, data)
        else:
            try:
                resp = session.get(url, headers=headers, timeout=10)
                if '保密' in resp.text:
                    log.logger.debug('需要重新登陆')
                return resp
            except Exception as e:
                return self.request_headler(url, headers=headers)

    def run(self):
        global jingjia_dict
        global old_domain_set
        global new_domain_set
        while True:
            new_domain_set = set()
            old_domain_set = set()
            # self.table.setRowCount(0)
            #在这里把以前的数据收到old里  然后去对比新的
            table_row = self.table.rowCount()
            for row in range(table_row):
                old_domain_set.add(self.table.item(row,1).text())

            url = f'http://7a08c112cda6a063.juming.com:9696/user_main/jj_list?page=1&limit={limit}&myjj=1'
            # resp = self.request_headler(url, method='post', data=data, headers=self.headers2)
            resp = self.request_headler(url, headers=headers3)
            try:
                all_domain = json.loads(resp.text)['data']
            except Exception as e:
                all_domain = []
            #整理出所有域名列表  每次都要更新
            for domain in all_domain:
                is_guding = '不固定' if '不固定' in domain['dl_ts'] else '固定'
                try:
                    jingjia_dict[ym]['is_guding'] = is_guding
                except Exception as e:
                    pass
                id = domain['id']
                ym = domain['ym']
                lx_price = domain['qian'] #领先金额
                sytime = domain['shengsj_sc'] #剩余时间
                endtime = domain['jssj'] #结束时间
                status = '落后' if domain['iflx'] == 0 else '领先'
                ticheng = f"{domain['wbqian']} / {domain['tc_num']}"  #代理
                remark = domain['bz']
                shiji_price = domain['qian'] - domain['tc_num'] #实际金额
                chujia = domain['zdqian']  #出价金额
                max_price = d['max_price']  #预设价
                #如果选择隐藏  把不需要的都隐藏掉   预设价 >= 实际价格添加

                if d['yincang'] == '2':
                    # if 最大额度+100 >= 实际的金额
                    if int(max_price)+100 >= shiji_price:
                        new_domain_set.add(ym)
                        self.signal.emit([id, ym, remark, lx_price, shiji_price, ticheng, sytime, endtime, status, max_price,chujia])
                    elif status == '领先':
                        self.signal.emit([id, ym, remark, lx_price, shiji_price, ticheng, sytime, endtime, '领先', max_price,chujia])
                        new_domain_set.add(ym)
                        continue
                else:
                    #不隐藏的情况下判断是否超预算
                    if shiji_price > int(max_price) and status != '领先':
                        self.signal.emit([id, ym, remark, lx_price, shiji_price, ticheng, sytime, endtime, '已停止，超出预算', max_price,chujia])
                        new_domain_set.add(ym)
                        continue
                    new_domain_set.add(ym)
                    self.signal.emit([id, ym, remark, lx_price, shiji_price, ticheng, sytime, endtime, status, max_price,chujia])
            if old_domain_set == set():
                continue

            chaji = old_domain_set.difference(new_domain_set)
            #查找差集 删除差集中的数据
            for c in chaji:
                table_row = self.table.rowCount()
                for row in range(table_row):
                    try:
                        if self.table.item(row,1).text() == c:
                            jingjia_dict.pop(c, '404')
                            print(f'删除{c}')
                            self.table.removeRow(row)
                    except Exception as error:
                        pass

            table_row = self.table.rowCount()
            for row in range(table_row):
                try:
                    ym = self.table.item(row, 1).text()
                    if jingjia_dict.get(ym) == None:
                        jingjia_dict[ym] = {}
                    jingjia_dict[ym]['id'] = self.table.item(row, 0).text()
                    jingjia_dict[ym]['ym'] = ym
                    jingjia_dict[ym]['lx_price'] = self.table.item(row, 3).text()
                    jingjia_dict[ym]['shiji_price'] = self.table.item(row, 4).text()
                    jingjia_dict[ym]['ticheng'] = self.table.item(row, 5).text()
                    jingjia_dict[ym]['sytime'] = self.table.item(row, 6).text()
                    jingjia_dict[ym]['endtime'] = self.table.item(row, 7).text()
                    jingjia_dict[ym]['status'] = self.table.item(row, 8).text()
                    jingjia_dict[ym]['max_price'] = self.table.item(row, 9).text()
                    jingjia_dict[ym]['chujia'] = self.table.item(row, 10).text()
                    jingjia_dict[ym]['row_index'] = row

                except Exception:
                    continue

            time.sleep(int(d['refresh_time']))


class PlaceJob(QtCore.QThread):
    signal = pyqtSignal(bool)

    def __init__(self, tableWidget):
        super(PlaceJob, self).__init__()
        self.tableWidget = tableWidget
        self.name = 'place_job'


    def request_headler(self, url, headers, method='get', data=None):
        if method == 'post':
            try:
                resp = session.post(url, headers=headers, data=data, timeout=10)
                return resp
            except Exception as e:
                return self.request_headler(url, headers, method, data)
        else:
            try:
                resp = session.get(url, headers=headers, timeout=10)
                if '保密' in resp.text:
                    log.logger.debug('需要重新登陆')
                return resp
            except Exception as e:
                return self.request_headler(url, headers=headers)

    def bid(self,id, chujia):
        global headers3
        global headers
        token_url = 'http://7a08c112cda6a063.juming.com:9696/user/#/qiang_jj'
        resp = self.request_headler(token_url, headers=headers3)
        token = re.findall("token='(.*?)'", resp.text)[0]
        url = 'http://7a08c112cda6a063.juming.com:9696/p/chujia'
        try:
            data = f'csrf_token={token}&id={id}&jg={chujia}'
            headers['Referer'] = f'http://7a08c112cda6a063.juming.com:9696/p/{id}/'
            headers['Content-Length'] = str(len(data))
            resp = self.request_headler(url, headers=headers, data=data, method='post')
            if json.loads(resp.text)['msg'] == '出价成功！':
                log.logger.debug(json.loads(resp.text))
                return True
            elif '出价失败，请至少出价' in json.loads(resp.text)['msg']:
                log.logger.debug(json.loads(resp.text))
                chujia = re.findall('\d+', json.loads(resp.text)['msg'])[0]
                return self.bid(id,chujia)
            else:
                log.logger.debug(json.loads(resp.text))

        except Exception as e:
            log.logger.error(e)

    def check_and_place(self,value,shiji_price,chujia,key):
        # 去竞价   之后要修改状态  更改领先金额
        log.logger.debug(f'{value["id"]} {value["ym"]} 出价为：{value["chujia"]} 实际需付：{shiji_price}')
        is_succeed = self.bid(value['id'], value['chujia'])
        if is_succeed == True:
            # 更改状态
            row_count = self.tableWidget.rowCount()
            for row in range(row_count):
                if self.tableWidget.item(row, 1).text() == value['ym']:
                    # 添加数据 状态
                    new_item = QTableWidgetItem('领先')
                    new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.tableWidget.setItem(row, 8, new_item)
                    new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)

                    # 添加数据 领先金额
                    new_item = QTableWidgetItem(str(chujia))
                    new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.tableWidget.setItem(row, 3, new_item)
                    new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)

                    jingjia_dict[key]['status'] = '领先'
                    jingjia_dict[key]['lx_price'] = str(chujia)

    def run(self):
        global jingjia_dict
        while True:
            if d['is_status'] == 'finish':
                time.sleep(1)
                continue
            try:
                for key,value in jingjia_dict.items():
                    try:
                        if value['status'] != '落后':
                            continue
                    except Exception as e:
                        log.logger.error(e)
                        continue

                    #获取剩余时间
                    date_time = get_minute(value['sytime'])
                    if date_time == '':
                        continue
                    minute = date_time.minute
                    hour = date_time.hour
                    # 剩余时间小于设置的时间
                    sy_shijian = hour * 60 + minute

                    # 去出价判断  读取设置是否是统一 还是固定不固定
                    #首先判断是否在预算内
                    #如果是分别的
                    # 判断额度    实际需付 = 出价价格- ((出价价格-代理显示价格)*60%)
                    daili_price = int(value['ticheng'].split('/')[0].strip())
                    chujia = int(value['chujia'])
                    shiji_price = chujia - (chujia - daili_price) * 0.6
                    if d['is_fenbie'] == '2':
                        try:
                            #获取固定和不固定的时间
                            if jingjia_dict[key].get('is_guding') == '固定':
                                if int(d['guding1']) <= sy_shijian <= int(d['guding2']):
                                    self.check_and_place(value,shiji_price,chujia,key)

                            elif jingjia_dict[key].get('is_guding') == '不固定':
                                if int(d['buguding1']) <= sy_shijian <= int(d['buguding2']):
                                    self.check_and_place(value,shiji_price,chujia,key)
                        except Exception :
                            pass

                    else:
                        #判断时间
                        if int(d['tongyi1']) <= sy_shijian <= int(d['tongyi2']):
                            # #判断额度    实际需付 = 出价价格- ((出价价格-代理显示价格)*60%)
                            # daili_price = int(value['ticheng'].split('/')[0].strip())
                            # chujia = int(value['chujia'])
                            # shiji_price = chujia - (chujia-daili_price)*0.6
                            #判断金额
                            if int(d['max_price']) >= shiji_price and value['status'] == '落后':
                               self.check_and_place(value,shiji_price,chujia,key)

                time.sleep(5)
            except Exception as e:
                print(e)
                time.sleep(10)
                pass


class InItTable(QtCore.QThread):
    signal = pyqtSignal(dict)

    def __init__(self,table):
        self.table = table
        self.name = 'init_table'
        super(InItTable, self).__init__()

    def request_headler(self, url, headers):
        try:
            resp = session.get(url, headers=headers, timeout=10)
            if '保密' in resp.text:
                log.logger.debug('需要重新登陆')
            return resp
        except Exception as e:
            return self.request_headler(url, headers=headers)

    def run(self):
        url = f'http://7a08c112cda6a063.juming.com:9696/user_main/jj_list?page=1&limit={limit}&myjj=1'
        resp = self.request_headler(url, headers=headers3)
        try:
            all_domain = json.loads(resp.text)['data']
        except Exception as e:
            all_domain = []
        self.table.setRowCount(0)
        #整理出所有域名列表  每次都要更新
        for domain in all_domain:
            self.signal.emit(domain)


class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        初始化UI
        :return:
        """
        self.setObjectName("loginWindow")
        self.setStyleSheet('#loginWindow{background-color:white}')
        self.setFixedSize(650, 400)
        self.setWindowTitle("登录")
        self.setWindowIcon(QIcon('static/juming_ico.ico'))

        self.text = "聚名用户登录"

        # 添加顶部logo图片
        pixmap = QPixmap("static/3.png")
        scaredPixmap = pixmap.scaled(850, 140)
        label = QLabel(self)
        label.setPixmap(scaredPixmap)

        # 绘制顶部文字
        lbl_logo = QLabel(self)
        lbl_logo.setText(self.text)
        lbl_logo.setStyleSheet("QWidget{color:white;font-weight:600;background: transparent;font-size:30px;}")
        lbl_logo.move(250, 50)
        lbl_logo.setAlignment(Qt.AlignCenter)
        lbl_logo.raise_()

        # 登录表单内容部分
        login_widget = QWidget(self)
        login_widget.move(0, 140)
        login_widget.setGeometry(0, 140, 650, 260)

        hbox = QHBoxLayout()
        # 添加左侧logo
        logolb = QLabel(self)
        logopix = QPixmap("static/logo.png")
        logopix_scared = logopix.scaled(100, 100)
        logolb.setPixmap(logopix_scared)
        logolb.setAlignment(Qt.AlignCenter)
        hbox.addWidget(logolb, 1)
        # 添加右侧表单
        self.fmlayout = QFormLayout()
        self.lbl_workerid = QLabel("用户名")
        self.led_workerid = QLineEdit(user_id)
        self.led_workerid.setFixedWidth(270)
        self.led_workerid.setFixedHeight(38)

        self.lbl_pwd = QLabel("密码")
        self.led_pwd = QLineEdit(password)
        self.led_pwd.setEchoMode(QLineEdit.Password)
        self.led_pwd.setFixedWidth(270)
        self.led_pwd.setFixedHeight(38)

        btn_login = QPushButton("登录")
        btn_login.setFixedWidth(270)
        btn_login.setFixedHeight(40)
        btn_login.setFont(QFont("Microsoft YaHei"))
        btn_login.setObjectName("login_btn")
        btn_login.setStyleSheet("#login_btn{background-color:#2c7adf;color:#fff;border:none;border-radius:4px;}")
        btn_login.clicked.connect(self.login)
        self.msg = QLabel()
        self.fmlayout.addRow(self.msg)


        self.fmlayout.addRow(self.lbl_workerid, self.led_workerid)
        self.fmlayout.addRow(self.lbl_pwd, self.led_pwd)
        self.fmlayout.addWidget(btn_login)
        hbox.setAlignment(Qt.AlignCenter)



        # 调整间距
        self.fmlayout.setHorizontalSpacing(20)
        self.fmlayout.setVerticalSpacing(12)

        hbox.addLayout(self.fmlayout, 2)

        login_widget.setLayout(hbox)

        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def login(self):
        global password_md5
        global session
        global user_id
        global password
        user_id = self.led_workerid.text()
        password = self.led_pwd.text()
        m = hashlib.md5()
        m1 = hashlib.md5()
        m.update(f'[jiami{password}mima]'.encode())
        m1.update(m.hexdigest()[0:19].encode())
        password_md5 = m1.hexdigest()[0:19]

        session,msg = Login(f're_mm={password_md5}&re_yx={user_id}&re_yzm=').index()
        if msg['code'] == -1:
            self.msg.setText(f'<font color="red">{msg["msg"]}</font>')
            return
        with open('./config/setting.ini','w',encoding='utf-8') as fw:
            d['user_id'] = user_id
            d['password'] = password
            fw.write(json.dumps(d))

        self.hide()
        self.f = Bidding()
        self.f.show()


class Bidding(QWidget):
    def __init__(self):
        super().__init__()
        self.thread_list = []

        self.initUI()
        if d['is_tongyi'] == '2':
            self.is_tongyi.setChecked(True)
            self.set_is_tongyi()
        else:
            self.is_fenbie.setChecked(True)
            self.set_is_fenbie()
        if d['yincang'] == '2':
            self.is_box.setChecked(True)
        else:
            self.is_box.setChecked(False)

        self.init_table_job()
        self.TableJob = TableJob(self.tableWidget)
        self.TableJob.signal.connect(self.get_table_data)
        self.TableJob.start()
        self.thread_list.append(self.TableJob)

    #ui
    def initUI(self):
        # 整数校验器[1,99]
        intValidator = QIntValidator(self)
        intValidator.setRange(1, 1000)

        self.resize(1250, 800)
        self.setWindowTitle('聚名域名竞价')
        self.setWindowIcon(QIcon('./static/juming_ico.ico'))
        self.grid = QGridLayout()

        self.grid.setSpacing(20)
        self.setLayout(self.grid)
#################################################################################

        self.is_tongyi = QCheckBox()
        self.is_tongyi.clicked.connect(self.set_is_tongyi)

        self.grid.addWidget(self.is_tongyi, 1, 0)
        #出价时间设置
        self.chujia_time_t = QLabel("出价时间设置/分")
        self.grid.addWidget(self.chujia_time_t, 1, 1)

        # 统一出价时间
        self.chujia_time_t = QLabel("统一出价")
        self.grid.addWidget(self.chujia_time_t, 2, 0)

        self.chujia_time1 = QLineEdit(d['tongyi1'])
        self.chujia_time1.setPlaceholderText("输入整数")
        self.chujia_time1.setValidator(intValidator)
        self.grid.addWidget(self.chujia_time1, 2, 1)

        a = QLabel("-")
        self.grid.addWidget(a, 2, 2)


        self.chujia_time2 = QLineEdit(d['tongyi2'])
        self.chujia_time2.setPlaceholderText("输入整数")
        self.chujia_time2.setValidator(intValidator)
        self.grid.addWidget(self.chujia_time2, 2, 3)
##############################################################################
        self.is_fenbie = QCheckBox()
        self.is_fenbie.clicked.connect(self.set_is_fenbie)

        self.grid.addWidget(self.is_fenbie, 3, 0)
        #分别出价
        self.fenbie_t = QLabel("分别出价/分")
        self.grid.addWidget(self.fenbie_t, 3, 1)

        guding = QLabel("外部固定：")
        self.grid.addWidget(guding, 4, 0)

        self.guding_time1 = QLineEdit(d['guding1'])
        self.guding_time1.setPlaceholderText("输入整数")
        self.guding_time1.setValidator(intValidator)
        self.grid.addWidget(self.guding_time1, 4, 1)

        a = QLabel("-")
        self.grid.addWidget(a, 4, 2)

        self.guding_time2 = QLineEdit(d['guding1'])
        self.guding_time2.setPlaceholderText("输入整数")
        self.guding_time2.setValidator(intValidator)
        self.grid.addWidget(self.guding_time2, 4, 3)

        buguding = QLabel("外部不固定：")
        self.grid.addWidget(buguding, 5, 0)


        self.buguding_time1 = QLineEdit(d['buguding1'])
        self.buguding_time1.setPlaceholderText("输入整数")
        self.buguding_time1.setValidator(intValidator)
        self.grid.addWidget(self.buguding_time1, 5, 1)

        b = QLabel("-")
        self.grid.addWidget(b, 5, 2)

        self.buguding_time2 = QLineEdit(d['buguding2'])
        self.buguding_time2.setPlaceholderText("输入整数")
        self.buguding_time2.setValidator(intValidator)
        self.grid.addWidget(self.buguding_time2, 5, 3)

        ##########################################################################################
        #价格设置
        self.max_price_t = QLabel("价格设置/元(实际需付)")
        self.grid.addWidget(self.max_price_t, 1, 4,1,6)
        #统一出价
        self.tongyi_chujia = QLabel("统一出价：")
        self.grid.addWidget(self.tongyi_chujia, 2, 4)

        self.max_price = QLineEdit(d['max_price'])
        self.max_price.setPlaceholderText("输入整数")
        self.max_price.setValidator(intValidator)
        self.grid.addWidget(self.max_price, 2, 5)

        # 导入价格
        self.daoru = QLabel("导入价格：")
        self.grid.addWidget(self.daoru, 3, 4)
        #
        self.btn2 = QPushButton('选择预算文件')
        self.btn2.clicked.connect(self.yusuan_file)
        self.grid.addWidget(self.btn2, 3, 5)


        # ##########################################################################################
        # 刷新设置
        self.refresh = QLabel("刷新设置/秒")
        self.grid.addWidget(self.refresh, 1, 7)
        #
        self.refresh_time_q = QLabel("自动刷新：")
        self.grid.addWidget(self.refresh_time_q, 2, 7)


        self.refresh_time = QLineEdit(d['refresh_time'])
        self.refresh_time.setPlaceholderText("输入整数")
        self.refresh_time.setValidator(intValidator)
        self.grid.addWidget(self.refresh_time, 2, 8)

        #手动刷新按钮
        self.shou_refresh = QPushButton('手动刷新')
        self.shou_refresh.clicked.connect(self.shoudong_refresh)
        self.grid.addWidget(self.shou_refresh, 3, 7)

        # 应用设置按钮
        self.shou_refresh = QPushButton('应用设置')
        self.shou_refresh.clicked.connect(self.set_setting)
        self.grid.addWidget(self.shou_refresh, 4, 7)
        ################################################################################################
        #列表显示
        c = QLabel("列表显示设置")
        self.grid.addWidget(c, 1, 9)


        c = QLabel("是否自动隐藏：")
        self.grid.addWidget(c, 2, 9)

        self.is_box = QCheckBox()
        self.grid.addWidget(self.is_box, 2, 10)
##############################################
        # 执行 停止
        if d['is_status'] == 'finish':
            self.start_botton = QPushButton('执行')
        else:
            self.start_botton = QPushButton('停止')

        self.start_botton.clicked.connect(self.start)
        self.start_botton.setStyleSheet("QPushButton{font:50px}")
        self.grid.addWidget(self.start_botton, 1, 11,6,9)

        # 创建表格
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(13)
        self.grid.addWidget(self.tableWidget, 6, 0, 6, 20)

        self.tableWidget.setHorizontalHeaderLabels(['id', '域名', '备注','领先价','实付价','外部/提成', '剩余时间', '结束时间', '状态', '预设价','出价额','操作','隐藏'])  # 设置行表头字段
        self.tableWidget.setColumnWidth(0, 70)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setColumnWidth(3, 70)
        self.tableWidget.setColumnWidth(4, 70)
        self.tableWidget.setColumnWidth(5, 100)
        self.tableWidget.setColumnWidth(6, 100)
        self.tableWidget.setColumnWidth(7, 150)
        self.tableWidget.setColumnWidth(8, 130)
        self.tableWidget.setColumnWidth(9, 50)
        self.tableWidget.setColumnWidth(10, 50)
        self.tableWidget.setColumnWidth(11, 50)
        self.tableWidget.setColumnWidth(12, 50)
    #手动刷新
    def shoudong_refresh(self):
        reply = QMessageBox.question(self, '竞价', '是否重新刷新列表？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        self.init_table_job()

    #线程初始化话列表
    def init_table_job(self):
        self.InItTable = InItTable(self.tableWidget)
        self.InItTable.signal.connect(self.init_table)
        self.InItTable.start()
        self.thread_list.append(self.InItTable)

    #初始化列表 给线程用
    def init_table(self, parm):
        domain = parm
        row_count = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(row_count + 1)
        data_row = self.tableWidget.rowCount()
        if data_row == 1:
            data_row = 0
        else:
            data_row -= 1

        id = domain['id']
        ym = domain['ym']
        lx_price = domain['qian']  # 领先金额
        sytime = domain['shengsj_sc']  # 剩余时间
        endtime = domain['jssj']  # 结束时间
        status = '落后' if domain['iflx'] == 0 else '领先'
        ticheng = f"{domain['wbqian']} / {domain['tc_num']}"  # 代理
        remark = domain['bz']
        shiji_price = domain['qian'] - domain['tc_num']  # 实际金额
        chujia = domain['zdqian']  # 出价金额
        max_price = d['max_price']  # 预设价
        guding = '不固定' if '不固定' in domain['dl_ts'] else '固定'
        self.set_domain_table(data_row=data_row,
                              data_list=[id, ym, remark, lx_price, shiji_price, ticheng, sytime, endtime, status,
                                         max_price, chujia,guding])

    #设置复选框
    def set_is_tongyi(self):
        #等于2可编辑 固定的都不可编辑      1不可编辑 解除
        if self.is_tongyi.checkState() == 2:
            #选中   设置下面的固定价格 不能输入  统一的可以输入
            self.chujia_time1.setEnabled(True)
            self.chujia_time2.setEnabled(True)

            self.guding_time1.setEnabled(False)
            self.guding_time2.setEnabled(False)

            self.buguding_time1.setEnabled(False)
            self.buguding_time2.setEnabled(False)
            self.is_fenbie.setChecked(False)

    def set_is_fenbie(self):
        # 等于2可编辑  1不可编辑
        if self.is_fenbie.checkState() == 2:
            self.guding_time1.setEnabled(True)
            self.guding_time2.setEnabled(True)
            self.buguding_time1.setEnabled(True)
            self.buguding_time2.setEnabled(True)

            self.chujia_time1.setEnabled(False)
            self.chujia_time2.setEnabled(False)
            self.is_tongyi.setChecked(False)

    def yusuan_file(self):
        global yd
        fname_path = QFileDialog.getOpenFileNames(self, 'Open file', '.')[0]
        try:
            with open(fname_path[0], 'r', encoding='utf-8') as fr:
                yd = fr.readlines()
            self.set_yusuan()
        except Exception as e:
            log.logger.error(e)

    def set_setting(self,event):
        global d
        reply = QMessageBox.question(self, '竞价', '确认设置么？',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        try:
            #如果统一 等于2    选中
            if self.is_tongyi.checkState() == 2:
                is_tongyi = '2'
                is_fenbie = ''
                tongyi1 = self.chujia_time1.text()
                tongyi2 = self.chujia_time2.text()
                guding1 = ''
                guding2 = ''
                buguding1 = ''
                buguding2 = ''
            else:
                is_fenbie = '2'
                is_tongyi = '0'
                guding1 = self.guding_time1.text()
                guding2 = self.guding_time2.text()
                buguding1 = self.buguding_time1.text()
                buguding2 = self.buguding_time2.text()
                tongyi1 = ''
                tongyi2 = ''

            is_box = '2' if self.is_box.checkState() == 2 else ''
            refresh_time = self.refresh_time.text()
            max_price = self.max_price.text()
            setting_d = {"user_id": user_id,
                 "password": password,
                 "refresh_time": refresh_time,
                 "max_price": max_price,
                 'is_tongyi': is_tongyi,
                 'tongyi1': tongyi1,
                 'tongyi2': tongyi2,
                 'is_fenbie': is_fenbie,
                 'guding1': guding1,
                 'guding2': guding2,
                 'buguding1': buguding1,
                 'buguding2': buguding2,
                 'yincang': is_box,
                 'is_status':d['is_status']
                 }

            with open('./config/setting.ini', 'w', encoding='utf-8') as fw:
                fw.write(json.dumps(setting_d))
            d = setting_d
            reply = QMessageBox.question(self, '竞价', '设置成功', QMessageBox.Yes, QMessageBox.Yes)

        except Exception as e:
            log.logger.error(e)

    #发送请求
    def request_headler(self, url, headers, method='get', data=None):
        if method == 'post':
            try:
                resp = session.post(url, headers=headers, data=data, timeout=10)
                return resp
            except Exception as e:
                return self.request_headler(url, headers, method, data)
        else:
            try:
                resp = session.get(url, headers=headers, timeout=10)
                return resp
            except Exception as e:
                return self.request_headler(url, headers=headers)

    # 设置预算最大金额
    def set_yusuan(self):
        row_count = self.tableWidget.rowCount()
        for ys in yd:
            for row in range(row_count):
                ys_data = ys.split('|')
                if self.tableWidget.item(row, 1).text() == ys_data[0]:
                    # 修改预算
                    # 修改最大金额
                    new_item = QTableWidgetItem(ys_data[1].strip())  # 添加最大金额
                    new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)
                    # new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.tableWidget.setItem(row, 9, new_item)  # 添加到表格中

    #出价按钮
    def buttonForRow(self,data_list):
        widget = QWidget()
        chujiaBtn = QPushButton('出价')
        chujiaBtn.clicked.connect(lambda: self.chujia_botton(data_list))
        chujiaBtn.setStyleSheet(''' text-align : center;
                                                      background-color : NavajoWhite;
                                                      height : 30px;
                                                        border-style: outset;
                                                        font : 13px  ''')
        hLayout = QHBoxLayout()
        hLayout.addWidget(chujiaBtn)
        hLayout.setContentsMargins(5, 2, 5, 2)
        widget.setLayout(hLayout)
        return widget

    #出价按钮方法
    def chujia_botton(self,data_list):
        global d
        reply = QMessageBox.question(self, '竞价', '确认出价么？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        self.ChuJiaJob = ChuJiaJob(data_list,self.tableWidget)
        self.ChuJiaJob.signal.connect(self.chuajia_set_table)
        self.ChuJiaJob.start()
        self.thread_list.append(self.ChuJiaJob)

    def chuajia_set_table(self,parm):
        self.set_domain_table(parm['row'],parm['data_list'])
        # msg_box = QMessageBox(QMessageBox.Warning, '竞价', '出价成功')
        reply = QMessageBox.question(self, '竞价', '出价成功', QMessageBox.Yes, QMessageBox.Yes)


    #设置table
    def set_domain_table(self,data_row,data_list):

        new_item = QTableWidgetItem(data_list[0])
        new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(data_row, 0, new_item)
        new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)

        # 添加数据  域名
        new_item = QTableWidgetItem(data_list[1])
        new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(data_row, 1, new_item)
        new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)

        # 添加数据  备注
        new_item = QTableWidgetItem(data_list[2])
        new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(data_row, 2, new_item)
        new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)

        # 添加数据  领先金额
        new_item = QTableWidgetItem(str(data_list[3]))
        new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(data_row, 3, new_item)
        new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)



        # 添加数据  实付价
        new_item = QTableWidgetItem(str(data_list[4]))
        if data_list[-1] == '固定':
            new_item.setForeground(QBrush(QColor(255, 0, 0)))
        new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(data_row, 4, new_item)
        new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)

        # 添加数据  提成
        new_item = QTableWidgetItem(str(data_list[5]))
        new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(data_row, 5, new_item)
        new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)

        # 添加数据 剩余时间
        new_item = QTableWidgetItem(data_list[6])
        new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(data_row, 6, new_item)
        new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)

        # 添加数据 结束时间
        new_item = QTableWidgetItem(data_list[7])
        new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(data_row, 7, new_item)
        new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)

        try:
            if '超预算，停止' == self.tableWidget.item(data_row, 8).text():
                status = '超预算，停止'
        except Exception:
            pass
        # 添加数据 状态
        new_item = QTableWidgetItem(data_list[8])
        new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        if data_list[8] == '落后':
            new_item.setForeground(QBrush(QColor(255, 0, 0)))
        elif data_list[8] == '已停止，超出预算':
            new_item.setForeground(QBrush(QColor(0, 0, 255)))
        self.tableWidget.setItem(data_row, 8, new_item)
        new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)

        max_price = d['max_price']
        for ys in yd:
            if ys.split('|')[0] == data_list[1]:
                max_price = ys.split('|')[-1]
                break
        # # 添加数据 预算
        # try:
        #     max_price = self.tableWidget.item(data_row, 9).text()
        # except Exception:



        new_item = QTableWidgetItem(max_price)
        self.tableWidget.setItem(data_row, 9, new_item)
        new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)

        # 添加数据 出价
        # new_item = QPushButton(str(chujia))
        new_item = QTableWidgetItem(str(data_list[10]))
        self.tableWidget.setItem(data_row, 10, new_item)
        new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)

        self.tableWidget.setCellWidget(data_row, 11, self.buttonForRow(data_list))

    #获取列表数据
    def get_table_data(self,parm):
        global doamin_dict
        global jingjia_dict
        data_row = self.tableWidget.rowCount()
        if data_row == 1:
            data_row = 0
        else:
            data_row -= 1
        for row in range(data_row+1):
            if self.tableWidget.item(row,1).text() == parm[1]:
                self.set_domain_table(row, parm)
                return
        print(f'没找到该域名 {parm[1]}')
        row_count = self.tableWidget.rowCount()
        data_row = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(row_count + 1)
        self.set_domain_table(data_row, parm)
        parm.append(data_row)
        # jingjia_dict[parm[1]] = parm

    # 监控价格接口
    def set_table_data(self, parm):
        # 要获取key对应的值
        sytime, data = parm[0], parm[1]
        # 修改剩余时间
        new_item = QTableWidgetItem(sytime)  # 添加状态列
        new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)
        new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(data['row_index'], 3, new_item)  # 添加到表格中

        # 修改最大金额
        new_item = QTableWidgetItem(data['max_price'])  # 添加最大金额
        new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)
        self.tableWidget.setItem(data['row_index'], 6, new_item)  # 添加到表格中

        # 修改状态
        new_item = QTableWidgetItem(data['status'])  # 添加最大金额
        if data['status'] == '落后':
            new_item.setForeground(QBrush(QColor(255, 0, 0)))
        elif data['status'] == '超预算，停止':
            new_item.setForeground(QBrush(QColor(0, 0, 255)))

        new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)
        new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(data['row_index'], 5, new_item)  # 添加到表格中

        # 修改领先价格
        new_item = QTableWidgetItem(data['lx_price'])  # 添加最大金额
        new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)
        new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(data['row_index'], 2, new_item)  # 添加到表格中

    def start(self):
        #更改按钮
        if d['is_status'] == 'running':
            self.start_botton.setText('执行')
            d['is_status'] = 'finish'

        else:
            self.start_botton.setText('停止')
            d['is_status'] = 'running'
        for t in self.thread_list:
            if t.name == 'place_job':
                return


        self.PlaceJob = PlaceJob(self.tableWidget)
        self.PlaceJob.signal.connect(self.get_table_data)
        self.PlaceJob.start()
        self.thread_list.append(self.PlaceJob)

    #关闭窗口执行方法
    def closeEvent(self, event):
        with open('./config/setting.ini', 'w', encoding='utf-8') as fw:
            d['is_status'] = 'finish'
            fw.write(json.dumps(d))

        # for t in self.thread_list:
        #     t.stop()
        print(2)

    #检测是否需要登陆
    def check_login(self):
        global session
        global password
        global user_id
        while True:
            url = 'http://7a08c112cda6a063.juming.com:9696/user/#/qiang_jj'
            resp = self.request_headler(url,headers3, method='get', data=None)
            if '<title>用户登录-聚名网</title>' in resp.text:
                session = Login(f're_mm={password_md5}&re_yx={user_id}&re_yzm=').index()
            time.sleep(10)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = LoginForm()
    sys.exit(app.exec_())
