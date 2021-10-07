# @Time : 2021/5/7 8:32 
# @Author : HH
# @File : 距离.py 
# @Software: PyCharm
# @explain:
import random

import numpy as np


def get_random_ge(distance):
    """
    生成随机的轨迹
    {
        "d":0.85,"m":"","c":"总耗时","w":372,"h":186,"os":"weapp","cs":0,"wd":0,"sm":1
    }
    """
    length = random.choice(np.arange(8, 12))
    avge = int(distance / length)

    difference = int(distance - avge * length)

    tracks = [avge] * length
    randomFlag = 0
    for i in range(length):
        if randomFlag:
            tracks[random.randint(0, length - 1)] += randomFlag
            randomFlag = 0
        if random.choice([False, True]):
            if tracks[i] > 1:
                randomFlag = random.randint(1, tracks[i])
            else:
                randomFlag = random.randint(tracks[i], 1)

            tracks[i] -= randomFlag
    if randomFlag:
        tracks[random.randint(0, length - 1)] += randomFlag
    luck = random.randint(0, length - 1)
    # 补全损失值
    tracks[luck] = tracks[luck] + difference

    tracksList = []
    tracksList.append([0, 0, 0])
    moveCount = 101
    for index in range(len(tracks)):
        if index != 0:
            tracks[index] = tracks[index] + tracks[index - 1]
            tracksList.append([tracks[index], 0, 0 + moveCount])
        else:
            tracksList.append([tracks[index], 0, 0 + moveCount])
        moveCount += 100

    data = {
        "d": distance / 372,
        "m": tracksList,
        "c": tracksList[-1][-1] + 56,
        "w": 372,
        "h": 186,
        "os": "weapp",
        "cs": 0,
        "wd": 0,
        "sm": 1
    }

    print(data)
    return data


if __name__ == '__main__':
    get_random_ge(100)