import re
import os
import time
import random

import requests
from selenium import webdriver


def download_html(url: str, file: str):
    """
    利用selenium框架调用浏览器，下载js渲染后的页面代码
    :param url: 网址
    :param file: html文件名字
    :return:
    """
    # 这里我调用的是FireFox来渲染网页，大家也可以用其它浏览器来渲染页面，不过要下载对应得驱动才行
    # FireFox驱动下载：https://github.com/mozilla/geckodriver/releases
    # Google Chrome：http://npm.taobao.org/mirrors/chromedriver/
    driver = webdriver.Firefox(executable_path=r'geckodriver.exe')  # 调用驱动，我的浏览器版本78.0.2
    driver.get(url)  # 加载网页

    time.sleep(30)  # 暂停30s,在这个时间内进行登陆操作

    driver.find_element_by_class_name('fold').click()  # 触发点击操作
    time.sleep(2)
    with open(file, 'w', encoding='utf-8') as f:  # 下载网页
        f.write(driver.page_source)
    driver.close()


def download_css(html: str, css: str):
    """
    根据网页下载css文件
    :param html:
    :param css:
    :return:
    """
    with open(html, 'r', encoding='utf-8') as f:
        html = f.read()

    css_url = re.findall('<link rel="stylesheet" type="text/css" href="(.*?)">', html, re.S)  # 提取链接
    css_url = 'http:{}'.format(css_url[1])
    css_content = requests.get(css_url).text
    with open(css, 'w', encoding='utf-8') as f:  # 保存css文件
        f.write(css_content)


def down_load_fontLibrary(css: str, fontLibrary: str):
    """
    根据css文件下载字体库
    :param css: css文件
    :param fontLibrary: 下载的字体库文件名字
    :return:
    """
    with open(css, 'r', encoding='utf-8') as f:
        css_content = f.read()

    font = re.findall('background-image: url\((.*?)\);', css_content, re.S)  # 提取链接
    font_url = 'http:{}'.format(font[1])
    font_content = requests.get(font_url).text
    with open(fontLibrary, 'w', encoding='utf-8') as f:  # 保存文件
        f.write(font_content)


def restore_text(css: str, font_library: str, html: str):
    """
    还原原始评论
    :param css: 用于加密的css文件
    :param fontLibrary: 字体库文件
    :param html: 原始html文件
    :return:
    """
    with open(css, 'r', encoding='utf-8') as f:
        css = f.read()

    with open(html, 'r', encoding='utf-8') as f:
        html = f.read()

    with open(font_library, 'r', encoding='utf-8') as f:
        font_library = f.read()

    inf = re.findall('<div class="review-words(.*?)<div class="less-words">', html, re.S)
    for record in inf:
        inf_copy = record
        svgmti = re.findall('<svgmtsi class="(.*?)">', record)
        for class_name in svgmti:
            XY = re.findall('.%s{background:-(.*?)px -(.*?)px;}' % class_name, css, re.S)
            X = int(float(XY[0][0]) / 14)  # 被替换的文字X坐标换算为字体库的X
            Y = int(float(XY[0][1]) + 23)  # 被替换的文字Y坐标换算为字体库的Y
            fo = re.findall('<text x="0" y="%s">(.*?)</text>' % Y, font_library)
            inf_copy = re.sub(f'<svgmtsi class="{class_name}"></svgmtsi>', fo[0][X], inf_copy, count=0)

        # 删除干扰字符
        inf_copy = re.sub('<img .*? alt="">', '', inf_copy, count=0)
        inf_copy = re.sub('</div>.*?<div class="review-words', '', inf_copy, count=0, flags=re.S)
        inf_copy = inf_copy.replace('Hide">', '')
        inf_copy = inf_copy.replace('">', '')
        inf_copy = inf_copy.replace('\n', '')
        inf_copy = inf_copy.replace(' ', '')
        inf_copy = inf_copy.strip()

        print(inf_copy)


def create_folder():
    """
    检测当前目录下是否创建了这三个文件夹，没有则创建
    :return:
    """
    ls = os.listdir()
    if "html" not in ls:
        os.mkdir("html")

    if "css" not in ls:
        os.mkdir("css")

    if "font" not in ls:
        os.mkdir("css")


def main():
    """
    主程序
    :return:
    """
    create_folder()
    url = 'http://www.dianping.com/shop/G41gaJfqGBICtiVY/review_all/p{}'
    for i in range(1, 3):
        download_html(url.format(i), "html/p1.html")
    download_css("html/1.html", "css/font.css")
    down_load_fontLibrary("css/font.css", "font/font.swg")

    for i in range(1, 3):
        restore_text("css/font.css", "font/font.swg", f"html/p{i}.html")


if __name__ == "__main__":
    main()
