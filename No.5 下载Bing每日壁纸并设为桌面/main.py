import requests
import time
import win32api
import win32con
import win32gui
import os


class Bing(object):
    def __init__(self):
        self.pic_url = None
        self.pic_path = None

        # 检查当前路径下有无'img'文件夹
        if 'img' not in os.listdir():
            os.mkdir('img')

    def spider(self):
        """
        获取图片链接
        :return:
        """
        url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&nc={}"
        timestamp = round(time.time() * 1000)
        res = requests.get(url.format(timestamp))
        pic_url = res.json()['images'][0]['url']
        self.pic_url = "https://cn.bing.com{}".format(pic_url)
        return self

    def downloadPicture(self):
        """
        下载图片
        :return:
        """
        # 获取当前日期
        today = time.strftime("%Y-%m-%d")
        content = requests.get(url=self.pic_url).content
        # 得到图片的绝对路径
        self.pic_path = r"{}\img\{}.jpg".format(os.getcwd(), today)
        # 下载图片
        with open(self.pic_path, 'wb') as f:
            f.write(content)
            return self

    def setupDesktop(self):
        """
        将图片设置为桌面
        :return:
        """
        # 打开注册表
        reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
        # 2：拉伸  0：居中  6：适应  10：填充
        win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "6")
        # 设置桌面背景，路径需要传递绝对路径
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, self.pic_path, win32con.SPIF_SENDWININICHANGE)
        return self


Bing().spider().downloadPicture().setupDesktop()
