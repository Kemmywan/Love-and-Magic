前面三天在赶nis3316的pre和os的lab1，真是绕了好大一圈啊...

课上一边听pre一边刷刷crypto和misc好了

buuoj.cn

## 权限获得第一步

Administrator:500:806EDC27AA52E314AAD3B435B51404EE:F4AD50F57683D4260DFD48AA351A17A8:::

是windows老系统的pwd密文，前面是LM，后面是NTLM

温习一下hashcat的使用，在mac上也配置了一下：

常见的 Windows 哈希类型：
1000 = NTLM
3000 = LM

hashcat -m 1000 hash.txt rockyou.txt

用指定字典进行NTLM的破解

攻击优先级:

    LM优先: 如果存在LM哈希，优先攻击
    NTLM次之: 使用字典+规则攻击
    组合信息: LM破解结果可以帮助NTLM破解

(base) kemmywan@KemmywandeMacBook-Air 2025.11.4 % hashcat -m 3000 -a 3 hash.txt '?a?a?a?a?a?a?a'

进行7位枚举破解，没想到正好是7位（看来7位是什么默认的长度对于这类题目来说

（?a匹配任意ascii可见字符）

(base) kemmywan@KemmywandeMacBook-Air 2025.11.4 % hashcat -m 3000 -a 3 hash.txt --show          
806edc27aa52e314aad3b435b51404ee:3617656

得到密码3617656

## RSA1

与给出私钥d相比，题目里除了p, q, c之外给出的额外参数是dp, dq

这并不是d和p的乘积，而是RSA的CRT简化参数：

dp = d mod (p-1)（因为有fermat所以直接mod (p-1)来减小数字）

```py
# 使用 CRT 参数加速解密
mp = pow(c, dp, p)  # 在模 p 下解密
mq = pow(c, dq, q)  # 在模 q 下解密

# 使用中国剩余定理合并结果
m = (mp * q * qinv + mq * p * pinv) mod n
```

因为 m ≡ c^d (mod n)，所以实质上是一个中国剩余定理的拆分，其中qinv和pinv分别是q模p的逆和p模q的逆

那么我们的解码脚本就可以简化成上面的样子

最后得到的raw_number一般可以试着转化成hex编码：

```py
print(f"The text message is: {bytes.fromhex(hex(m)[2:])}")
```

得到flag把noxCTF换成flag就行（这里还要坑我一下

## 传统知识+古典密码

六十花甲子：

01.甲子
	
02.乙丑
	
03.丙寅
	
04.丁卯
	
05.戊辰
	
06.己巳
	
07.庚午
	
08.辛未
	
09.壬申
	
10.癸酉
11.甲戌
	
12.乙亥
	
13.丙子
	
14.丁丑
	
15.戊寅
	
16.己卯
	
17.庚辰
	
18.辛巳
	
19.壬午
	
20.癸未
21.甲申
	
22.乙酉
	
23.丙戌
	
24.丁亥
	
25.戊子
	
26.己丑
	
27.庚寅
	
28.辛卯
	
29.壬辰
	
30.癸巳
31.甲午
	
32.乙未
	
33.丙申
	
34.丁酉
	
35.戊戌
	
36.己亥
	
37.庚子
	
38.辛丑
	
39.壬寅
	
40.癸卯
41.甲辰
	
42.乙巳
	
43.丙午
	
44.丁未
	
45.戊申
	
46.己酉
	
47.庚戌
	
48.辛亥
	
49.壬子
	
50.癸丑
51.甲寅
	
52.乙卯
	
53.丙辰
	
54.丁巳
	
55.戊午
	
56.己未
	
57.庚申
	
58.辛酉
	
59.壬戌
	
60.癸亥

我们的内容： 

辛卯，癸巳，丙戌，辛未，庚辰，癸酉，己卯，癸巳。

信的背面还写有“+甲子”，请解出这段密文。

对应：

28, 30, 23, 8, 17, 10, 16, 30

+60（一甲子称为60年！）

对应的应该是ascii:

88， 90， 83， 68， 77， 70， 76， 90

XZSDMFLZ

wp告诉我这里要用栅栏解密！虽然完全看不出来...

1. 基本原理

栅栏加密是一种置换密码，通过将明文按照锯齿状（栅栏状）排列，然后按行读取来实现加密。
核心思想

    将明文字符按照"之"字形路径排列在多行上
    按行顺序读取得到密文

2. 加密过程演示
示例：3层栅栏加密 "HELLO WORLD"
步骤1：去除空格（可选）
Code

明文: HELLOWORLD

步骤2：按栅栏排列（3层）
Code

行号  字符排列
1     H   L   W   L
2      E L O O R D
3       L   O   O

步骤3：可视化栅栏路径
Code

H . . . L . . . W . . . L
. E . L . O . O . R . D .
. . L . . . O . . . O . .

步骤4：按行读取
Code

第1行: HLWL
第2行: ELOORD  
第3行: LOO

密文: HLWLELOORDLOO

实质上就是先分组再重新排列

这里我们的XZSDMFLZ:

二栏：

两组：xzsd, mflz

解密：xmzfsldz

四栏：

四组：xz, sd, mf, lz

解密；xsmlzdfz

没有明显含义，放到ROT里面转转：

发现：

xmzfsldz + 21 = shuangyu

看来这个就是flag了

----

有一个想法就是可以后面用py脚本来solve（打字好累）





