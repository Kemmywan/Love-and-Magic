from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# 加载私钥
with open('private_key.pem', 'rb') as f:
    key = RSA.import_key(f.read())

# 读入密文（按二进制读取，最安全）
with open('flag.enc', 'rb') as f:
    cipher_bytes = f.read()

# 解密
decryptor = PKCS1_OAEP.new(key)
plaintext = decryptor.decrypt(cipher_bytes)

print(plaintext.decode(errors='ignore'))  # flag如果是ascii/utf-8可直接输出