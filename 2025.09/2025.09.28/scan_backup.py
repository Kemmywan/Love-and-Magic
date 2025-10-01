import requests

def load_backup_files(wordlist_path):
    with open(wordlist_path, 'r', encoding='utf-8') as f:
        # 去除每行首尾空白，过滤掉空行
        return [line.strip() for line in f if line.strip()]

# 用法示例
BACKUP_FILES = load_backup_files('./backup_words.txt')

# 判断为正常的状态码
NORMAL_STATUS = [200, 301, 302, 304]

def searchBackupFiles(baseurl):
    # 获取首页长度作为基准
    try:
        r_home = requests.get(baseurl, timeout=5)
        home_length = len(r_home.content)
    except Exception:
        home_length = None

    print("Scanning backup files for:", baseurl)
    for filename in BACKUP_FILES:
        if baseurl.endswith('/'):
            url = baseurl + filename
        else:
            url = baseurl + '/' + filename

        try:
            r = requests.get(url, timeout=5, allow_redirects=True)
            status = r.status_code
            length = len(r.content)
        except Exception as e:
            print(f"[error] {url} Exception: {e}")
            continue

        # 状态码异常
        if status not in NORMAL_STATUS:
            print(f"[unnormal status code] {url}    {status}")
        # 长度异常
        elif home_length is not None and abs(length - home_length) > 1000:
            print(f"[unnormal length] {url}    {length}")
        else:
            print(f"[normal] {url}    {status}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        searchBackupFiles(sys.argv[1])
    else:
        print("Usage: python util.py <baseurl>")
