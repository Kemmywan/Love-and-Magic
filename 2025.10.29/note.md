当前进度：

5/104-1/13

buuoj

## [GXYCTF2019]BabySQli

随便输入一个账户密码，在源代码处找到下面这一串提示：

MMZFM422K5HDASKDN5TVU3SKOZRFGQRRMMZFM6KJJBSG6WSYJJWESSCWPJNFQSTVLFLTC3CJIQYGOSTZKJ2VSVZRNRFHOPJ5

仅有大写字母和数字->base32，解码得到：

c2VsZWN0ICogZnJvbSB1c2VyIHdoZXJlIHVzZXJuYW1lID0gJyRuYW1lJw==

这个是base64，解码得到：

select * from user where username = '$name'%

直接提示了我们拼接查询语句的具体方法，真是大善人（）

万能密码被过滤，试了一下发现是or被过滤了，

然后试一下union，可以联合查询

那么先试字段数，试到union select 1,2,3#不报错，那么看来字段数就是3

根据经验猜测估计是id,admin,password，

id猜1，admin试出来是'admin'，那么剩下的就是password，因为最后也只是验证password。

那么我们可以利用select的特性来伪造所获得的数据，像这样：

```
username=1' union select 1,'admin','123'#
password=123
```

理想中的情况就会成功，但是还是回显密码错误，那么看来内部的密码可能使用了md5加密来存储，这也很简单，用自带的md5sum加密一下123即得到最终payload:

```
username=1' union select 1,'admin','202cb962ac59075b964b07152d234b70'#
password=123
```

得到flag

## [GYCTF2020]Blacklist

参考2025.09.26/note.md里的随便注那道题，感觉基本上是从那个改过来的。

得到的过滤有：

set|prepare|alter|rename|select|update|delete|drop|insert|where

不过这次rename被ban掉了，老样子用show 命令可以爆表名和列名等等，但是关键怎么把FlagHere里的flag取出来。

又学到新东西：handler命令，也是一个很强力的查询命令：

- handler命令查询规则

    handler table_name open;handler table_name read first;handler table_name close;
    handler table_name open;handler table_name read next;handler table_name close;

- 用法

    首先打开数据库，开始读它第一行数据，读取成功后进行关闭操作。
    首先打开数据库，开始循环读取，读取成功后进行关闭操作。

那么我们的payload非常简单：

```
?inject=1%27%3Bhandler+FlagHere+open%3Bhandler+FlagHere+read+first%3Bhandler+FlagHere+close%23
```

就可以查到payload。

（看来之前那道随便注也可以用这种方法！）

## [RoarCTF 2019]Easy Java

登录无果，结合标题猜应该是要利用java模板的漏洞，

点击help，回显奇怪的页面：

java.io.FileNotFoundException:{help.docx}

看来FileName参数被载入java模板中进行了一个文件查询并尝试下载，但是为什么没能下载成功呢？

（结果原来是不知道怎的换成POST传入就可以了

总之下载了help.docx，但里面只有作者无情的嘲讽，

只好去找wp：

学新东西啦！

（详细的关于web源码的泄漏利用在下面这篇文章里可以找到

https://blog.csdn.net/wy_97/article/details/78165051

这里我们用到web-xml漏洞：

WEB-INF是Java的WEB应用的安全目录。如果想在页面中直接访问其中的文件，必须通过web.xml文件对要访问的文件进行相应映射才能访问。WEB-INF主要包含一下文件或目录：

- /WEB-INF/web.xml：Web应用程序配置文件，描述了 servlet 和其他的应用组件配置及命名规则。

- /WEB-INF/classes/：含了站点所有用的 class 文件，包括 servlet class 和非servlet class，他们不能包含在 .jar文件中

- /WEB-INF/lib/：存放web应用需要的各种JAR文件，放置仅在这个应用中要求使用的jar文件,如数据库驱动jar文件

- /WEB-INF/src/：源码目录，按照包名结构放置各个java文件。

- /WEB-INF/database.properties：数据库配置文件

漏洞成因：通常一些web应用我们会使用多个web服务器搭配使用，解决其中的一个web服务器的性能缺陷以及做均衡负载的优点和完成一些分层结构的安全策略等。在使用这种架构的时候，由于对静态资源的目录或文件的映射配置不当，可能会引发一些的安全问题，导致web.xml等文件能够被读取。漏洞检测以及利用方法：通过找到web.xml文件，推断class文件的路径，最后直接class文件，在通过反编译class文件，得到网站源码。一般情况，jsp引擎默认都是禁止访问WEB-INF目录的，Nginx 配合Tomcat做均衡负载或集群等情况时，问题原因其实很简单，Nginx不会去考虑配置其他类型引擎（Nginx不是jsp引擎）导致的安全问题而引入到自身的安全规范中来（这样耦合性太高了），修改Nginx配置文件禁止访问WEB-INF目录就好了： location ~ ^/WEB-INF/* { deny all; } 或者return 404; 或者其他！

因为这个漏洞给了我们任意文件的下载权限，那么先把web.xml下载下来看看，放在日期目录下面了。

然后去找与Flag有关的那个class，下载下来：

```
filename=/WEB-INF/classes/com/wm/ctf/FlagController.class
```

下载得到的.class文件要进行一步反编译，我们使用brew管理下的cfr-compiler工具即可对其反编译：

cfr-decompiler _WEB-INF_classes_com_wm_ctf_FlagController.class > flagcontroller.txt 

在导出的.txt文件中可以看到一串base64编码，解码即得到flag!

进度：

8/104-2/13





