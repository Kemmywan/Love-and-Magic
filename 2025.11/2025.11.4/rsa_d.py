def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a) # x1 * (b % a) + y1 * a = gcd
        y = x1
        x = y1 - (b // a) * x1
        return gcd, x, y

def mod_inverse(a, m):
        gcd, x, y = extended_gcd(a, m) # x * a + y * m = gcd
        if gcd != 1:
            raise ValueError("Modular inverse does not exist")
        else:
            return x % m

def rsa_decrypt(p, q, e, c):
     
    n = p * q
     
    phi = (p - 1) * (q - 1)
    
    d = mod_inverse(e, phi)

    m = pow(c, d, n)

    return m

p = 8637633767257008567099653486541091171320491509433615447539162437911244175885667806398411790524083553445158113502227745206205327690939504032994699902053229 
q = 12640674973996472769176047937170883420927050821480010581593137135372473880595613737337630629752577346147039284030082593490776630572584959954205336880228469 
dp = 6500795702216834621109042351193261530650043841056252930930949663358625016881832840728066026150264693076109354874099841380454881716097778307268116910582929 
dq = 783472263673553449019532580386470672380574033551303889137911760438881683674556098098256795673512201963002175438762767516968043599582527539160811120550041 
c = 24722305403887382073567316467649080662631552905960229399079107995602154418176056335800638887527614164073530437657085079676157350205351945222989351316076486573599576041978339872265925062764318536089007310270278526159678937431903862892400747915525118983959970607934142974736675784325993445942031372107342103852

n = p * q

# 使用 CRT 参数加速解密
mp = pow(c, dp, p)  # 在模 p 下解密
mq = pow(c, dq, q)  # 在模 q 下解密

# 使用中国剩余定理合并结果
m = (mp * q * mod_inverse(q, p) + mq * p * mod_inverse(p, q)) % n

print(f"The raw number message is: {m}")
print(f"The text message is: {bytes.fromhex(hex(m)[2:])}")

# # 将数字转换为字符串，然后每两位作为 ASCII 码
# m_str = str(m)
# print(f"The decimal string: {m_str}")

# # 确保长度为偶数
# if len(m_str) % 2 == 1:
#     m_str = '0' + m_str

# print(f"Padded decimal string: {m_str}")

# # 每两位作为 ASCII 码进行解码
# ascii_message = ""
# for i in range(0, len(m_str), 2):
#     ascii_code = int(m_str[i:i+2])
#     if 32 <= ascii_code <= 126:  # 可打印 ASCII 范围
#         ascii_message += chr(ascii_code)
#     else:
#         ascii_message += f"[{ascii_code}]"  # 不可打印字符用方括号表示

# print(f"ASCII decoded message: {ascii_message}")