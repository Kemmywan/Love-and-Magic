# 做一下ssrf的题目

## [De1CTF 2019]SSRF Me

#! /usr/bin/env python #encoding=utf-8 from flask import Flask from flask import request import socket import hashlib import urllib import sys import os import json reload(sys) sys.setdefaultencoding('latin1') app = Flask(__name__) secert_key = os.urandom(16) class Task: def __init__(self, action, param, sign, ip): self.action = action self.param = param self.sign = sign self.sandbox = md5(ip) if(not os.path.exists(self.sandbox)): #SandBox For Remote_Addr os.mkdir(self.sandbox) def Exec(self): result = {} result['code'] = 500 if (self.checkSign()): if "scan" in self.action: tmpfile = open("./%s/result.txt" % self.sandbox, 'w') resp = scan(self.param) if (resp == "Connection Timeout"): result['data'] = resp else: print resp tmpfile.write(resp) tmpfile.close() result['code'] = 200 if "read" in self.action: f = open("./%s/result.txt" % self.sandbox, 'r') result['code'] = 200 result['data'] = f.read() if result['code'] == 500: result['data'] = "Action Error" else: result['code'] = 500 result['msg'] = "Sign Error" return result def checkSign(self): if (getSign(self.action, self.param) == self.sign): return True else: return False #generate Sign For Action Scan. @app.route("/geneSign", methods=['GET', 'POST']) def geneSign(): param = urllib.unquote(request.args.get("param", "")) action = "scan" return getSign(action, param) @app.route('/De1ta',methods=['GET','POST']) def challenge(): action = urllib.unquote(request.cookies.get("action")) param = urllib.unquote(request.args.get("param", "")) sign = urllib.unquote(request.cookies.get("sign")) ip = request.remote_addr if(waf(param)): return "No Hacker!!!!" task = Task(action, param, sign, ip) return json.dumps(task.Exec()) @app.route('/') def index(): return open("code.txt","r").read() def scan(param): socket.setdefaulttimeout(1) try: return urllib.urlopen(param).read()[:50] except: return "Connection Timeout" def getSign(action, param): return hashlib.md5(secert_key + param + action).hexdigest() def md5(content): return hashlib.md5(content).hexdigest() def waf(param): check=param.strip().lower() if check.startswith("gopher") or check.startswith("file"): return True else: return False if __name__ == '__main__': app.debug = False app.run(host='0.0.0.0',port=80

启动实例之后得到这一大段代码，放到vs里用ai格式化一下，整理在了./ssrfme.py

提示告诉了我们flag存放在flag.txt，但是两个路由/geneSign和/De1ta并没有可以直接访问到flag.txt的方法。

我们要面对的防御措施包括在waf阶段的"gopher"和"file"协议的关键字筛查，还包括一道数字签名

观察Task实例的代码，可以看到两种actions包括scan和read，特点是scan能够读取内容放置于基于Ip的地址而read是把这个地址里的result读取出来，不过由于作者直接用"in"来判别，我们只需让action="readscan"或者"scanread"就可以，

剩下的就是绕过签名，签名由action和param来生成，我们的action应当包含read和scan，而param应该是flag.txt，而在geneSign路由中action默认是scan，

所以我们先通过geneSign路由导入param="flag.txtread"这样得到的签名就是"flag.txtreadscan"，而后续使用cookies导入action和sign只需要：

action="readscan"
param="flag.txt"

就可以了，编写脚本（exp_ssrfme.py）即得到flag！

这道题主要考察的是初级的waf绕过！