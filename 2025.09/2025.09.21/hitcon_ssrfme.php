192.168.122.15 
<?php
    if (isset($_SERVER['HTTP_X_FORWARDED_FOR'])) {
        $http_x_headers = explode(',', $_SERVER['HTTP_X_FORWARDED_FOR']);
        $_SERVER['REMOTE_ADDR'] = $http_x_headers[0];
    }
    // 如果有代理就获取其x_forwarded_for的第一个ip，否则获取headers中的ip，这样是为了获取发起请求的真实服务器Ip
    echo $_SERVER["REMOTE_ADDR"];

    $sandbox = "sandbox/" . md5("orange" . $_SERVER["REMOTE_ADDR"]); // 加盐ip生成沙箱
    @mkdir($sandbox); // 在 PHP 中，函数或表达式前面加上 @ 符号，表示抑制该语句可能产生的错误或警告信息，让这些错误不会输出到页面或日志。
    @chdir($sandbox); // 创建并切换

    $data = shell_exec("GET " . escapeshellarg($_GET["url"])); // Copilot said: `escapeshellarg()` 是 PHP 中的一个函数，用于将字符串安全地转义为可以用于 shell 命令的参数。它会在参数两边加上单引号，并且正确地转义字符串中的单引号和特殊字符，从而防止命令注入攻击。
    // $data是执行这一命令所得的结果，随后被写入我们指定的文件中
    // GET是Lib for WWW in Perl中的命令,目的是模拟http的GET请求,GET函数底层就是调用了open处理,open存在命令执行，并且还支持file函数
    $info = pathinfo($_GET["filename"]); // 解析filename
    $dir  = str_replace(".", "", basename($info["dirname"])); // 去.防止目录穿越
    @mkdir($dir);
    @chdir($dir);
    @file_put_contents(basename($info["basename"]), $data);
    highlight_file(__FILE__);