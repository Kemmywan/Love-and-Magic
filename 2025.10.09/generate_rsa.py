# import sys
# print(sys.executable) //用于查看当前python解释器路径


p = 473398607161
q = 4511491
e = 17

phi_n = (p - 1) * (q - 1)

d = pow(e, -1, phi_n)

print(d)