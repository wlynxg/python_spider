import requests
import os
import time
import random
import pymysql
import json


class Lagou(object):
    def __init__(self, keyword):
        self.kw = keyword
        self.spider()

    def spider(self):
        """
        爬虫主程序
        :return:
        """
        if 'data' not in os.listdir():  # 判断有无 "data" 目录
            os.mkdir('data')

        # 用于建立 session 的链接
        url1 = "https://www.lagou.com/jobs/list_/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput="
        # 用于获取数据的链接
        url2 = "https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"
        # 请求头
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
            'Referer': 'https://www.lagou.com/jobs/list_/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput='
        }

        # 建立 session
        session = requests.session()
        # 模拟登录，伪造访问地址
        session.get(url1, headers=header)

        count = 1
        while True:
            data = {
                'first': 'false',
                'pn': count,
                'kd': self.kw
            }  # pn 代表着页数， kd 代表着关键字
            # Post方法请求数据
            resp = session.post(url2, data=data, headers=header)
            try:
                if resp.json()['content']["pageNo"] != 0:  # 当 pageNo 等于0时代表着数据已经爬取完
                    # 将数据写入文件方便下一步的操作
                    with open(f"data/{count}.json", 'w', encoding='utf-8') as f:
                        f.write(resp.text)
                        print(f"第{count}页数据已经下载完毕！")
                        time.sleep(5)  # 做一个君子
                else:
                    break
            except KeyError:  # 系统会检测我们的爬虫，如果出现了这个异常说明我们的爬虫已经被系统检测到，需要重新建立 session
                session = requests.session()
                session.get(url1, headers=header)
            finally:
                count += 1

if __name__ == '__main__':
    Lagou('爬虫')

