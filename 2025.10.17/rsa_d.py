def rsa_decrypt(p, q, e, c):
     
    n = p * q
     
    phi = (p - 1) * (q - 1)

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
    
    d = mod_inverse(e, phi)

    m = pow(c, d, n)

    return m

p =  9648423029010515676590551740010426534945737639235739800643989352039852507298491399561035009163427050370107570733633350911691280297777160200625281665378483
q =  11874843837980297032092405848653656852760910154543380907650040190704283358909208578251063047732443992230647903887510065547947313543299303261986053486569407
e =  65537
c =  83208298995174604174773590298203639360540024871256126892889661345742403314929861939100492666605647316646576486526217457006376842280869728581726746401583705899941768214138742259689334840735633553053887641847651173776251820293087212885670180367406807406765923638973161375817392737747832762751690104423869019034

m = rsa_decrypt(p, q, e, c)

print(f"The raw number message is: {m}")

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

print(f"ASCII decoded message: {ascii_message}")