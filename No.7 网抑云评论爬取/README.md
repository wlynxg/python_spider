# 网抑云评论爬取

## 简介

网址：https://music.163.com/#/song?id=1492319432

效果：**破解JS加密，爬取评论**

使用框架：**requests**

难度系数：**✩✩✩✩**

## 一、网站分析

**目标网址**：https://music.163.com/#/song?id=1492319432

按 F12 进入 Network，发现评论数据都在 **get?csrf_token=** 这个请求中，观察请求头：

![img](https://img-blog.csdnimg.cn/20201107102211364.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTkz,size_16,color_FFFFFF,t_70#pic_center)

观察请求头发现该请求是一个 **POST请求**，表单中提交了一个 **params** 和 **encSecKey**。这两个数据都是一串密文，只能弄清楚它的加密过程才能构造。

接下来的工作就是摸清楚这两个参数的加密过程了！

## 二、JS加密

### 1. 调试 JS 代码

![img](https://img-blog.csdnimg.cn/20201107103258809.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTkz,size_16,color_FFFFFF,t_70#pic_center)

**Ctrl+Shift+F** 查找参数，进入 JS 代码：

![img](https://img-blog.csdnimg.cn/20201107103620711.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTkz,size_16,color_FFFFFF,t_70#pic_center)

由于这些 JS代码都是被丑化压缩过的，原始的 JS代码不适合我们观察，因此我们有必要将丑化的 JS代码进行美化。按下那个 **“{}”**键即可将丑化的 JS代码进行美化。

![img](https://img-blog.csdnimg.cn/20201107104238224.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTkz,size_16,color_FFFFFF,t_70#pic_center)

在美化后的代码里，按 **Ctrl+F** 查找关键字，找寻JS的加密过程。

### 2. 整理得到  JS  加密部分代码

```js
var bZj7c = window.asrsea(JSON.stringify(i8a), bkk7d(["流泪", "强"]), bkk7d(YR2x.md), bkk7d(["爱心", "女孩", "惊恐", "大笑"]));
e8e.data = j8b.cr9i({
    params: bZj7c.encText,
    encSecKey: bZj7c.encSecKey
})


!function() {
    function a(a) {
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length,
            e = Math.floor(e),
            c += b.charAt(e);
        return c
    }
    function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {
            iv: d,
            mode: CryptoJS.mode.CBC
        });
        return f.toString()
    }
    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) {
        var h = {}
          , i = a(16);
        return h.encText = b(d, g),
        h.encText = b(h.encText, i),
        h.encSecKey = c(i, e, f),
        h
    }
    function e(a, b, d, e) {
        var f = {};
        return f.encText = c(a + e, b, d),
        f
    }
    window.asrsea = d,
    window.ecnonasr = e
}();

function encryptedString(a, b) {
    for (var f, g, h, i, j, k, l, c = new Array, d = b.length, e = 0; d > e; )
        c[e] = b.charCodeAt(e),
        e++;
    for (; 0 != c.length % a.chunkSize; )
        c[e++] = 0;
    for (f = c.length,
    g = "",
    e = 0; f > e; e += a.chunkSize) {
        for (j = new BigInt,
        h = 0,
        i = e; i < e + a.chunkSize; ++h)
            j.digits[h] = c[i++],
            j.digits[h] += c[i++] << 8;
        k = a.barrett.powMod(j, a.e),
        l = 16 == a.radix ? biToHex(k) : biToString(k, a.radix),
        g += l + " "
    }
    return g.substring(0, g.length - 1)
}
```

找到 JS 的加密代码之后就需要用 Python 来实现了。

## 三、JS断点调试

在分析 JS 代码的时候，我们对于代码中某些函数或者某些值不清楚，这个时候我们就可以在谷歌浏览器中使用断点调试的方式来帮助我们理解 JS 代码。

下面简单介绍一下断点调试的步骤：

### 1. 打断点

![img](https://img-blog.csdnimg.cn/20201107230929512.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTkz,size_16,color_FFFFFF,t_70#pic_center)![在这里插入图片描述](https://img-blog.csdnimg.cn/20201107230929512.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTkz,size_16,color_FFFFFF,t_70#pic_center)

在箭头指向的位置点击一下即代表打下了一个断点。

### 2. 刷新网页

![img](https://img-blog.csdnimg.cn/20201107230559454.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTkz,size_16,color_FFFFFF,t_70#pic_center)

回到原网页中，刷新网页。此时可以发现网页没有全部加载，这是因为JS代码只运行到我们打下断点的位置就没有运行了。

### 3.  观察值

![img](https://img-blog.csdnimg.cn/20201107230409322.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTkz,size_16,color_FFFFFF,t_70#pic_center)

此时在右侧即可发现运行到当前位置时各个变量的值。此时即可对值进行分析。

### 4. 单步调试

![img](https://img-blog.csdnimg.cn/20201107231306389.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQzNTgwMTkz,size_16,color_FFFFFF,t_70#pic_center)

打下另一个断点后，点击箭头指向处按钮即可运行至下一个断点处。

## 四、Python 构造加密

### 1. 函数 a

```JS
function a(a) {
    var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
    for (d = 0; a > d; d += 1)
    e = Math.random() * b.length,
    e = Math.floor(e),
    c += b.charAt(e);
    return c
}
```

该函数主要作用是 **返回一个随机产生的16位字符串**。

```Python
def func_a(self, a):
    b, c = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", ""
    for d in range(a):
    e = random.random() * b.__len__()
    e = math.floor(e)
    c += b[e]
	return c
```

### 2. 函数b

```JS
function b(a, b) {
    var c = CryptoJS.enc.Utf8.parse(b)
      , d = CryptoJS.enc.Utf8.parse("0102030405060708")
      , e = CryptoJS.enc.Utf8.parse(a)
      , f = CryptoJS.AES.encrypt(e, c, {
        iv: d,
        mode: CryptoJS.mode.CBC
    });
    return f.toString()
}
```

查询了一下，这个函数的主要目的是对**参数 b** 以 **CBC 模式**进行 **AES 加密**，然后返回加密后的结果。

> 密码学中的高级加密标准（Advanced Encryption Standard，AES），又称Rijndael[加密法](https://baike.baidu.com/item/加密法)，是美国联邦政府采用的一种区块加密标准。
>
> AES加密过程是在一个4×4的[字节](https://baike.baidu.com/item/字节)矩阵上运作，这个矩阵又称为“体（state）”，其初值就是一个明文区块（矩阵中一个元素大小就是明文区块中的一个Byte）。

Python 中的 **Crypto库** 实现了多种加密过程，我们可以使用它进行 **AES加密**，这个需要自己 pip 安装一下：

> pip install Crypto

```Python
def func_b(self, a, b):
    iv = "0102030405060708"
    pad: int = 16 - len(a) % 16
    a += pad * chr(pad)
    encrypt = AES.new(b.encode('utf-8'), AES.MODE_CBC, iv.encode())
    encrypt_text = encrypt.encrypt(a.encode())
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text.decode('utf-8')
```

### 3. 函数c

```JS
function c(a, b, c) {
    var d, e;
    return setMaxDigits(131),
    d = new RSAKeyPair(b,"",c),
    e = encryptedString(d, a)
}

function encryptedString(a, b) {
    for (var f, g, h, i, j, k, l, c = new Array, d = b.length, e = 0; d > e; )
        c[e] = b.charCodeAt(e),
        e++;
    for (; 0 != c.length % a.chunkSize; )
        c[e++] = 0;
    for (f = c.length,
    g = "",
    e = 0; f > e; e += a.chunkSize) {
        for (j = new BigInt,
        h = 0,
        i = e; i < e + a.chunkSize; ++h)
            j.digits[h] = c[i++],
            j.digits[h] += c[i++] << 8;
        k = a.barrett.powMod(j, a.e),
        l = 16 == a.radix ? biToHex(k) : biToString(k, a.radix),
        g += l + " "
    }
    return g.substring(0, g.length - 1)
}
```

该函数主要实现的是对 **参数a 以从后向前的方向** 进行 **RSA加密**。

本来还是想利用 Crypto库 进行 RSA加密 的，但是在使用的时候由于版本问题出现了一些问题，于是采用手工实现的方法进行 加密了。

> RSA公开密钥密码体制是一种使用不同的加密密钥与解密密钥，“由已知加密密钥推导出解密密钥在计算上是不可行的”密码体制。
>
> RSA算法的原理：
>
> 加密：m^e % n = c
>
> 解密：c^d % n = m
>
> m：原始数据；c：密文；n、e：公钥；n、d：私钥

```Python
def func_c(self, a, b, c):
    num = pow(int(a[::-1].encode().hex(), 16), int(b, 16), int(c, 16))
    return format(num, 'x')
```

### 4. 函数d

```JS
function d(d, e, f, g) {
    var h = {}
      , i = a(16);
    return h.encText = b(d, g),
    h.encText = b(h.encText, i),
    h.encSecKey = c(i, e, f),
    h
}
```

该函数的主要作用是**调用其它的三个函数实现加密过程**。

```Python
    def func_d(self, d, e, f, g):
        h, i = {}, func_a(16)
        h['encText'] = self.func_b(d, g)
        h['encText'] = self.func_b(h['encText'], i)
        h['encSecKey'] = self.func_c(i, e, f)
        return h
```

## 五、中途遇到的问题

开始以为 **函数d** 中的 **变量d** 为 **{"csrf_token":""}**，然后将该变量进行参与加密，加密结果与 JS调试时得到的值一毛一样。说明我们构造的函数是正确的。

但是将得到的参数带入表单进行爬取时，给我们的返回值却总是：

```json
{"msg":"参数错误","code":400}
```

心态有点炸了。

然后观察网页请求的 **params**，发现它是 **256位** 的，但是我们加密得到的却是 **64位** 的！

这就说明我们加密的参数长度不够啊！

经过多次断点调试，发现 **参数d** 是变化的！！！

**{"csrf_token":""}** 只是它第一次的值，它的值后面还会变化。。。

多次断点调试后发现 d值为：

```json
1. "{"csrf_token":""}"
2. "{"platform":"web","product":"cloudmusic","csrf_token":""}"
3. "{"rid":"R_SO_4_1492319432","threadId":"R_SO_4_1492319432","pageNo":"1","pageSize":"20","cursor":"-1","offset":"0","orderType":"1","csrf_token":""}"
4. "{"id":"1492319432","lv":-1,"tv":-1,"csrf_token":""}"
5. "{"logs":"[{\"action\":\"commentimpress\",\"json\":{\"type\":\"song\",\"cid\":3599061418,\"sourceid\":\"1492319432\"}},{\"action\":\"commentimpress\",\"json\":{\"type\":\"song\",\"cid\":3599127936,\"sourceid\":\"1492319432\"}},{\"action\":\"commentimpress\",\"json\":{\"type\":\"song\",\"cid\":3599056529,\"sourceid\":\"1492319432\"}},{\"action\":\"commentimpress\",\"json\":{\"type\":\"song\",\"cid\":3599043614,\"sourceid\":\"1492319432\"}},{\"action\":\"commentimpress\",\"json\":{\"type\":\"song\",\"cid\":3599041736,\"sourceid\":\"1492319432\"}},{\"action\":\"commentimpress\",\"json\":{\"type\":\"song\",\"cid\":3599111999,\"sourceid\":\"1492319432\"}},{\"action\":\"commentimpress\",\"json\":{\"type\":\"song\",\"cid\":3599095072,\"sourceid\":\"1492319432\"}},{\"action\":\"commentimpress\",\"json\":{\"type\":\"song\",\"cid\":3599094042,\"sourceid\":\"1492319432\"}},{\"action\":\"commentimpress\",\"json\":{\"type\":\"song\",\"cid\":3599042584,\"sourceid\":\"1492319432\"}},{\"action\":\"commentimpress\",\"json\":{\"type\":\"song\",\"cid\":3599032785,\"sourceid\":\"1492319432\"}},{\"action\":\"commentimpress\",\"json\":{\"type\":\"song\",\"cid\":3599075137,\"sourceid\":\"1492319432\"}},{\"action\":\"commentimpress\",\"json\":{\"type\":\"song\",\"cid\":3599024799,\"sourceid\":\"1492319432\"}},{\"action\":\"commentimpress\",\"json\":{\"type\":\"song\",\"cid\":3599061249,\"sourceid\":\"1492319432\"}},{\"action\":\"commentimpress\",\"json\":{\"type\":\"song\",\"cid\":3599102881,\"sourceid\":\"1492319432\"}},{\"action\":\"commentimpress\",\"json\":{\"type\":\"song\",\"cid\":3599110809,\"sourceid\":\"1492319432\"}},{\"action\":\"commentimpress\",\"json\":{\"type\":\"song\",\"cid\":3599105822,\"sourceid\":\"1492319432\"}},{\"action\":\"commentimpress\",\"json\":{\"type\":\"song\",\"cid\":3598993744,\"sourceid\":\"1492319432\"}},{\"action\":\"commentimpress\",\"json\":{\"type\":\"song\",\"cid\":3599055174,\"sourceid\":\"1492319432\"}},{\"action\":\"commentimpress\",\"json\":{\"type\":\"song\",\"cid\":3599039376,\"sourceid\":\"1492319432\"}},{\"action\":\"commentimpress\",\"json\":{\"type\":\"song\",\"cid\":3599071873,\"sourceid\":\"1492319432\"}}]","csrf_token":""}"
```

最后发现，当 d为**{"rid":"R_SO_4_1492319432","threadId":"R_SO_4_1492319432","pageNo":"1","pageSize":"20","cursor":"-1","offset":"0","orderType":"1","csrf_token":""}** 时，得到的是正确的加密结果！