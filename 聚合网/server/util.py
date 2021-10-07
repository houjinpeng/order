js1 = '''() =>{

           Object.defineProperties(navigator,{
             webdriver:{
               get: () => false
             }
           })
        }'''

js2 = '''() => {
        alert (
            window.navigator.webdriver
        )
    }'''

js3 = '''() => {
        window.navigator.chrome = {
    runtime: {},
    // etc.
  };
    }'''

js4 = '''() =>{
Object.defineProperty(navigator, 'languages', {
      get: () => ['en-US', 'en']
    });
        }'''

js5 = '''() =>{
Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5,6],
  });
        }'''

import time

def now_time():
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return t


def div_list(ls, n):
    print(now_time(), "进行拆分urls分组, 按%d个分组" % n)
    res = []
    temp = []
    count = 0
    for i in ls:
        if count >= n:
            res.append(temp)
            temp = []
            count = 0
        else:
            count += 1
            temp.append(i)
    if temp:
        res.append(temp)
    print(now_time(), "分组完毕, 共分为%d组" % len(res))
    return res
