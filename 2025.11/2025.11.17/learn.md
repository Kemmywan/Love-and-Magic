# 偷师ing...

看一下大佬的2025-0ops-ctf的wp：https://shuiyuan.sjtu.edu.cn/t/topic/365479/5

## Welcome3

sha-256哈希先猜后证

## ezCrypt

传统加密套娃，用cyberch做菜谱（大佬锐评

R3VyIHN5bnQgdmYgMHd4eXsxPW54cl9zeUBUX2JTX1BFbENHQl9QdW4xMSF9ISBWJ3ogeHZxcXZhdC4gTmNldnkgU2JieSEgR3VyZXIgdmYgYWIgc3ludCB2YSBndXZmIGJhcn4gT2hnIFYgcG5hIGNlYml2cXIgbGJoIGZienIgdXZhZyBzYmUgZ3VyIGJndXJlIG95YnB4IQogWm5sb3IgdmcgdmYgbiBwYnpjbnBnIGVyY2VyZnJhZ25ndmJhIGJzIFZDaTYgbnFxZXJmZnJmLCBuZyB5cm5mZyBucHBiZXF2YXQgZ2IgZmJ6ciBzaGFhbCBFU1BmIFYgZXJucSBybmV5dnJlLiBOc2dyZSBndW5nLCBsYmggenZ0dWcgam5hZyBnYiB5cm5lYSBub2JoZyBFRk4sIG5hcSBndXIgcmtnZXJ6ciBxdnNzdnBoeWdsIGdiIHNucGdiZSB1aHRyIGFoem9yZWYsIHJmY3Jwdm55eWwganVyYSBndXJsIG5lciBndXIgY2VicWhwZyBicyBnamIgeW5ldHIgY2V2enJmLCBoYXlyZmYgZmJ6cmJhciB1bnEgY2hveXZmdXJxIGd1ciBlcmZoeWcgYnMgZ3VyIHNucGdiZXZtbmd2YmEuIFRiYnEgeWhweCE=

NhfU}b8jGXZ*p>ZEFeiBW^Zz5Z*(AZZy<AFc4Z)RXk{R9a%py9bY&oGWqBZUZy;o4V{c?-AarPDAZBb~XD%Q@b#x$eZ*65Db9HcKa$|38aCLNLav*47c4Z)8Y;t8`WO*QCa$#d@Wn>^}bRc1FWFU2LY;R#?Wn>_9Zy;fAAa8DLX>Mg8WMVELLt$<pd2e+fW@&C@AarPDAZBb~XFm!GZXi7%FnBjNF=942WMySxH)S$qV`MO9VKFr@IXPivIWRaiWieqkVlg%|V>B@}Vq|4CHe)t1Wn(xoF)}bQWHmBnG&MG5G+{V5He_NpWMMa9W->N8HDxj|He@+vGh#9`WMwciVKFvlHa9h4WH2~4V>DuAW;0=9V>V+nWid8kVlxV5AUz;9H8nFg3S%HWATW3}HZ(D0IASn0W@KS9IAb|sW-~Q4VKg{6Vq!LAIX7fEW@R!lWnnfnHDY5jH8?ReWMVThH)b$2W?^ACG+{PoWH~ctVKX>0GdVUjGBai{H85g1HaKN5IX7lFIc8;IVPrToFg7tXI5aS2WnyGDH#K21W;ro8Gcq)0Ib<*j

Maybe it is a compact representation of IPv6 addresses, at least according to some funny RFCs I read earlier. After that, you might want to learn about RSA, and the extreme difficulty to factor huge numbers, especially when they are the product of two large primes, unless someone had published the result of the factorization. Good luck!

I'm so sorry, I forgot to save the private key to decode the flag. But some supercomputer have already cracked it and uploaded to an online db. Can you find the flag?

n = 0x771b68deea7e2ecd0fa15099ae9085e1a6b163c415bde56c61ec811201d52e456e4a876db6da7af2695e206d9e3b23de02a16f675ad087c4bef3acc6c4e16ab3
e = 65537
c = 0x5641d8b05fda28c9af355a488bb6d97d9fe21ea645bc25814db317f04faa84a6fd93fa383396523f050b968e197f89febad840614840eebd675a3f917324f9d0

p = 66720953144911165998838491049270049821121906475512246576323412599571011308613
q = 93496017058652140120451192281187268387402942550918512435321834788719825835671

cyberchef的magic使用：

现在作为一个module，拖到recipe上，选择depth是探索可能的深度（steps）

然后可以看到可能的输出以及对应的recipe，右侧有一个entropy，越小代表可读性越高，可能已经是可读文本

用Tail模块可以分隔文本的不同段落，来构成完整的recipe（elegant

有的时候magic不会直接给recipe：

- 会给提示，自行使用相应的module
- 可能还缺一步rot，这个可以手动来操作

用python的int函数可以简单的转进制：

n = "0x771b68deea7e2ecd0fa15099ae9085e1a6b163c415bde56c61ec811201d52e456e4a876db6da7af2695e206d9e3b23de02a16f675ad087c4bef3acc6c4e16ab3"
n_d = int(n, 16) // int(:string, :int)

使用pow可以直接做rsa求解：

d = pow(e, -1, (p-1)*(q-1))
m = pow(c, d, n)

p,q涉及大素数分解问题，用这个网站查询：

https://factordb.com/

（似乎要挂梯子）

用python简单的转bytes：（很万用）

print(m.to_bytes(114).lstrip(b'\0'))

把整数 m 按114字节转bytes，去掉前面的所有0字节，然后打印出结果。

114是随便取的，这里相当于每两位转成ascii字符(前提是在ascii可见范围)

真是学到不少实用的东西

## Notes

http://7b93rfbx2rr6kwtf.instance.penguin.0ops.sjtu.cn:18080/note?token=dG9tbzAuR08.YWE1OTViMjAxYjkyZmFmZmM2NzE2OGYyNjQ0N2I5MTBmMDM1YjBlMTM3NjU3YjQ0ZWE2MTFlMzE2NWI5N2U5NA

http://7b93rfbx2rr6kwtf.instance.penguin.0ops.sjtu.cn:18080/note?token=dG9tbzAuR08.NTQyMjcxOTEyNGNiZTYxNDljNWFjMTIwMzJjNTBjN2I1OTg4MjFiODE5YjkwYzRiYzlkNzE0Y2QzYzc2Y2M4Yw

用ai帮我看一下源码：

难点在于每10秒随机生成的secret，会被用于和org生成sm3散列（中国国家密码标准），后者安全性与sha-256相当，

竞速思路！输入默认的账号密码可以在url处得到token，用ai写反解源码，把org改成crycry再得到token去验证，这个就看速度了。

## AnatahEtodokuSakebi

时间戳被拼接成字符串，拼接后其长度为文本长度（通常10位，如1763377800）

str(int(timestamp // 600 * 600))

