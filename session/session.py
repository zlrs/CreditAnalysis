'''
    模拟登录教务系统，抓取成绩
'''
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlencode
import os, sys

def login(auth_url, data_url, headers, username, password):
    '''
    This function uses a session to perform all requests
    flow:
    1. login system
    - 'get' login page
    - parse login form
    - 'post' form
    2. fetch course data
    - 'get' page containing course data
    - if multi-login happens
    -     'get': redirect page according to guidence in html_response
    3. parse course data
    4. display course data
    '''
    s = requests.Session()
    auth_r = s.get(auth_url, headers = headers)
    if auth_r.status_code == 200:
        # parse for post_body
        post_body = {}
        soup = BeautifulSoup(auth_r.text, "lxml")
        form = soup.find_all("form", attrs = {"id": "casLoginForm"})[0]
        inputs = form.find_all("input")
        post_body = {}
        for i in inputs:
            post_body[i.attrs["name"]] = i.attrs["value"]  # "name": "value"
        post_body["username"] = username
        post_body["password"] = password
        post_url = "http://idas.uestc.edu.cn" + form["action"] # is like "http://idas.uestc.edu.cn/authserver/login/<may_have_more>"
        
        # perform post method
        print("Now performing post method...")
        print("post_body:", post_body)
        print("post_url:", post_url, end="\n\n")
        post_r = s.post(post_url, data=post_body)
        # print(post_r.headers)
        # print(post_r.text)
        
        # save post response
        try:
            with open(".\\post_response.html", "w", encoding = "utf-8") as f:
                f.write(post_r.text)
        except IOError:
            print("cannot write file .\\post_response.html")
    else:
        print("status_code: %d" % auth_r.status_code)
        sys.exit(0)
    
    data_r = s.get(data_url, headers = headers)
    data_soup = BeautifulSoup(data_r.text, "lxml")
    # 如果有重复登录，根据html中提示的导航到正确数据页面
    if data_soup.h2 and data_soup.h2.string.find("重复登录"):
        print("服务器提示账户有重复登录，正在重新导航...")
        if data_soup.a:
            print("正在访问a标签的href属性: ", data_soup.a.attrs["href"])
            data_r = s.get(data_soup.a.attrs["href"], headers = headers)
            data_soup = BeautifulSoup(data_r.text, "lxml")
        else:
            print("cannot find data_soup.a, place see response body blow: ")
            print(data_r.text)
    else:
        print("已到达数据页面")
    # 存储数据
    try:
        with open(".\\data_page.html", "w", encoding = "utf-8") as f:
            print("data_response_header:", data_r.headers)
            f.write(data_r.text)
    except IOError:
        print("cannot write file .\\data_page.html")

    # 可选需求 - 在此退出登录
    s.close()
    return data_r.text


def main():
    try:
        with open(".\\config.json", "r", encoding="utf-8") as fobj:
            config = json.load(fobj)
        # print(config)
    except IOError:
        print("can not open file config.json")
        
    try:
        login(config["auth_url"], config["data_url"], config["headers"], config["username"],
            config["password"])
        pass
    except IOError:
        print("login(): IOError")

    

main()