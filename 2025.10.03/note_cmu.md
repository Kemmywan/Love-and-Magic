## Crack the Power

这是一道和密码有关的解密题，一眼RSA，给到的公钥n,e和密文c，但是e=20让人一头雾水，感觉是经过了加密

想了很久百思不得其解...先做web吧

## Crack the Gate 1

根据提示查看源代码，发现下面这行字：

ABGR: Wnpx - grzcbenel olcnff: hfr urnqre "K-Qri-Npprff: lrf" 

在Cyperchef上用ROT13（凯撒密码）来解密，前走13位得到解密后的信息：

NOTE: Jack - temporary bypass: use header "X-Dev-Access: yes" 

看来是要我们使用bs去抓包改报文，只要添上这个一个标注应该就可以bypass。

尝试了发现不行？看scripts标签里的代码，是用POST来传参数的，那么我们填一下用户名和密码然后再用bs请求，加上我们的bypass-header，这次大公告成了。

趁此机会复习一下GET和POST的区别吧！

GET 和 POST 都是 HTTP 协议中最常用的两种请求方式（方法），但它们的用途、行为和安全性等方面有显著区别。下面详细介绍：

- GET
    - 用途
        - 用于向服务器请求数据（获取资源）。
        - 例如：访问网页、查询信息。
    - 参数传递
        - 参数通过 URL 传递（如 ?key1=value1&key2=value2）。
        - 例如：http://example.com/search?query=test
    - 安全性
        - 参数暴露在URL中，不适合传递敏感信息（如密码）。
        - 浏览器、代理、服务器都可能记录URL。
    - 长度限制
        - URL有长度限制（通常2KB~8KB）。
    - 幂等性
        - 多次GET请求同一资源，结果应相同（不改变服务器状态）。
    - 可缓存
        - GET请求可被缓存、收藏、保存在浏览器历史记录中。
- POST
    - 用途
        - 用于向服务器提交数据（如表单、上传文件），通常会修改服务器数据（如注册、登录、发帖）。
    - 参数传递
        - 参数在请求体（body）中，URL中不显示。
        - 例：

            POST /login HTTP/1.1
            Host: example.com
            Content-Type: application/x-www-form-urlencoded

            username=abc&password=123
    - 安全性
        - 参数不会暴露在URL中，相对GET更适合传敏感信息，但仍需HTTPS保障安全。
    - 长度限制
        - 理论上没有大小限制（实际受服务器设置影响）。
    - 幂等性
        - 非幂等，多次POST请求可能导致多次插入、提交等动作。
    - 不可缓存
        - 默认不会被缓存，也不会被浏览器保存到历史记录。


## Crack the Gate 2

还是老样子登录网站，不过这次源代码里没有给我们producer_bypass了

这里发现账号一定要用给的那个org_url，不然没法POST上去

然后在POST命令里，我们开始试密码，用题目给的密码本

发现同ip不能连续试，也很简单，用X-Forwarded-For伪造一下，就这样手动把密码试出来就可以。

（下次应该打个python脚本来解决这件事情，试得手有点累

## byp4ss3d

明显是一道文件上传漏洞题，我们先随便上传一下我们的一句话木马，

上传php格式会报错，看来我们又要用非常经典的图片绕过，

名字改成1.jpg，文件类型改成images/jpg，

上传成功！

但是直接在url里打开不了，显示图片无法显示。看来是apache的框架默认按照文件类型来解析文件，这下有点难办。

于是又学到了新东西：apache的.htaccess文件！

```
<FilesMatch "1.jpg">
	SetHandler application/x-httpd-php
</FilesMatch>
```

内容大概就是这样子，看个大概也知道这个文件是用来配置文件的解析的，这里我们直接精准匹配到我们的木马文件。

**.htaccess** 文件是 Apache Web 服务器中用于进行目录级配置的一个特殊的隐藏配置文件（以点号开头）。它的作用是允许网站管理员在不修改主配置文件（如 httpd.conf）的情况下，对单独目录或子目录进行灵活设置。

也就是它只要放在我们的上传目录就对目录下所有文件生效！

这里起到的只是一个解析规则的添加，还有很多别的用法，以后可能还会遇到，至少这样子之后我们就可以上传我们的木马。

用phpinfo()测试，生效！再看几眼Index.php也可以知道这次只审核了文件类型和后缀名，真是轻轻又松松啊

接下来就是在服务器里找flag时间！根目录下有一个challenge目录，感觉flag就在里面，但是打不开？

-ld看权限，发现是500，然后...然后我就一直研究怎么提权研究了一个小时...

艹！仔细一想，这个服务器各方面都很新很完善，怎么想也没法给我提权吧？

绝望中我想到有可能flag在别的地方，那就用find找一下吧！

```bash
find / -type f -iname "*flag*" 2>/dev/null
```

在根目录下寻找所有文件名带flag的文件（不区分大小写），2/dev/null是用来丢弃无权限访问的报错。

不找不知道，一找吓一跳，居然放在/var/www下面？？？

我服了。以后也要注意一下/var目录才可以，真是浪费我时间...也怪我自己蠢，sudo提权这个在ctf本来就很少见说是...

