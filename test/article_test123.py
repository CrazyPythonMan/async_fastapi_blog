import requests

BASE_URL = "http://127.0.0.1:8000/api"

# -------------------
# 1. 登录获取 token
# -------------------
def login(username: str, password: str) -> str:
    url = f"{BASE_URL}/auth/jwt/login"
    data = {
        "username": username,
        "password": password,
        "grant_type": "password"  # 如果接口默认可省略
    }
    resp = requests.post(url, data=data)
    resp.raise_for_status()
    token = resp.json()["access_token"]
    print(f"token: {token}")
    return token

# -------------------
# 2. 封装 headers
# -------------------
def get_headers(token: str):
    return {"Authorization": f"Bearer {token}"}

# -------------------
# 3. 测试创建文章
# -------------------
def test_create_article(token: str):
    url = f"{BASE_URL}/articles/"
    headers = get_headers(token)
    data = {
        "title": "测试文章",
        "content": "这是测试内容",
        "category_id": 1,
        "tag_ids": None
    }
    resp = requests.post(url, json=data, headers=headers)
    resp.raise_for_status()
    print("创建文章:", resp.json())
    return resp.json()["id"]

# -------------------
# 4. 测试查询文章
# -------------------
def test_get_article(article_id: int, token: str):
    url = f"{BASE_URL}/articles/{article_id}"
    headers = get_headers(token)
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    print("查询文章:", resp.json())

# -------------------
# 5. 测试更新文章
# -------------------
def test_update_article(article_id: int, token: str):
    url = f"{BASE_URL}/articles/{article_id}"
    headers = get_headers(token)
    data = {
        "title": "更新后的标题",
        "content": "更新后的内容",
        "tag_ids": [2, 3]
    }
    resp = requests.put(url, json=data, headers=headers)
    resp.raise_for_status()
    print("更新文章:", resp.json())

# -------------------
# 6. 测试删除文章
# -------------------
def test_delete_article(article_id: int, token: str):
    url = f"{BASE_URL}/articles/{article_id}"
    headers = get_headers(token)
    resp = requests.delete(url, headers=headers)
    resp.raise_for_status()
    print("删除文章:", resp.json())

# -------------------
# 7. 测试流程
# -------------------
# if __name__ == "__main__":
token = login("1@1.com", "1")
article_id = test_create_article(token)
test_get_article(article_id, token)
test_update_article(article_id, token)
test_delete_article(article_id, token)
