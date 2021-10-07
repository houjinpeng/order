# 557747
# qq123123

# 301111
# hamigua10086
import logging
import threading
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
from lxml import etree
import json
from logging import handlers

cookie = 'gr_user_id=369b158e-a04d-471e-a6af-91be2682116e; PHPSESSID=02e5s1b9j5tcj6q34naje4jgm5; laiyuan=7a08c112cda6a063.juming.com; Hm_lvt_f94e107103e3c39e0665d52b6d4a93e7=1632800099; UM_distinctid=17c2a784b74f57-0041c7813c00c-a7d173c-1fa400-17c2a784b75490; _qddaz=QD.oeyvft.ibtdvl.ku3j0sao; a801967fdbbbba8c_gr_session_id=175db61b-e783-4432-9d16-03fafafc628f; a801967fdbbbba8c_gr_session_id_175db61b-e783-4432-9d16-03fafafc628f=true; Hm_lpvt_f94e107103e3c39e0665d52b6d4a93e7=1632817095; Juming_uid=301111; Juming_isapp=0; Juming_zhu=b262bd87c3d016f4159090f817facac7; Juming_jf=1abf0a421fae22c366275c8cdf6585df; Juming_qy=666bcb257ddbb5d407bc19f13eab46fe'
session = requests.session()

doamin_dict = {}
jingjia_dict = {}
# 读取预算

yd = []

# 读取设置
try:
    with open('./config/setting.ini', 'r', encoding='utf-8') as fr:
        data = fr.read()
    d = json.loads(data)
except Exception:
    d = {"refresh_time": "1", "max_price": "303", "shengyu_shijian": "10","user_id":"301111","password":"hamigua10086"}



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


log = Logger('./config/域名竞价.log', level='debug')
password_md5 = ''

try:
    user_id = d['user_id']
    password = d['password']
except Exception :
    user_id = ''
    password = ''
# pyqt5 封装线程类
class Job(QtCore.QThread):
    signal = pyqtSignal(list)

    def __init__(self, key):
        super(Job, self).__init__()
        self.key = key
        self.headers = {
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
        self.headers3 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'cookie': cookie,
            'Host': '7a08c112cda6a063.juming.com:9696',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
        }

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

    # 出价接口
    def bid(self, domain_id, token, price):
        log.logger.debug(f'{domain_id}出价中')
        url = 'http://7a08c112cda6a063.juming.com:9696/p/chujia'
        try:
            data = f'csrf_token={token}&id={domain_id}&jg={price}'
            self.headers['Referer'] = f'http://7a08c112cda6a063.juming.com:9696/p/{domain_id}/'
            self.headers['Content-Length'] = len(data)
            resp = self.request_headler(url, headers=self.headers, data=data, method='post')
            log.logger.debug(resp.text)
            if json.loads(resp.text)['msg'] == '出价成功！':
                log.logger.debug(json.loads(resp.text))
                return True
            else:
                log.logger.debug(json.loads(resp.text))
                return False
        except Exception as e:
            return False

    def run(self):
        global d
        global jingjia_dict
        try:
            while True:
                try:
                    data = jingjia_dict[self.key]
                except Exception as e:
                    time.sleep(1)
                    continue

                if data['max_price'] == '':
                    data['max_price'] = d['max_price']

                url = f'http://7a08c112cda6a063.juming.com:9696/p/{data["id"]}/'
                resp = self.request_headler(url, headers=self.headers3)
                # 更新剩余时间   获取token  先判断是否超过预算  没超过加价
                e = etree.HTML(resp.text)
                try:
                    token = e.xpath('//input[@name="csrf_token"]/@value')[0]
                    sytime = e.xpath('//span[@id="lefttime"]/text()')[0]
                    now_price = int(e.xpath('//span[@id="now-price"]/text()')[0])
                    data['lx_price'] = str(now_price)
                    if '您的出价</font>(已冻结' in resp.text:
                        data['status'] = '领先'
                except Exception as error:
                    continue
                # 判断是否是落后
                if data['status'] == "落后":
                    # 判断时间是否在竞价时间
                    date_time = ''
                    try:
                        date_time = datetime.datetime.strptime(sytime, '%H小时%M分')
                    except Exception as error:
                        pass
                    try:
                        date_time = datetime.datetime.strptime(sytime, '%M分%S秒')
                    except Exception as error:
                        pass
                    try:
                        date_time = datetime.datetime.strptime(sytime, '%H小时%S秒')
                    except Exception as error:
                        pass
                    if date_time == '':
                        continue
                    minute = date_time.minute
                    hour = date_time.hour
                    # 剩余时间小于设置的时间
                    sy_shijian = hour * 60 + minute
                    if sy_shijian <= int(d['shengyu_shijian']):
                        # 判断出价是否大于竞价最高额度
                        add_price_num = e.xpath('//p[@id="app_jjfd"]/text()')[0]
                        add_price_num = int(re.findall('\d+', add_price_num)[0])
                        daili_price = e.xpath('//p[@id="daili_%s"]/font/text()' % data['id'])[0]
                        daili_price = int(re.findall('\d+', daili_price)[0])
                        # 实际需付 = 出价价格-(出价价格-代理显示价格)*60%
                        shiji_price = (now_price + add_price_num) - (now_price + add_price_num - daili_price) * 0.6
                        if int(data['max_price']) >= shiji_price:
                            # 去竞价   之后要修改状态  更改领先金额
                            log.logger.debug(f'{data["id"]} {data["ym"]} 出价为：{now_price + add_price_num} 实际需付：{shiji_price}')
                            is_succeed = self.bid(data['id'], token, now_price + add_price_num)
                            if is_succeed == True:
                                jingjia_dict[self.key]['lx_prict'] = str((now_price + add_price_num))
                                jingjia_dict[self.key]['status'] = '领先'
                        else:
                            log.logger.debug(f'{data["id"]} {data["ym"]} 出价为：{now_price + add_price_num} 实际需付：{shiji_price}   已经超过预算 停止监控此域名')
                            data['status'] = '超预算，停止'
                            self.signal.emit([sytime, data])
                            return
                self.signal.emit([sytime, data])
                time.sleep(int(d['refresh_time']))

        except Exception as error:
            log.logger.error(error)

    def stop(self):
        log.logger.debug("Stop programm.")


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
        lbl_logo.setFont(QFont("Microsoft YaHei"))
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
        self.lbl_workerid.setFont(QFont("Microsoft YaHei"))
        self.led_workerid = QLineEdit(user_id)
        self.led_workerid.setFixedWidth(270)
        self.led_workerid.setFixedHeight(38)

        self.lbl_pwd = QLabel("密码")
        self.lbl_pwd.setFont(QFont("Microsoft YaHei"))
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

        # session,msg = Login(f're_mm={password_md5}&re_yx={user_id}&re_yzm=').index()
        # if msg['code'] == -1:
        #     self.msg.setText(f'<font color="red">{msg["msg"]}</font>')
        #     return
        # with open('./config/setting.ini','w',encoding='utf-8') as fw:
        #     d['user_id'] = user_id
        #     d['password'] = password
        #     fw.write(json.dumps(d))

        self.hide()
        self.f = Bidding()
        self.f.show()


