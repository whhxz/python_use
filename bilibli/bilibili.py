# -*- coding: utf-8 -*-
# 需要指定改进地方：
# 1.部分文件下载不动，需要修改
# 2.抓包获取的收藏地址，不方便，需改进自己依据用户id获取
# 3.下载出错文件没有删除，需要手动删除
# 4.多线程下载，不等待单个文件下载

import json
import os
import re
import urllib.request
import xml.etree.ElementTree

# python中文编码问题
import sys

# reload(sys)
# sys.setdefaultencoding('utf-8')

# 存储相关信息
mylist = []
# 当前文件夹所有文件
allFile = []
downloadFolder = "/Volumes/document/bilibili"

# 抓包获取的收藏地址
s = urllib.request.urlopen(
    "http://space.bilibili.com/ajax/fav/getList?mid=10732479&pagesize=30&fid=11485738&tid=0&kw=&pid=1").read().decode("utf8")
jsondata = json.loads(s)["data"]["vlist"]

# 获取相关数据
for av in jsondata:
    # url转换为专门解析哔哩哔哩的网站
    mydata = {
        "avId": "av" + str(av["aid"]),
        "name": av["title"].encode("utf8"),
        "url": av["link"].replace("bilibili", "ibilibili")
    }
    # 放入数据
    mylist.append(mydata)

for file in os.listdir(downloadFolder):
    allFile.append(file.split(".")[0])

# 准备下载
for data in mylist:

    str = urllib.request.urlopen(data["url"]).read().decode("utf8")

    # strEtree = xml.etree.ElementTree.fromstring(str)
    # strEtree.xpath("//*[@id=\"firstLi\"]/p/a")
    # 正则表达式解析得到下载地址
    downurl = re.findall(r'http://www.bilibilijj.com/Files/DownLoad/.*.mp4/www.bilibilijj.com.mp4\?mp3=true', str)[0]
    # 下载文件名获取
    filename = data["name"].decode('utf8').replace("/", "_", 99) + "." + downurl.split(".")[-1].split("?")[0]
    # 判断下载目录中是否存在已经下载的文件
    fileExist = False
    for file in allFile:
        if file in filename:
            fileExist = True
            continue
    if fileExist:
        # 跳过已经下载的文件
        continue
    # 输出下载文件名
    print(filename)
    # 输出文件下载路径
    print(downurl)
    # 下载获取文件
    filedata = urllib.request.urlopen(downurl)
    # 获取下载文件信息
    meta = filedata.info()
    # 获取文件大小
    file_size = int(meta.get("Content-Length")) / 1024 / 1024
    print("文件大小为：%dM" % (file_size))
    # 下载小于300M文件，防止内存不够，需要改进
    if file_size < 300:
        # 保存文件
        f = open(downloadFolder + "/" + filename, "wb")
        # 分段下载，没段多少，这里为1M
        block_sz = 1 * 1024 * 1024
        file_size_dl = 0
        # 读取下载文件保存
        while True:
            buffer = filedata.read(block_sz)
            print(">>>>%dM" % (file_size_dl / 1024 / 1024)),
            if not buffer:
                print("下载完成：%s" % filename)
                break
            file_size_dl += len(buffer)
            f.write(buffer)
        f.close()
