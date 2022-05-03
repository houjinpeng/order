import execjs

import os

# os.environ["EXECJS_RUNTIME"] = "PhantomJS"
with open('icpfuben.js', encoding='utf-8') as f:
    js_code = f.read()
ctx = execjs.compile(js_code,cwd='E:\\soft\\worker\\NodeJs\\node_modules')

# print(execjs.get().name)
a = {
    "SendInterval": 5,
    "SendMethod": 8,
    "isSendError": 1,
    "MaxMCLog": 12,
    "MaxKSLog": 14,
    "MaxMPLog": 5,
    "MaxGPLog": 1,
    "MaxTCLog": 12,
    "GPInterval": 50,
    "MPInterval": 4,
    "MaxFocusLog": 6,
    "Flag": 2980046,
    "OnlyHost": 1,
    "MaxMTLog": 500,
    "MinMTDwnLog": 30,
    "MaxNGPLog": 1,
    "sIDs": [
        "_n1t|_n1z|nocaptcha|-stage-1"
    ],
    "mIDs": [
        "nc-canvas",
        "click2slide-btn"
    ],
    "hook": 1,
    "font": 1,
    "api": 1
}

data2 = ctx.call('e', 1,a)
# data2 = ctx.call('ccc',a)
print(data2)

