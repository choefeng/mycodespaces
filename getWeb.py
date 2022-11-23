# coding=utf-8
import random
import time
from http import cookiejar

import requests
import os, re
from bs4 import BeautifulSoup
import datetime


def getWebPageSite(url, headers=None, params=None):
    try:
        # 第一种
        # session = requests.Session()
        # res = session.get(url, headers=headers)
        # 第二种
        res = requests.get(url, params=params, headers=headers)
        res.encoding = 'utf-8'  # 更改网页编码--------不改会乱码
        # 由于res的格式为requests.models.Response无法直接print，用text转成str格式
        # 若用于下载图片、视频、音频等多媒体格式,应用response.content转成二进制的bytes格式
        html = res.text
        # 创建一个BeautifulSoup对象
        soup = BeautifulSoup(html, "html.parser")
        # 找出目标网址中所有的a标签
        # 函数返回的是一个list
        ans = soup.find_all("a")
        print(ans)
    except requests.exceptions.RequestException as e:
        print(e)
        return 0
    site_list = []
    for tag in ans:
        # 获取a标签下的href网址
        string_ans = str(tag.get("href"))
        site_list.append(string_ans)

    remove_attr = [0, 0, 0, -1, -1, -1]
    try:
        for i in remove_attr:
            site_list.pop(i)
    except IndexError as e:
        print("发生错误：", e)
        return 0
    print(site_list)
    print("读取完成，共%d个。" % (len(site_list)))
    return site_list


def fileIO(fileurl, type, data=None, encoding="utf-8"):
    result = []
    if type == 1:
        with open(fileurl, "w+", encoding=encoding) as f:
            if isinstance(data, list):
                str1 = ""
                for i in data:
                    str1 += (i + "\n")
                f.write(str1)
            else:
                f.write(str(data))
            f.flush()
            result.append("OK")
            f.close()
    elif type == 0:
        with open(fileurl, "r", encoding=encoding) as f:
            for s in f.readlines():
                result.append(s[:-1])
            f.close()
    return result


def saveFile(final_url, dir, name, headers=None, params=None):
    if (os.path.exists(dir) == False):
        # 如果不存在新建文件夹
        os.mkdir(dir)
    time.sleep(1)
    html = ""
    try:
        res = requests.get(final_url, params=params, headers=headers)
        res.encoding = 'utf-8'
        html = res.text
    except requests.exceptions.RequestException as e:
        print(e)
    fileIO(os.path.join(dir, name), 1, html)


def getWebPage(start_url, end_url, dir, where, headers, params=None):
    count = 0
    for i in end_url:
        name = ""
        if i[7:8] == "A":
            name = i[14:]
        elif i[7:8] == "B":
            name = i[12:]
        if os.path.exists(os.path.join(dir, name)) or os.path.exists(os.path.join(dir[:-1], name)):
            print("已存在%s！" % (name))
            pass
        else:
            final_url = start_url + i[1:]
            if where == "both":
                saveFile(final_url, dir, name, headers, params)
                print("已下载：%s，网址：\"%s\"" % (name, final_url))
                count += 1
            elif where == "A" and i[7:8] == "A":
                saveFile(final_url, dir, name, headers, params)
                print("已下载：%s，网址：\"%s\"" % (name, final_url))
                count += 1
            else:
                pass

    print("全部下载完成，共%d个。" % (count))



if __name__ == '__main__':
    url = 'https://zhihu2.xiaomiqiu.com'
    params = {
        'kw': '赵丽颖吧',
        'pn': '50'
    }
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 UOS"
    # }
    headers = {}
    #
    user_agent_list = [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A432 QQ/7.1.8.452 V1_IPH_SQ_7.1.8_1_APP_A Pixel/750 Core/UIWebView NetType/WIFI QBWebViewType/1",
        "Mozilla/5.0 (Linux; Android 5.1.1; NX529J Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043613 Safari/537.36 V1_AND_SQ_7.2.5_744_YYB_D QQ/7.2.5.3305 NetType/WIFI WebP/0.3.0 Pixel/1080",
        "Mozilla/5.0 (Linux; Android 7.1.1; MIX 2 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043613 Safari/537.36 V1_AND_SQ_7.2.5_744_YYB_D QQ/7.2.5.3305 NetType/4G WebP/0.3.0 Pixel/1080",
        "Mozilla/5.0 (Linux; Android 7.0; STF-AL10 Build/HUAWEISTF-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043622 Safari/537.36 V1_AND_SQ_7.2.5_744_YYB_D QQ/7.2.5.3305 NetType/4G WebP/0.3.0 Pixel/",
        "Mozilla/5.0 (Linux; Android 7.0; FRD-AL10 Build/HUAWEIFRD-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043622 Safari/537.36 V1_AND_SQ_7.2.5_744_YYB_D QQ/7.2.5.3305 NetType/4G WebP/0.3.0 Pixel/",
        "Mozilla/5.0 (Linux; Android 7.0; ZUK Z2121 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043613 Safari/537.36 V1_AND_SQ_7.2.5_744_YYB_D QQ/7.2.5.3305 NetType/WIFI WebP/0.3.0 Pixel/1080",
        "Mozilla/5.0 (Linux; Android 6.0.1; SM-A9100 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043613 Safari/537.36 V1_AND_SQ_7.2.5_744_YYB_D QQ/7.2.5.3305 NetType/WIFI WebP/0.3.0 Pixel/1080",
        "Mozilla/5.0 (Linux; Android 6.0.1; SM-A9100; Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.92 Mobile Safari/537.36 SogouMSE,SogouMobileBrowser/5.8.32",
        "Mozilla/5.0 (Linux; Android 6.0.1; MI 5 Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043613 Safari/537.36 V1_AND_SQ_7.1.0_0_TIM_D TIM2.0/2.0.1.1720 QQ/6.5.5  NetType/WIFI WebP/0.3.0 Pi",
        "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; SM-G5108 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.9 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043622 Safari/537.36 V1_AND_SQ_7.2.5_744_YYB_D QQ/7.2.5.3305 NetType/WIFI WebP/0.3.0 Pixel/1080",
        "Mozilla/5.0 (Linux; Android 7.1.1; ONEPLUS A5000 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043622 Safari/537.36 V1_AND_SQ_7.2.0_730_YYB_D QQ/7.2.0.3270 NetType/WIFI WebP/0.3.0 Pixel",
        "Mozilla/5.0 (Linux; Android 7.1.1; ONEPLUS A5000 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 5.1; OPPO A37m Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.2.5_744_YYB_D QQ/7.2.5.3305 NetType/4G WebP/0.3.0 Pixel/720",
        "Mozilla/5.0 (Linux; U; Android 5.1; zh-cn; OPPO A37m Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.134 Mobile Safari/537.36 OppoBrowser/4.3.9",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A432 QQ/7.2.8.478 V1_IPH_SQ_7.2.8_1_APP_A Pixel/750 Core/UIWebView Device/Apple(iPhone 7) NetType/WIFI QBWebViewType/1"

    ]
    headers['User-Agent'] = random.choice(user_agent_list)
    # print(headers['User-Agent'])


    today = datetime.date.today()

    # 读网页列表
    # data = getWebPageSite(url, headers)
    # result = fileIO(os.path.join("txt", str(today))+".txt", 1, data)
    # print(result)

    # 写网页
    content = fileIO(os.path.join("txt", str(today))+".txt", 0)
    getWebPage(url, content, "webPage1", "both", headers, params)


