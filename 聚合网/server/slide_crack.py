import json
import multiprocessing
import random
import socket
import sqlite3
import threading
import time
import re
import requests
from pyppeteer import launch
from retrying import retry
import os
import asyncio
from util import js1, js3, js4, js5
from flask import Flask, request, render_template
from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all()


pattern = re.compile(
    r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
    r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
    r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
    r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
)

app = Flask(__name__)

verify_lake = set()

# >  域名建站历史查询
domain_done = set()
domain_task = set()
domain_init = set()
reslut_save_db = set()

TOKEN_LEN = 50  # 设置暂停获取验证码token的数量
TOKEN_SLEEP = 30  #设置休息时长
host = '127.0.0.1'
user = 'root'
passwd = '123456'
port = 3306
db = 'test'

def save_none_urls(data):
    con = sqlite3.connect("spider.db")
    cursor = con.cursor()
    # con = pymysql.connect(host=host, user=user, passwd=passwd, port=port, db=db)
    # cursor = con.cursor()
    try:
        cursor.execute("create table IF NOT EXISTS none_urls(link varchar(255) primary key)")
        con.commit()
    except Exception as e:
        pass
    cursor.execute("select link from none_urls where link = ?", (data, ))
    # cursor.execute("select link from none_urls where link = %s"%(data[0]))
    row = cursor.fetchone()
    if row:
        return
    else:
        # cursor.execute("insert into none_urls values('%s')"%escape_string(data[0]))
        cursor.execute("insert into none_urls values(?)", (data, ))

    cursor.close()
    con.commit()
    con.close()

def save_db(data):
    '''
    保存到 DB
    :param data:
    :return:
    '''
    con = sqlite3.connect("spider.db")
    cursor = con.cursor()
    # con = pymysql.connect(host=host, user=user, passwd=passwd, port=port, db=db)
    # cursor = con.cursor()
    try:
        cursor.execute("create table IF NOT EXISTS urls(link varchar(255) primary key, "
                       "info LONGTEXT, detail LONGTEXT)")
        con.commit()
    except Exception as e:
        pass
    for item in data:
        if not item or len(item) < 3 or not item[0] or not item[1] or not item[2]:
            print(item, "该数据异常")
            continue
        cursor.execute("select link from urls where link = ?", (item[0], ))
        # cursor.execute("select link from urls where link = '%s'"%item[0])
        row = cursor.fetchone()
        if row:
            continue
        else:
            cursor.execute("insert into urls values(?, ?, ?)", item)
            # cursor.execute("insert into urls values('%s', '%s', '%s')"%(escape_string(item[0]),escape_string(item[1]),escape_string(item[2])))

    cursor.close()
    con.commit()
    con.close()

def thread_save_db():
    '''
    接口返回的数据保存到 DB
    :return:
    '''
    while True:
        while True:
            # print(len(reslut_save_db))
            if len(reslut_save_db) < 1:
                break
            else:
                data = reslut_save_db.pop()
            if len(data) == 1:
                save_none_urls(data[0])
            elif len(data) == 3:
                save_db([data])
        time.sleep(1)

def init_task_txt():
    """初始化域名任务"""
    global domain_done
    # 处理完成的
    print(os.getcwd())
    with open("./taskdata/urls_output.txt", "r", encoding="UTF-8") as f:
        rows = f.readlines()
        for row in rows:
            row = row.replace("\t", "").replace("\n", "").replace(" ", "")
            flag = True if pattern.match(row) else False
            if not flag:
                continue
            domain_done.add(row)
    # 未处理的
    with open("./taskdata/urls.txt", "r", encoding="UTF-8-sig") as f:
        rows = f.readlines()
        for row in rows:
            row = row.replace("\t", "").replace("\n", "").replace(" ", "")
            if row not in domain_done:
                flag = True if pattern.match(row) else False
                if flag:
                    domain_init.add(row)

    domain_done = set()


def write_done(domain, query_type=""):
    txt_name = "urls_output.txt" if not query_type else (query_type + "_urls_output.txt")
    with open("./taskdata/" + txt_name, "a+") as f:
        f.write(domain + "\n")



def now_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

def retry_if_result_none(result):
    return result is None

@retry(retry_on_result=retry_if_result_none,)
async def mouse_slide(page=None):
    await asyncio.sleep(3)
    try:
        await page.hover('#nc_1_n1z')
        await page.mouse.down()

        await page.mouse.move(1800, 0, {'delay': random.randint(4000, 8000)})
        await page.mouse.up()
    except Exception as e:
        print(e, '     :slide login False')
        return None
    else:
        return
        # await asyncio.sleep(3)
        # slider_again = await page.Jeval('.nc-lang-cnt', 'node => node.textContent')
        # if slider_again != '验证通过':
        #     return None
        # else:
        #     print('验证通过')

async def build_browser():
    browser = await launch({'headless': False, 'args': ['--no-sandbox', '--window-size=1366,850'], "userDataDir": r"./temp"})
    return browser

