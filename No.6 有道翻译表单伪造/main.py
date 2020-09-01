import requests
import time
import random
from hashlib import md5


class YouDao(object):
    """
    输入关键词
    """
    def __init__(self, keyword):
        self.keyword = keyword
        self.get_response()

    def get_response(self):
        """
        提交表单得到响应
        :return:
        """
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Content-Length": "252",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "fanyi.youdao.com",
            "Origin": "http://fanyi.youdao.com",
            "Referer": "http://fanyi.youdao.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }

        get_url = "http://fanyi.youdao.com/"
        post_url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"

        session = requests.session()
        session.get(url=get_url)
        data = self._fake_form()
        response = session.post(url=post_url, headers=headers, data=data)
        self._parse_response(response)

    def _fake_form(self):
        """
        伪造表单
        :return: 表单
        """
        # 静态数据
        data = {
            "i": "爬虫",
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME"
        }

        enc = md5()
        enc.update(
            "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 "
            "Safari/537.36".encode())
        data['bv'] = enc.hexdigest()
        data['lts'] = time.time() * 1000
        data['salt'] = data['lts'] + random.randint(0, 9)

        enc = md5()
        sign = f"fanyideskweb{self.keyword}{data['salt']}]BjuETDhU)zqSxf-=B#7m"
        enc.update(sign.encode())
        data['sign'] = enc.hexdigest()
        return data

    def _parse_response(self, response):
        """
        解析响应的数据
        :param response:
        :return:
        """
        if response.status_code == 200:
            self.result = response.json()['translateResult'][0][0]['tgt']
        else:
            self.result = "未查询到翻译结果"

    def __str__(self):
        return self.result


print(YouDao("爬虫"))
