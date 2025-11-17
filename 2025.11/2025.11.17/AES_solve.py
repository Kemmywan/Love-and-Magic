import requests
import time
from Crypto.Cipher import AES
from hashlib import md5

KEY = b"UZhyYC6oiNH2IDZE"
IV = b"sjtuctf20250oops"
BLOC = 16

def pad_pkcs7(data: bytes) -> bytes:
    pad = BLOC - (len(data) % BLOC)
    return data + bytes([pad]) * pad

def aes_cbc_encrypt(msg: bytes):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    return cipher.encrypt(msg)

def build_ciphertext(msg: str):
    # 还原service端的decrypt流程的逆过程
    m = msg.encode()
    pad = 0
    if len(m) % BLOC > 0:
        pad = BLOC - (len(m) % BLOC)
        m = pad_pkcs7(m)
    enc = aes_cbc_encrypt(m)
    data = bytearray(enc)
    if pad != 0:
        # 服务端混淆逆思路
        # 把最后一块和倒数第二块对调
        last_block = data[-BLOC:]
        second_to_last_block = data[-2*BLOC:-BLOC]
        rest = data[:-2*BLOC]
        # 创建ECB加密
        ecb = AES.new(KEY, AES.MODE_ECB)
        ecb_enc = ecb.encrypt(bytes(last_block))
        new_pad_part = ecb_enc[-pad:]
        # 补到倒数第二块末尾
        new_second_to_last_block = second_to_last_block + new_pad_part
        new_data = rest + new_second_to_last_block + last_block
        return new_data.hex()
    else:
        return data.hex()

def find_pow(data, timestamp):
    """
    暴力找到md5((data + str(timestamp) + code).encode())[:5]=='00000'
    """
    base = f"{data}{timestamp}"
    for i in range(100_000_000):
        code = str(i)
        val = md5(f"{base}{code}".encode()).hexdigest()
        if val.startswith("00000"):
            return code
    raise Exception("POW failed")

def main():
    url = "http://ht92y2fy3v97eeyh.instance.penguin.0ops.sjtu.cn:18080/flag"  # 替换为靶场服务器地址
    now = int(time.time())
    ts = now
    ts_group = int(ts // 600 * 600)
    flag_msg = f"Give me! It's MyFLAG!!!!!{ts_group}"

    # 1. 构造密文data
    data = build_ciphertext(flag_msg)
    # 2. POW
    code = find_pow(data, str(ts))
    print(f"data: {data}\ntimestamp: {ts}\ncode: {code}")
    # 3. POST
    res = requests.post(url, data={"data": data, "timestamp": str(ts), "code": code})
    print(res.text)

if __name__ == "__main__":
    main()