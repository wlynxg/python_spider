import requests
import random
import math
import base64
from Crypto.Cipher import AES


class Encryption(object):
    def func_a(self, a):
        b, c = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", ""
        for d in range(a):
            e = random.random() * b.__len__()
            e = math.floor(e)
            c += b[e]
        return c

    def func_b(self, a, b):
        iv = "0102030405060708"
        pad: int = 16 - len(a) % 16
        a += pad * chr(pad)
        encrypt = AES.new(b.encode('utf-8'), AES.MODE_CBC, iv.encode())
        encrypt_text = encrypt.encrypt(a.encode())
        encrypt_text = base64.b64encode(encrypt_text)
        return encrypt_text.decode('utf-8')

    def func_c(self, a, b, c):
        num = pow(int(a[::-1].encode().hex(), 16), int(b, 16), int(c, 16))
        return format(num, 'x')

    def func_d(self, d, e, f, g):
        h, i = {}, self.func_a(16)
        h['encText'] = self.func_b(d, g)
        h['encText'] = self.func_b(h['encText'], i)
        h['encSecKey'] = self.func_c(i, e, f)
        return h


class WangYiYun(Encryption):
    def __init__(self, url):
        self.url = url

    def spider(self):
        d = '{"rid":"R_SO_4_1492319432","threadId":"R_SO_4_1492319432","pageNo":"1","pageSize":"20","cursor":"-1","offset":"0","orderType":"1","csrf_token":""}'
        e = "010001"
        f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341" \
            "f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        g = "0CoJUm6Qyw8W8jud"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"
        }

        data0 = self.func_d(d, e, f, g)
        data = {
            'params': data0['encText'],
            'encSecKey': data0['encSecKey']
        }
        print(data)
        session = requests.session()
        session.get("https://music.163.com/", headers=headers)
        result = session.post(self.url, headers=headers, data=data)
        return result.text


if __name__ == '__main__':
    a = WangYiYun("https://music.163.com/weapi/comment/resource/comments/get?csrf_token=")
    print(a.spider())

