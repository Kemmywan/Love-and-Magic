d = "afZ_r9VYfScOeO_UL^RWUc"

e = ""

for i in range(len(d)):
    e += chr(ord(d[i]) + i + 5)

print(e)