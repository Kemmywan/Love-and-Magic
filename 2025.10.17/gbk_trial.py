# 方法1：每两位作为一个字节
decimal = "606046152623600817831216121621196386"
bytes_data = bytes([int(decimal[i:i+2]) for i in range(0, len(decimal), 2)])
print(bytes_data)
try:
    result = bytes_data.decode('ascii')
    print(f"ASCII解码结果: {result}")
except:
    print("ASCII解码失败")

