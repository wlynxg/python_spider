import requests
import json
import traceback
import time


def exception_capture(func):
    """
    装饰器
    :param func: 函数对象
    :return:
    """

    def work(*args, **kwargs):
        """
        捕捉异常并写入文件
        :param args: 位置参数
        :param kwargs: 关键字参数
        :return:
        """
        file = open("log.log", 'a', encoding='utf-8')
        try:
            func(*args, **kwargs)  # 调用函数
        except Exception as e:
            traceback.print_exc(limit=None, file=file)  # 捕捉异常
        file.close()

    return work


class Bilibili(object):
    """
    Bilibili搜索界面的爬虫
    搜索结果由两种API组成
    第一个API为第一个界面的数据，该API种包含有官方信息和第一页用户上传视频信息
    第二个API为用户上传视频的信息
    """
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/84.0.4147.89 Safari/537.36",
        'Referer': "https://search.bilibili.com"
    }

    file = open("log.log", 'a', encoding='utf-8')

    def __init__(self, keyword: str):
        self.keyword = keyword  # 搜索关键词

        self._numPages = 0
        self.get_official_works()
        self.get_user_works()

    @exception_capture
    def get_official_works(self):
        url = "https://api.bilibili.com/x/web-interface/search/all/v2?context=&page=1&order=&keyword={" \
              "}&duration=&tids_1=&tids_2=&__refresh__=true&_extra=&highlight=1&single_column=0&jsonp=jsonp&callback" \
              "=__jp0"
        response = requests.get(url=url.format(self.keyword), headers=self.headers).text  # 抓取结果
        data = json.loads(response[6:len(response) - 1])  # 返回结果非标准json，需要删去首尾冗余字符
        self._numPages = data['data']['numPages']  # 用户视频的页面数量
        for record in data['data']['result'][:9]:  # 最后一条记录为用户视频page=1时的信息，为避免重复输出，此处省略
            if record['data']:
                print(record['data'])

    @exception_capture
    def get_user_works(self):
        url = "https://api.bilibili.com/x/web-interface/search/type?context=&page={}&order=&keyword={" \
              "}duration=&tids_1=&tids_2=&__refresh__=true&_extra=&search_type=video&highlight=1&single_column=0" \
              "&jsonp=jsonp&callback=__jp0"
        for i in range(1, self._numPages + 1):
            response = requests.get(url=url.format(i, self.keyword), headers=self.headers).text
            data = json.loads(response[6:len(response) - 1])
            for record in data['data']['result']:
                print(record['author'], record['title'].replace('<em class="keyword">', '').replace('</em>', ''),
                      record['arcurl'])

            time.sleep(2)  # 停一下，别过分了


a = Bilibili('约会大作战')
