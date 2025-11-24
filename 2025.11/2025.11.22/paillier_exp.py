from pwn import *
import math
from Crypto.Util.number import getStrongPrime, long_to_bytes, bytes_to_long

p = remote("127.0.0.1", 61234)

n = int(p.recvline().decode().split()[2].strip())

# print(f"received n={n}")

flag_enc = int(p.recvline().decode().split()[5].strip())

# Z	90	0x5A
# J	74	0x4A
# U	85	0x55
# C	67	0x43
# T	84	0x54
# F	70	0x46
# {	123	0x7B
# }	125	0x7D

# length = 39
# temp = pow(flag_enc, 256, n**2) * pow(n + 1, 125, n**2)

# while True:
#     p.recvuntil(b"Show me how skilled you are at additive homomorphism: ")
#     p.sendline(b"BEGGING FOR FLAG")
#     p.recvuntil(b"Parameters: ")
#     temp_str = b"ZJUCTF{" + b"\x00" * (length + 1)
#     temp_n = temp * pow(n + 1, bytes_to_long(temp_str), n**2)
#     p.sendline(str(flag_enc).encode() + b"," + str(temp_n).encode())
#     res = p.recvline()
#     if b"bro" in res:
#         break
#     else:
#         length += 1
    
#     print(length)
#     print(temp_str)

# print(f"length of flag is {length}")

# length = 39

# offset_str = b"ZJUCTF{" + b"\x00" * (length + 1)

ans = bytes_to_long(b'ZJUCTF{\x03A\x07F\x0f\xbdV\x9b$g\xa0\xa3"\xf6\x03&\xc4\x89RB\xc1\xcbvz\x93\xc4\xb26\xa0\xfe\x97W99\xb0<\x01T\xd6\x14')

# ans = bytes_to_long(b"ZJUCTF{" + b"\x00"*39 + b"}")

# ans = 0

i = 1674

for _ in range(250):
    while True:
        temp = flag_enc * pow(n + 1, n - ans, n ** 2)
        temp = pow(temp, 2**i, n**2)

        # Cal the length
        temp_s = pow(temp, 256, n**2) * pow(n + 1, 125, n**2)
        # length = int(math.log(n, 256)) + 2 # Can start from here max 248?
        length = 100

        while True:
            p.recvuntil(b"Show me how skilled you are at additive homomorphism: ")
            p.sendline(b"BEGGING FOR FLAG")
            p.recvuntil(b"Parameters: ")
            temp_str = b"ZJUCTF{" + b"\x00" * (length + 1)
            temp_n = temp_s * pow(n + 1, bytes_to_long(temp_str), n**2)
            p.sendline(str(temp).encode() + b"," + str(temp_n).encode())
            res = p.recvline()
            if bytes_to_long(temp_str) > n:
                break
            if b"bro" in res:
                break
            else:
                length += 1

            print(length)

        print(f"length of temp is {length}")


        # p.recvuntil(b"Show me how skilled you are at additive homomorphism: ")
        # p.sendline(b"BEGGING FOR FLAG")
        # p.recvuntil(b"Parameters: ")

        # p.sendline(str(temp).encode() + b"," + str(pow(temp, 256, n**2) * pow(n + 1, 125, n**2) * pow(n + 1, bytes_to_long(offset_str), n**2)).encode())

        # res = p.recvline()

        print(i, res)

        if b"bro" not in res:
            if bytes_to_long(temp_str) > n:
                ans += (n - 125) // (256 ** 7) // (2**i)
            else:
                ans += (n - 125 - pow(bytes_to_long(temp_str), 1, n)) // 256 // (2**i)
            print(long_to_bytes(ans))
            break
        
        i += 1

