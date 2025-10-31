## Riddle Registry

下载得到一个pdf，blabla说一大堆。

可以直接复制粘贴出来看一下涂黑的部分是什么，从前到后分别是：

Aenean lacinia bibendum nulla sed consectetur

Lorem ipsum dolor sit amet

The author have done a great and good job

No flag here. Nice try though!

前两条看起来是随便生成的，后两条是无情嘲讽（笑）

提示2：Look beyond the surface for hidden clues

把前面一段文本粘贴给cpt，告诉我这是一段用于展示排版效果的拉丁文，看起来是真的没有什么用...

```
唉，假文内容用于排版测试，与实际内容无关。这段“Lorem Ipsum”是常用的拉丁文填充文本，实际没有特定意思，只是用于展示字体和版面效果。如果你需要正式翻译，请提供真实内容。如果你只是想了解它的形式意义，通常可以译为：

“这是一些用于展示排版效果的虚拟文本。它没有实际含义，只是用来填充页面，便于查看字体和布局。”
```

可是为什么要涂黑呢？百思不得其解。

看来我们只能启动我们的010editor，发现author项是一段很像base64编码的字符串：

cGljb0NURntwdXp6bDNkX20zdGFkYXRhX2YwdW5kIV9lZTQ1NDk1MH0

解码为：

picoCTF{puzzl3d_m3tadata_f0und!_ee454950}

好吧原来作者没有骗我，真的和文本内容没有关系...

PS:看来要注意这段开头的base64编码了，后面可能还会出现

## Corrupted file

给了我们一个损坏的文件，那常规方法自然是打不开的。

我们用010editor打开，先看前八位的hex：

5c 78 ff e0

cpt告诉我这不是常见的文件格式应有的文件头，但是有一个很相近的格式叫jpeg图片，它的文件头是：

ff d8 ff e0

我们手动把这个文件头修改过来，然后用图片查看器打开它，就得到了flag。

## Hidden in plainsight

下载img.jpg，提示我们查看metadata，我们用kali上的exiftool来处理它，命令是：

```
exiftool 文件名.jpg //查看元数据
exiftool -DateTimeOriginal 文件名.jpg //查看特定字段
exiftool *.jpg //批量查看多个文件
exiftool -Artist="YourName" 文件名.jpg //修改元数据
```

直接查看，发现一行Comment：

c3RlZ2hpZGU6Y0VGNmVuZHZjbVE9

Base64解码：

steghide:cEF6endvcmM=

继续把后面解码：

steghide:pAzzword

看来是提示我们要用steghide来解密，并给出了加密的密码。

用stegihde解密：

```
steghide extract -sf img.jpg -p pAzzword
```

解密出文件flag.txt，成功！

## Flah in Flame

提示用base64解码logs.txt，用cyberchef很方便！

地址：https://gchq.github.io/CyberChef/

解码之后是png图片格式（cyberchef神力）

然后把里面的数字串再用hex解密即可！

