<?php 
highlight_file(__FILE__);
function check_inner_ip($url) 
{ 
    $match_result=preg_match('/^(http|https)?:\/\/.*(\/)?.*$/',$url); //只要以http://或https://开头就可以
    if (!$match_result) 
    { 
        die('url fomat error'); 
    } 
    try 
    { 
        $url_parse=parse_url($url); 
    } 
    catch(Exception $e) 
    { 
        die('url fomat error'); 
        return false; 
    } 
    $hostname=$url_parse['host']; //利用url_parse来检测是否为内网ip
    $ip=gethostbyname($hostname); // DNS -> IP
    $int_ip=ip2long($ip); 
    return ip2long('127.0.0.0')>>24 == $int_ip>>24 || ip2long('10.0.0.0')>>24 == $int_ip>>24 || ip2long('172.16.0.0')>>20 == $int_ip>>20 || ip2long('192.168.0.0')>>16 == $int_ip>>16; 
    /**
     * 防止以下内网网段
     * 127.0.0.0/8 本地回环
     * 10.0.0.0/8 A类私有地址
     * 172.16.0.0/12 B类私有地址
     * 192.168.0.0/16 C类私有地址
     */
} 

function safe_request_url($url) 
{ 
     
    if (check_inner_ip($url)) 
    { 
        echo $url.' is inner ip'; 
    } 
    else 
    {
        $ch = curl_init(); 
        curl_setopt($ch, CURLOPT_URL, $url); 
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); 
        curl_setopt($ch, CURLOPT_HEADER, 0); 
        $output = curl_exec($ch); 
        $result_info = curl_getinfo($ch); //curl请求
        if ($result_info['redirect_url']) 
        { 
            safe_request_url($result_info['redirect_url']); //重定向则递归调用
        } 
        curl_close($ch); 
        var_dump($output); 
    } 
     
} 

$url = $_GET['url']; 
if(!empty($url)){ 
    safe_request_url($url); 
} 

?> 