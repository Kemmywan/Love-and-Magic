import hashlib

s = "101999966233"

md5_hash = hashlib.md5(s.encode('utf-8'))

print(md5_hash.hexdigest())

