# 下载Bing每日壁纸并设为桌面

## 一、简介

网址：[https://cn.bing.com/?scope=web&FORM=ANNTH1](https://cn.bing.com/?scope=web&FORM=ANNTH1)

效果：**下载壁纸**

使用框架：**requests、win32gui、win32con、win32api**

难度系数：**✩✩**

## 二、教程

### 1. 简介

> 微软必应（英文名：Bing）是微软公司于2009年5月28日推出，用以取代Live Search的全新搜索引擎服务。为符合中国用户使用习惯，Bing中文品牌名为“必应”。「Bing」搜索最大的“特色”且与百度、Google 最大的不同就在于，它每天都会更新一张高清精美的背景图片，大多数是风景摄影作品，质量都非常高。

我们今天的任务就是下载下来 Bing 每天更新的壁纸，并且将他设为我们自己本地的桌面。

### 2. 网站分析

打开 [Bing](https://cn.bing.com/?scope=web&FORM=ANNTH1) ：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200807232428728.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTkz,size_16,color_FFFFFF,t_70)

后面这张美丽的壁纸就是我们本次的目标了。

审查网络请求我们发现了我们需要的信息：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200807232725615.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTkz,size_16,color_FFFFFF,t_70)

观察请求链接，分析数据：

```javascript
https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&nc=1596814004872&pid=hp&scope=web&FORM=BEHPTB&uhd=1&uhdwidth=2880&uhdheight=1620
```

- nc：当前时间的13位时间戳
- uhdwidth：宽为 2880
- uhdheight：高为 1620

### 3. 构造爬虫

> 这次的爬虫比较简单，也没有反爬措施，我们就直接上代码了

```python
import requests
import time
import os

# 提取链接
url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&nc={}"
timestamp = round(time.time() * 1000)
res = requests.get(url.format(timestamp))
pic_url = res.json()['images'][0]['url']
pic_url = "https://cn.bing.com{}".format(pic_url)

# 下载图片
today = time.strftime("%Y-%m-%d")
content = requests.get(url=self.pic_url).content
# 得到图片的绝对路径
self.pic_path = r"{}\img\{}.jpg".format(os.getcwd(), today)
with open(self.pic_path, 'wb') as f:
    f.write(content)
```

### 4. 设置桌面壁纸

设置桌面壁纸我们需要调用 Windows 的接口，我们需要使用 pip 下载 `win32gui、win32con、win32api` 这三个模块。

（Ps：我记得下载 win32gui 的时候有一些坑，小伙伴们可能需要自行解决一下）

**代码：**

```python
# 打开注册表
reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
# 2：拉伸  0：居中  6：适应  10：填充
win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "6")
# 设置桌面背景，路径需要传递绝对路径
win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, pic_path, win32con.SPIF_SENDWININICHANGE)
```

### 5. 后续

偶然间发现 Microsoft 出了 **[Bing Wallpaper](https://www.microsoft.com/en-gb/bing/bing-wallpaper?SilentAuth=1&wa=wsignin1.0)** 这款应用，的功能就是**获取每天 Bing 的壁纸并设为桌面**，感兴趣的小伙伴们可以看看。

### 6. 完整代码

[传送门](https://github.com/1314liuwei/python_spider/blob/master/No.5%20%E4%B8%8B%E8%BD%BDBing%E6%AF%8F%E6%97%A5%E5%A3%81%E7%BA%B8%E5%B9%B6%E8%AE%BE%E4%B8%BA%E6%A1%8C%E9%9D%A2/main.py)