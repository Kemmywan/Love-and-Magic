刷题刷题go

buuoj

## [极客大挑战 2019]BuyFlag

打开实例，点击右上角的菜单MENU，有一项PAY THE PASSWORD

点进去显示要我们花天文数字购买flag（当然是假的

F12看源代码，发现一行注释掉的hint：

```php
	~~~post money and password~~~
    if (isset($_POST['password'])) {
        $password = $_POST['password'];
        if (is_numeric($password)) {
            echo "password can't be number</br>";
        }elseif ($password == 404) {
            echo "Password Right!</br>";
        }
    }
```

需要我们post两参数money和password，其中money看起来是没有任何要求，关键就在于这个password，要求不能是数字，但又要等于404

> 关于is_numeric():
> is_numeric()是php中用于识别数的函数，其识别范围是整数/浮点数、带符号的数字和科学计数法等，其一大特点是如果传入的是数字那么0x194和0b101等会直接被识别为数字，而如果传入的是""字符串，则不会将"0x194"识别成数字
>
> 123 -> true
> 0x1a -> true
> "0x1a" -> false
> 0b1010 -> true
> "0b1010" -> false
> "0755" -> true
> "2e3" -> true
> "123" -> true
> "+123" -> true
> "1.23" -> true

也就是我们可以利用弱等号来绕过！

> 在php中比较数字和字符串时，会试图将字符串（按十进制）转换成数再比较，至于转换的方式也很粗暴，就是直接取字符串前最长的数字序列组成一个数，比如"404abc"就会被转换成404

用hackbar传入两个参数：money=100000000&password=404a

返回处显示我不是一个Cuiter（是哪个大学的名字吗？

关于身份识别，最简单的是关注请求所带的cookie，注意到我们默认user=0，改成1试试，果然成功通过，这次返回：

you are Cuiter
Password Right!
Nember lenth is too long

说我们输入的长度太长了！也不知道是说money还是password，应该是money，因为money有足足九位。

有可能Money随便填一个就可以？money=1000试试：

you have not enough money,loser

好吧看来还是要一亿，想必是有一个Money和1e8的比较，

唉等等，我刚刚是不是说了1e8？对啊，可以用科学计数法！

试试money=1e8，不行，再试money=1e9，pass！

得到flag{b5f3e62a-50b2-4662-8ef0-6190ce7a27cc}

PS:这道题有关php中对于数字的绕过处理！



