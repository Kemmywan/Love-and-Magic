国庆假期结束...先来几道crypto活跃一下大脑！

嘿嘿这个季度又可以看到小栗帽了真是开心！

（buuoj）

![alt text](424166855bffd269a47c2877f8abe93d.png)

buuoj娘镇楼

## 一眼就解密

ZmxhZ3tUSEVfRkxBR19PRl9USElTX1NUUklOR30=

有大小写和数字，还有等号，是base64！

## md5

e00cf25ad42683b3df678c61f42c6bda

题目提示是md5，先浅浅学习一下：

MD5（Message Digest Algorithm 5）是一种哈希函数，常用于对数据进行摘要、校验和加密存储。它将任意长度的数据“压缩”成一个128位（16字节，32位十六进制）的哈希值。MD5 由 Ronald Rivest 在1991年设计，是MD系列的第五个版本。

那么这个32位的字符串毫无疑问是hex格式的md5哈希值

查了一下这个哈希值，是一个很经典的md5哈希值，其原文是：

e00cf25ad42683b3df678c61f42c6bda -> admin1

关于md5的解密，也可以用下面这个网站！

https://www.cmd5.com/

## Url编码

%66%6c%61%67%7b%61%6e%64%20%31%3d%31%7d

用cyberchef进行url-decode即可

## 看我回旋踢

synt{5pq1004q-86n5-46q8-o720-oro5on0417r1}

看起来就是rot密码，用cyberchef解密即可，就是最经典的rot13

## 摩丝

.. .-.. --- ...- . -.-- --- ..-

摩丝密码！用cyberchef解密即可。

趁机补一补摩斯密码的课：

- 点（· 或 .）：短促信号，读作“滴”；划（– 或 -）：长信号，读作“嗒”

- 同一字母的各个点和划之间：间隔一个单位时长
    
- 同一单词内相邻字母之间：间隔三个单位时长
    
- 单词之间：间隔七个单位时长

一般解码用大写！除非特别说明

## password

这样的乱码一般是因为误把gbk编码当作utf-8打开导致的！

用python解码得到：

姓名：张三 
生日：19900315

key格式为key{xxxxxxxxxx}

自然猜出flag{zs19900315}

了解一下gbk编码：

### gbk

GBK（全称：汉字内码扩展规范，Chinese Internal Code Specification）是中国大陆广泛使用的一种汉字编码方式，是对GB2312的扩展。

双字节编码为主：GBK采用变长编码方式，英文字符用1字节，汉字和其他字符用2字节。

第一个字节范围：0x81-0xFE

第二个字节范围：0x40-0xFE（去除0x7F）

如果用UTF-8方式打开GBK编码的文件，中文部分通常会出现乱码（如“ÕÅÈý”）。

不支持全球所有字符：GBK主要面向中文，不能覆盖所有Unicode字符。

与Unicode不兼容：需要转换才能和Unicode/UTF-8互操作。

## 变异凯撒

afZ_r9VYfScOeO_UL^RWUc

这显然不是正常的凯撒密码，出现了非字母字符，而且还区分大小写...

61 66 5a 5f 72 39 56 59 66 53 63 4f 65 4f 5f 55 4c 5e 52 57 55 63

把hex值写出来观察，本来想的是每个hex值加上一个固定的值，但是发现不太对，因为f-a=5而l-f=6，

当然是要和提示对照，说明flag{对应前五个字母，那就来做一下减法：

f-a=5
l-f=6
a-Z=7

哦哦哦懂了，应该是我们的位移值也在不断增加，写一个python程序即可。

得到flag也就是题目的名字：

flag{Caesar_variation}

## Quoted-printable

=E9=82=A3=E4=BD=A0=E4=B9=9F=E5=BE=88=E6=A3=92=E5=93=A6

学习一下！

Quoted-printable（简称QP编码）是一种可打印字符编码方式，主要应用于电子邮件（MIME标准），用于安全地传输包含非ASCII字符（如中文、特殊符号等）的文本数据。它的设计目的是让数据在只支持7位ASCII字符的通道中也能被安全传递，并保持可读性。

Quoted-printable的基本规则

- 编码范围
    - 可直接打印的ASCII字符（33–60、62–126，除了等号=）原样输出。
    - 其他字节（包括非ASCII字符、控制字符、=本身）都被编码成=XX形式，其中XX是两位十六进制数（大写）。

- 等号（=）的作用
    - =是Quoted-printable的转义符。例如，中文“你”在UTF-8下的一个字节可能会被编码为=E4。

- 换行处理
    - QP编码每行最多76个字符，超出需要软换行（用等号=结尾，表示本行未结束，下一行继续）。
    - 原始文本中的换行符（CRLF）会被保留。

- 空格和制表符
    - 行尾的空格和Tab必须编码（如=20、=09），否则有些邮件服务器会自动去除行尾空白，导致内容丢失。

用python库解码即可!

解码出来是

那你也很棒哦

很暖心的flag呢！

## 篱笆墙的影子

felhaagv{ewtehtehfilnakgw}

仔细观察怎么感觉前面这里面已经出现了flag这个单词呢？

再看看，发现应该是把原文里的奇数位提前偶数位放后的加密方法，还原出来的flag自然是语义通顺的一句话：

flag{wethinkwehavetheflag} 

## Rabbit

U2FsdGVkX1/+ydnDPowGbjjJXhZxm2MP2AgI

Rabbit 是一种设计用于高效加密的流密码算法（stream cipher），由 Martin Boesgaard、Mette Vesterager、Thomas Pedersen、Jesper Christiansen 和 Ove Scavenius 于2003年提出。它是 eSTREAM 项目（一个欧洲流加密算法竞赛）的候选算法之一。

- 主要特点

- 用途：Rabbit 主要用于加密数据流，适合高性能环境（如网络通信、嵌入式系统等）。
- 密钥长度：128位（16字节）
- 初始向量（IV）长度：64位（8字节）
- 速度：Rabbit 非常快，在软件实现上能达到极高的加解密速度。
- 安全性：目前没有公开的实用攻击能破解Rabbit，安全性较好（但主流安全场景更多推荐AES-CTR、ChaCha20等）。

用下面这个网站可以进行rabbit的加解密：

http://www.jsons.cn/rabbitencrypt/

得到结果：

Cute_Rabbit

## RSA

有一点乱码，用gbk解码：

在一次RSA密钥对生成中，假设p=473398607161，q=4511491，e=17
求解出d作为flga提交

用python自带的逆元运算即可







