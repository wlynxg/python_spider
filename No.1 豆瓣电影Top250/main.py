import requests
import re
import os
import time

# 请求头
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/83.0.4103.14 Safari/537.36 "
}


def get_name_url(url: str, pattern: str):
    """
    获取图片的名字和url
    :param url: 网址
    :param pattern: 正则表达式
    :return: 结果集
    """
    response = requests.get(url=url, headers=headers)  # 获取网页源代码
    result = re.findall(pattern, response.text)  # 利用正则表达式提取信息
    return result


def download_picture(name: str, url: str):
    """
    下载图片保存至本地
    :param name: 图片名字
    :param url: 图片链接
    :return:
    """
    # 如果当前目录下没有“picture”文件夹就创建“picture”文件夹
    if 'picture' not in os.listdir():
        os.mkdir('picture')

    # 将数据写入图片
    with open(f"picture/{name}.jpg", 'wb') as f:
        response = requests.get(url, headers=headers)
        f.write(response.content)
        print(f'{name}.jpg 下载完成！')


def main():
    """
    主程序
    :return:
    """
    url = "https://movie.douban.com/top250?start={}"  # url
    pattern = '<img width="100" alt="(.*?)" src="(.*?)" class="">'  # 正则表达式
    result = []  # 图片信息结果集

    # 获取所有的图片名和链接
    for i in range(0, 251, 25):
        result += get_name_url(url.format(i), pattern)
        # 延时一秒是为了降低访问频率，爬虫运行时相当于在对网站进行DDOS攻击
        # 延时可以降低对网站造成的危害，我们要做一只有素质的爬虫
        time.sleep(1)

    # 下载图片到本地
    for name, url in result:
        download_picture(name, url)
        time.sleep(1)


if __name__ == '__main__':
    main()
