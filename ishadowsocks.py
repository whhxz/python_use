# -*- coding:utf-8 -*-
import urllib.request

import time
from lxml import etree
import tkinter

login_info = {}
change_password = False


def get_socks_password():
    url = "http://www.ishadowsocks.net"
    data = urllib.request.urlopen(url).read()
    data = data.decode('utf-8')
    html = etree.HTML(data)
    for num in range(3):
        find_password(html, num + 1)


def find_password(html, index):
    host = html.xpath("//*[@id=\"free\"]/div/div[2]/div[" + str(index) + "]/h4[1]")[0].text
    password = html.xpath("//*[@id=\"free\"]/div/div[2]/div[" + str(index) + "]/h4[3]")[0].text
    if password is None:
        del login_info[host]
    else:
        global change_password
        if login_info.get(host.split(":")[1]) != password.split(":")[1]:
            change_password = True
            login_info[host.split(":")[1]] = password.split(":")[1]
        else:
            change_password = False


def show_windows():
    root = tkinter.Tk()
    root.geometry("+1600+800")
    tkinter.Label(root, text="更新socks").grid(row=0)
    index = 1
    for (key, value) in login_info.items():
        tkinter.Label(root, text=key).grid(row=index)
        entry = tkinter.Entry(root)
        entry.insert(tkinter.INSERT, value)
        entry.grid(row=index, column=1)
        index += 1

    root.mainloop()


start_time = time.time()
while True:
    if time.time() > start_time + 5 * 60:
        get_socks_password()
        if change_password:
            show_windows()

        start_time = time.time()
    else:
        time.sleep(6)
