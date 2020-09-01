# 有道翻译表单伪造

## 一、简介

网址：http://fanyi.youdao.com/

效果：**模拟网页表单提交，实现实时翻译**

使用框架：**requests**

难度系数：**✩✩✩**

## 二、教程

### 1. 简介

> 有道翻译作为国内著名的翻译公司，他们也开设了在线翻译网站。本次我们的爬虫目标是爬取模拟有道翻译的表单提交，实现实时翻译的效果。

### 2. 网站分析

#### [网站首页](http://fanyi.youdao.com/)

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200901230306551.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTkz,size_16,color_FFFFFF,t_70#pic_center)

#### 尝试进行翻译

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200901230534630.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTkz,size_16,color_FFFFFF,t_70#pic_center)

#### 抓取网络请求

通过寻找发现在这个请求里有我们需要的结果，那么获取到这个请求我们就可以实现我们预期的效果了。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200901230607826.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTkz,size_16,color_FFFFFF,t_70#pic_center)

#### 分析表单

通过不同的请求分析表单参数

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200901231424241.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTkz,size_16,color_FFFFFF,t_70#pic_center)

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200901231500694.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTkz,size_16,color_FFFFFF,t_70#pic_center)

通过不同的请求我们可以发现表单变化的数据：

- **i**：被翻译的文本
- **salt**：时间戳
- **sign**：MD5 加密后的密文
- **lts**：时间戳，比 **salt** 多了一位
- **bv**：MD5 加密后的密文

#### 断点调试寻找表单数据

使用 **Ctrl + shift + F** 找到关键字所在的 JS 文件

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200901232344544.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTkz,size_16,color_FFFFFF,t_70#pic_center)

找到文件后， Ctrl + F 寻找关键字，然后在找到的关键字处打断点。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200901233229916.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTkz,size_16,color_FFFFFF,t_70#pic_center)

回到主页重新请求，可以发现程序网页暂停了，这个时候就是我们打的断点起作用了。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200901233443276.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTkz,size_16,color_FFFFFF,t_70#pic_center)

回到调试器发现没有任何变化，这就意味着程序运行到我们打的断点时没有产生 salt 值，直白点就是断点打错地方了。接下来的工作就是重复上述工作。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200901234309161.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTkz,size_16,color_FFFFFF,t_70#pic_center)

当我们打到这个位置的时候，终于发现了不得了的东西。在这里发现了所有我们需要的值，那么这里的 JS 代码就是我们需要破解的了：

![在这里插入图片描述](https://img-blog.csdnimg.cn/2020090123500255.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTkz,size_16,color_FFFFFF,t_70#pic_center)

#### 分析 JS 代码

```javascript
var r = function(e) {
    var t = n.md5(navigator.appVersion)  // navigator.appVersion的值为User-Agent，对该值进行md5加密
        , r = "" + (new Date).getTime()  // 获取当前时间戳
        , i = r + parseInt(10 * Math.random(), 10);  // 时间戳和一位随机数进行字符串拼接
        return {
            ts: r,
            bv: t,
            salt: i,
            sign: n.md5("fanyideskweb" + e + i + "]BjuETDhU)zqSxf-=B#7m")  // 字符串拼接后进行md5加密
    	}
 };
```

#### Python 代码实现

```python
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
```

表单伪造完成之后我们就可以数据请求了。数据请求部分比较简单，这里就不贴出详细教程了。具体代码可以在下面查看。