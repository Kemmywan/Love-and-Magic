# bbabla

讲到更实战的情形：bypass-method

最常见的defense就是把你的一些字符直接滤掉，比如空格：


```php
<?php
    $conn = mysqli_connect("localhost","root","kali","test");
    $id = $_GET['id'];
    echo "before replace: id:$id";
    $id = str_replace(" ","",$id);
    echo "<br>after replace: id:$id<br>";
    $sql = "SELECT title, content FROM wp_news WHERE id=".$id;
    
    $res = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($res);

    echo "<center>";
    echo "<h1>".$row['title']."</h1>";
    echo "<br>";
    echo "<h1>".$row['content']."</h1>";
    echo "</center>";
?>
```

其中str_replace把空格缩进，因此不能直接使用空格。

before replace: id:-1 union select 1,2
after replace: id:-1unionselect1,2

如果是这样简答的filter我们有许多方法可以绕过，
url-encoded下%0a,%09等等都可以替换空格而不被filter。

%09（Tab）、%0a（换行）、%0b（垂直制表）、%0c（换页）、%0d（回车）

id=-1%09union%09select%091,2

before replace: id:-1 union select 1,2
after replace: id:-1 union select 1,2

而在sql语法层面可以替代“空格”的关键字还有注释符：/**/，这个注释符也可以用来拆分关键字！比如SEL/**/ECT。

这就谈到另一种情况：用简单的str_replace来处理SELECT这样的关键字时，可以用上面说到的注释符，也可以写成：

SELSELECTECT

这样在strreplace成空字符之后就变回SELECT~(小巧思)

另外，sql的关键字是大小写不敏感的，也就是完全可以写成SelECt

如果是用正则表达式\bselect\b来精确匹配的话，用/*!50000select*/就可以绕过，其中/*!*/会条件判别mysql版本高于5.0.0时识别为select，而select和50000并列所以不会被正则匹配找到。

也有这样一种情况，那就是在WHERE条件下出现了AND从句，比如：

```php
$sql = "SELECT * FROM wp_news WHERE id = 'con1' AND title = 'con2'"
```

要同时针对这两个注入点来设计程序，可以这样子做：

```php
$sql = "SELECT * FROM wp_news WHERE id = 'a\' AND title = 'OR sleep(1)#'"
```

```sql
select * from wp_news where id='a\' AND title = ' union select * from wp_user#'
```

利用转义字符backslash\来将第一个单引号（quote）给绕过，这样'a\' AND title = '会被视为一个完整的字符串与id进行对照。也就意味着我们在title处可以执行任意我们想执行的语句了。

在mariadb中backslash-escape似乎默认不可用，测试环境下我们可以直接把sql_mode清空就可以正常使用backslash的转义功能了：

```sql
SET SESSION sql_mode='';
```

# File Read Vulnerability

Linux服务器的一些常用的路径文件等：

- /etc 各种系统认证文件

- /etc/passwd 所有用户可读，记录系统的所有用户账号信息，格式如下：

`用户名:密码占位符:用户ID:组ID:用户描述:家目录:登录shell`

如：

```
root:x:0:0:root:/root:/usr/bin/zsh
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
```

1. **用户名**  
   系统登录名，比如 `root`、`user1`。

2. **密码占位符**  
   早期直接存密码（明文或加密），现在一般为 `x`，实际密码存于 `/etc/shadow`。

3. **用户ID（UID）**  
   `0` 为超级用户，其它为普通用户。系统用户一般为1~999，普通用户从1000开始。

4. **组ID（GID）**  
   用户所属主组的编号。

5. **用户描述（注释）**  
   一些说明性文字，如用户名/描述。

6. **家目录**  
   用户登录后所在的主目录，例如 `/home/user1`、`/root`。

7. **登录Shell**  
   用户登录后默认使用的Shell，比如 `/bin/bash`，`/usr/sbin/nologin`（禁止登录用）。

- /etc/shadow 仅root可读，存储所有密码(的哈希值)

- /etc/apache2/* Apache配置

- /etc/nginx/* Nginx配置

- /etc/apparmor(.d)/*

- /etc/(cron.d/*|crontab)

- /etc/environment

- /etc/hostname

- /etc/hosts

- /etc/issue

- /etc/php

- /proc 管理当前进程

/proc/[pid]/* 指向该进程的各种信息（*=cmdline/cwd/environ/...）