async def open_verify(b):
    page = await b.newPage()
    await page.deleteCookie()
    await page.setViewport({'width': 1366, 'height': 768})

    await page.setUserAgent(
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36')
    await page.goto(f'file:///{os.getcwd()}/tset_verify.html')

    await page.evaluate(js1)
    await page.evaluate(js3)
    await page.evaluate(js4)
    await page.evaluate(js5)
    await page.click("#start")
    await mouse_slide(page=page)
    sleep_count = 0
    while True:
        token = await page.evaluate("document.getElementById(\"token\").innerHTML")
        auth = await page.evaluate("document.getElementById(\"auth\").innerHTML")
        session = await page.evaluate("document.getElementById(\"session\").innerHTML")
        if not token or not auth or not session:
            if sleep_count > 3:
                break
            sleep_count += 1
            await asyncio.sleep(1)
        else:
            # print(token, auth, session)
            break

    await page.close()
    return token, auth, session

async def main():
    b = None
    count = 0
    try:
        while True:
            if b is None:
                b = await build_browser()
            if count >= TOKEN_LEN:
                await b.close()
                b = None
                count = 0
                print("获取验证在中途休息中....")
                time.sleep(TOKEN_SLEEP)
                os.system("rd /s/q temp")
                os.mkdir("temp")
                continue

            verify = await open_verify(b)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("localhost", 8000))
            client.send(bytes(str(verify), encoding="utf8"))
            client.close()
            # verify_lake.add(verify)
            count += 1
            await asyncio.sleep(1)


    except Exception as e:
        await b.close()
        print(e)

def monitor():
    while True:
        print(f"监控台: 当前token池:{len(verify_lake)},未获取token域名数量:{len(domain_init)}, 未完成域名数量: {len(domain_task)}, 已处理域名:{len(domain_done)}")
        time.sleep(2)

def get_token():
    print("启动token获取程序")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print("token获取程序终止")

def child_process():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 8000))
    server.listen(0)
    while True:
        connection, address = server.accept()
        verify = eval(str(connection.recv(10000), encoding="utf8"))
        if verify:
            verify_lake.add(verify)
        time.sleep(1)

def exec_token():
    while True:
        if len(verify_lake) < 1:
            # print(now_time(), "token池为空,无法继续进行域名请求任务")
            time.sleep(2)
            continue
        if len(domain_init) < 1:
            # print(now_time(), "任务池为空，程序休息中...")
            time.sleep(5)
            continue
        # 开始抽取域名
        token, auth, session = verify_lake.pop()
        ds = []
        while len(ds) < 2000:
            if len(domain_init) < 1:
                break
            ds.append(domain_init.pop())

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
        data = {"ym": "\n".join(ds),
                "authenticate": auth,
                "token": token,
                "sessionid": session
                }
        try:
            res = requests.post(url=api, data=data, headers=headers)
            res = res.json()
            if res['code'] != 1:
                print("错误: ", res['msg'])
                for i in ds:
                    domain_init.add(i)
                continue
            for item in res['data']:
                print(item)
                if res['data'].index(item) % 2 == 0:
                    domain_task.add((item['ym'], item['token'], 0))
                else:
                    domain_task.add((item['ym'], item['token'], 1))

        except Exception as e:
            print("[209]", e)
            for i in ds:
                domain_init.add(i)

def deal_history(info, detail, domain, token):
    if not info:
        domain_task.add((domain, token))
        return "ok"
    try:
        jls = info.get("data", {}).get("jls", None)
        if not jls or jls == "0":
            reslut_save_db.add((domain, ))
            write_done(domain)
            domain_done.add(domain)
            return "OK"

        reslut_save_db.add((domain, json.dumps(info), json.dumps(detail)))
        write_done(domain)
        domain_done.add(domain)
    except Exception as e:
        print('出错   %s'%e)
        domain_task.add((domain, token))
        return "ok"


@app.route('/juming')
def senddomain():
    target = request.args.get("target")
    if not target:
        return json.dumps({"domain": "", "token": ""})
    d = {"domain": "", "token": ""}

    if len(domain_task) == 0:
        d = {"domain": "", "token": ""}
    else:
        row = domain_task.pop()
        try:
            d['domain'], d["token"], d['nums'] = row
        except Exception as e:
            print(e)
            return json.dumps(d)


    return json.dumps(d)


@app.route("/get_token",)
def get_token():
    try:
        token, auth, session = verify_lake.pop()
    except Exception as e:
        print('请更新token池  没有token了')
        return json.dumps('请更新token池')
    data = {
        'token':token,
        'auth':auth,
        'session':session,
    }
    return json.dumps(data)

@app.route("/return", methods=["POST"])
def returndomain():
    try:
        info = request.json.get("info")
        detail = request.json.get("detail")
        d = request.args.get("domain")
        token = request.args.get("token")
        target = request.args.get("target")
    except Exception as e:
        print(e)
        return "error"
    # print(info)
    # print(d, token)
    if target == "history":
        deal_history(info, detail, d, token)


    return "ok"

@app.route("/get_token_page", methods=["GET","POST"])
def get_token_page():
    token = request.form.get("token")
    auth = request.form.get("auth")
    session = request.form.get("session")
    if token and auth and session:
        verify_lake.add((token, auth, session))
        print((token, auth, session))
    return render_template("test_verify.html")

@app.route("/")
def monitor_html():
    token_lake = len(verify_lake)
    now = now_time()

    #   域名建站历史查询: history
    history_value = [len(domain_init), len(domain_task), len(domain_done)]

    data = {
        "token": token_lake,
        "now": now,
        "history": history_value,
    }
    return render_template("monitor.html", data=data)

if __name__ == '__main__':
    threading.Thread(target=exec_token).start()
    threading.Thread(target=thread_save_db).start()
    print("初始化任务")
    init_task_txt()
    print("初始化完成")
    http_server = WSGIServer(('0.0.0.0', 5001), app)
    http_server.serve_forever()
    # app.run(port=5001, threaded=True)
