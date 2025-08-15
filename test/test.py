import requests

# -------------------
# 1. 登录获取 token
# -------------------
def login():
    login_url = "http://127.0.0.1:8000/api/auth/jwt/login"
    login_data = {
        "username": "1@1.com",
        "password": "1",
        "grant_type": "password"  # 如果接口已默认，也可以省略
    }

    # 使用 data= 发送 form-data
    resp = requests.post(login_url, data=login_data)
    # resp.raise_for_status()
    token = resp.json()["access_token"]
    return token
# -------------------
# 2. 调用受保护接口
# -------------------
# print(token)
def get_protected_api():
    protected_url = "http://127.0.0.1:8000/api/categories/"
    headers = {
        "Authorization": f"Bearer {login()}"
    }

    # 假设保护接口还有 query 参数 skip, limit
    params = {
        "skip": 0,
        "limit": 10
    }

    resp2 = requests.get(protected_url, headers=headers, params=params)
    resp2.raise_for_status()
    print(resp2.json())
def get_protected_api_create(con):
    protected_url = "http://127.0.0.1:8000/api/categories/"
    headers = {
        "Authorization": f"Bearer {login()}",
        "Content-Type": "application/json"
    }

    # 假设保护接口还有 query 参数 skip, limit
    params = {
        "name":f'{con}'
    }

    resp2 = requests.post(protected_url, headers=headers, json=params)
    resp2.raise_for_status()
    print(resp2.json())
def get_protected_api_put(con):
    protected_url = "http://127.0.0.1:8000/api/categories/"
    headers = {
        "Authorization": f"Bearer {login()}",
        "Content-Type": "application/json"
    }

    # 假设保护接口还有 query 参数 skip, limit
    params = {
        "name":f'{con}'
    }

    resp2 = requests.post(protected_url, headers=headers, json=params)
    resp2.raise_for_status()
    print(resp2.json())
# get_protected_api_create('putt接口测试内容')
# get_protected_api()
def get_protected_api_by_id(con):
    protected_url = "http://127.0.0.1:8000/api/categories/"
    headers = {
        "Authorization": f"Bearer {login()}",
        "Content-Type": "application/json"
    }

    # 假设保护接口还有 query 参数 skip, limit
    params = {
        "name":f'{con}'
    }

    resp2 = requests.post(protected_url, headers=headers, params=params)
    resp2.raise_for_status()
    print(resp2.json())

def _test_create_article(token: str):
    url = f"http://127.0.0.1:8000/api/articles/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": "11测试文章",
        "content": "11这是测试内容",
        "category_id": 1,
        "tag_ids": None
    }
    resp = requests.post(url, json=data, headers=headers)
    resp.raise_for_status()
    print("创建文章:", resp.json())
    return resp.json()["id"]
_test_create_article(login())