class Bidding(QWidget):
    def __init__(self):
        super().__init__()
        self.thread_list = []
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '45',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': '7a08c112cda6a063.juming.com:9696',
            'cookie': cookie,
            'Origin': 'http://7a08c112cda6a063.juming.com:9696',
            'Referer': 'http://7a08c112cda6a063.juming.com:9696/p/9889689/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.headers3 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'cookie': cookie,
            'Host': '7a08c112cda6a063.juming.com:9696',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
        }
        self.initUI()
        # self.get_table_data()
        t = threading.Thread(target=self.get_table_data)
        t.start()
        self.start()

    def initUI(self):
        self.resize(1100, 800)
        self.setWindowTitle('聚名域名竞价')
        self.setWindowIcon(QIcon('./static/juming_ico.ico'))
        self.grid = QGridLayout()
        self.grid.setSpacing(20)
        self.setLayout(self.grid)

        self.remaining_time_t = QLabel("输入剩余时间竞价/分")
        self.remaining_time_t.setFont(QFont("Microsoft YaHei"))
        self.remaining_time = QLineEdit(d['shengyu_shijian'])
        self.remaining_time.setPlaceholderText("仅可以输入整数")
        # 整数校验器[1,99]
        intValidator = QIntValidator(self)
        intValidator.setRange(1, 1000)
        self.remaining_time.setValidator(intValidator)

        # self.remaining_time.setFixedWidth(270)
        self.grid.addWidget(self.remaining_time_t, 1, 0)
        self.grid.addWidget(self.remaining_time, 1, 1)
        ##########################################################################################
        self.max_price_t = QLabel("最高竞价金额/元(实际需付)")
        self.max_price_t.setFont(QFont("Microsoft YaHei"))
        self.max_price = QLineEdit(d['max_price'])
        self.max_price.setPlaceholderText("仅可以输入整数")
        # 整数校验器[1,99]
        intValidator = QIntValidator(self)
        intValidator.setRange(1, 1000000)
        self.remaining_time.setValidator(intValidator)
        # self.max_price.setFixedWidth(50)
        self.grid.addWidget(self.max_price_t, 1, 2)
        self.grid.addWidget(self.max_price, 1, 3)
        ##########################################################################################

        self.btn2 = QPushButton('选择预算文件')
        self.btn2.clicked.connect(self.yusuan_file)
        self.grid.addWidget(self.btn2, 1, 4)

        ##########################################################################################

        self.refresh_t = QLabel("设置刷新时间/秒")
        self.refresh_t.setFont(QFont("Microsoft YaHei"))
        self.refresh = QLineEdit(d['refresh_time'])
        self.refresh.setPlaceholderText("仅可以输入整数")
        # 整数校验器[1,99]
        intValidator = QIntValidator(self)
        intValidator.setRange(1, 1000)
        self.remaining_time.setValidator(intValidator)
        self.grid.addWidget(self.refresh_t, 1, 5)
        self.grid.addWidget(self.refresh, 1, 6)
        ####################################################################
        self.btn3 = QPushButton('确定设置')
        self.btn3.clicked.connect(self.set_setting)
        self.grid.addWidget(self.btn3, 1, 7)

        # 创建表格
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(7)
        self.grid.addWidget(self.tableWidget, 2, 0, 2, 8)

        self.tableWidget.setHorizontalHeaderLabels(
            ['id', '域名', '领先价格(已冻结)', '剩余时间', '结束时间', '您的状态', '最高竞价额度'])  # 设置行表头字段
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setColumnWidth(3, 150)
        self.tableWidget.setColumnWidth(4, 200)
        self.tableWidget.setColumnWidth(5, 100)
        self.tableWidget.setColumnWidth(6, 100)

    def yusuan_file(self):
        global yd
        fname_path = QFileDialog.getOpenFileNames(self, 'Open file', '.')[0]
        with open(fname_path[0], 'r', encoding='utf-8') as fr:
            yd = fr.readlines()
        self.set_yusuan()

    def set_setting(self):
        global d
        try:
            with open('./config/setting.ini', 'w', encoding='utf-8') as fw:
                refresh_time = self.refresh.text()
                max_price = self.max_price.text()
                shengyu_shijian = self.remaining_time.text()
                d = {'refresh_time': refresh_time, 'max_price': max_price, 'shengyu_shijian': shengyu_shijian,'user_id':user_id,'password':password}
                fw.write(json.dumps(d))
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

    #获取列表数据
    def get_table_data(self):
        global doamin_dict
        while True:
            url = ' http://7a08c112cda6a063.juming.com:9696/user_main/jj_list?page=1&limit=10000&myjj=1'
            data = 'page=1&limit=10000&myjj=1'
            resp = self.request_headler(url, method='post', data=data, headers=self.headers)
            try:
                all_domain = json.loads(resp.text)['data']
            except Exception as e:
                all_domain = []
            # row_count = 1 if row_count == 0 else row_count
            for domain in all_domain:
                f = True
                row_count = self.tableWidget.rowCount()
                if jingjia_dict.get(domain['ym']) == None:
                    self.tableWidget.setRowCount(row_count + 1)  # 添加一行
                    data_row = self.tableWidget.rowCount()
                    if data_row == 1:
                        data_row = 0
                    else:
                        data_row -= 1
                else:
                    data_row = jingjia_dict.get(domain['ym'])['row_index']

                # for row in range(row_count):
                #     if self.tableWidget.item(row,1).text() == domain['ym']:
                #         f = False
                #         break
                # if f == True:
                #     self.tableWidget.setRowCount(row_count + 1)  # 添加一行
                #如果有更新  没有添加
                #如果竞价列表有  更新row的数列   没有的话就是最大数列

                # '域名', '领先价格(已冻结)', '剩余时间', '结束时间', '您的状态', '最高竞价额度'
                id = domain['id']
                ym = domain['ym']
                lx_price = domain['qian']
                sytime = domain['shengsj_sc']
                endtime = domain['jssj']
                status = '落后' if domain['iflx'] == 0 else '领先'


                # 添加数据 id
                new_item = QTableWidgetItem(id)
                new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(data_row, 0, new_item)
                new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)

                # 添加数据  域名
                new_item = QTableWidgetItem(ym)
                new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(data_row, 1, new_item)
                new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)

                # 添加数据  领先金额
                new_item = QTableWidgetItem(str(lx_price))
                new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(data_row, 2, new_item)
                new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)

                # 添加数据 剩余时间
                new_item = QTableWidgetItem(sytime)
                new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(data_row, 3, new_item)
                new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)

                # 添加数据 结束时间
                new_item = QTableWidgetItem(endtime)
                new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(data_row, 4, new_item)
                new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)

                # 添加数据 状态
                new_item = QTableWidgetItem(status)
                new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                if status == '落后':
                    new_item.setForeground(QBrush(QColor(255, 0, 0)))
                self.tableWidget.setItem(data_row, 5, new_item)
                new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)

                # 添加数据 预算
                new_item = QTableWidgetItem(d['max_price'])
                self.tableWidget.setItem(data_row, 6, new_item)
                new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)

                #格式化时间   对比时间:
                date_time = ''
                try:
                    date_time = datetime.datetime.strptime(sytime, '%H小时%M分')
                except Exception as error:
                    pass
                try:
                    date_time = datetime.datetime.strptime(sytime, '%M分%S秒')
                except Exception as error:
                    pass
                try:
                    date_time = datetime.datetime.strptime(sytime, '%H小时%S秒')
                except Exception as error:
                    pass


                if date_time == '':
                    continue
                hour = date_time.hour
                minute = date_time.minute
                if hour*60+minute <= int(d['shengyu_shijian']):
                    if self.thread_list == []:
                        self.job = Job(domain['ym'])
                        self.job.signal.connect(self.set_table_data)
                        self.job.start()
                        self.thread_list.append(self.job)

                    for t in self.thread_list:
                        if t.key == domain['ym']:
                           break

                        self.job = Job(domain['ym'])
                        self.job.signal.connect(self.set_table_data)
                        self.job.start()
                        self.thread_list.append(self.job)

            time.sleep(10)

    #设置预算最大金额
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
                    self.tableWidget.setItem(row, 6, new_item)  # 添加到表格中

    # 初始化表格整完以后  需要实时更新   把id 行数都要传递到队列中
    def init_table_data(self):
        '''
        定时把每行的数据存到字典中，定时程序在字典中去取数据进行刷新等操作
        :return:
        '''
        while True:
            global jingjia_dict
            row_count = self.tableWidget.rowCount()
            for row in range(row_count):
                try:
                    ym = self.tableWidget.item(row, 1).text()
                except Exception as e:
                    continue
                if jingjia_dict.get(ym) == None:
                    jingjia_dict[ym] = {}

                jingjia_dict[ym]['id'] = self.tableWidget.item(row, 0).text()
                jingjia_dict[ym]['ym'] = ym
                jingjia_dict[ym]['lx_price'] = self.tableWidget.item(row, 2).text()
                jingjia_dict[ym]['sytime'] = self.tableWidget.item(row, 3).text()
                jingjia_dict[ym]['endtime'] = self.tableWidget.item(row, 4).text()
                jingjia_dict[ym]['status'] = self.tableWidget.item(row, 5).text()
                jingjia_dict[ym]['max_price'] = self.tableWidget.item(row, 6).text()
                jingjia_dict[ym]['row_index'] = row
            time.sleep(10)

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
        new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)
        new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(data['row_index'], 5, new_item)  # 添加到表格中

        # 修改领先价格
        new_item = QTableWidgetItem(data['lx_price'])  # 添加最大金额
        new_item.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)
        new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(data['row_index'], 2, new_item)  # 添加到表格中

    # 调度器  分配线程
    # def scheduler(self):
    #     if list(jingjia_dict.keys()) == []:
    #         return
    #
    #     self.thread_list = []
    #     for key in list(jingjia_dict.keys()):
    #         self.thread_list.append(Job(key))
    #
    #     for i in self.thread_list:
    #         i.signal.connect(self.set_table_data)
    #         i.start()
    #     # print(1)
    #     # self.t3 = Job(list(jingjia_dict.keys())[0])
    #     # self.t3.signal.connect(self.set_table_data)
    #     # self.t3.start()

    #开始程序
    def start(self):
        # 开启一个线程来刷新表格中的数据
        table_t = threading.Thread(target=self.init_table_data)
        table_t.start()
        check_login_t = threading.Thread(target=self.check_login)
        check_login_t.start()

    #关闭窗口执行方法
    def closeEvent(self, event):
        for t in self.thread_list:
            t.stop()
        print(2)

    #检测是否需要登陆
    def check_login(self):
        global session
        global password
        global user_id
        while True:
            url = 'http://7a08c112cda6a063.juming.com:9696/user/#/qiang_jj'
            resp = self.request_headler(url,self.headers3, method='get', data=None)
            if '<title>用户登录-聚名网</title>' in resp.text:
                session = Login(f're_mm={password_md5}&re_yx={user_id}&re_yzm=').index()
            time.sleep(10)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = LoginForm()
    sys.exit(app.exec_())
