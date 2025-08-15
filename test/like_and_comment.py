import requests

BASE_URL = "http://127.0.0.1:8000/api"  # 你的FastAPI服务地址


def login(username: str, password: str) -> str:
    """登录获取 JWT Token"""
    url = f"{BASE_URL}/auth/jwt/login"
    data = {
        "username": username,
        "password": password,
        "grant_type": "password"   # FastAPI Users 默认需要
    }
    resp = requests.post(url, data=data)
    resp.raise_for_status()
    token = resp.json()["access_token"]
    print("登录成功，token:", token)
    return token


def get_headers(token: str):
    return {"Authorization": f"Bearer {token}"}


# ---------------------------
#   评论系统
# ---------------------------
def test_create_comment(token: str, article_id: int):
    url = f"{BASE_URL}/comments/"
    data = {"content": "这是一条测试评论", "article_id": article_id}
    resp = requests.post(url, json=data, headers=get_headers(token))
    resp.raise_for_status()
    print("创建评论:", resp.json())
    return resp.json()["id"]


def test_get_comment(token: str, comment_id: int):
    url = f"{BASE_URL}/comments/{comment_id}"
    resp = requests.get(url, headers=get_headers(token))
    resp.raise_for_status()
    print("获取评论:", resp.json())


def test_update_comment(token: str, comment_id: int):
    url = f"{BASE_URL}/comments/{comment_id}"
    data = {"content": "更新后的评论内容"}
    resp = requests.put(url, json=data, headers=get_headers(token))
    resp.raise_for_status()
    print("更新评论:", resp.json())


def test_delete_comment(token: str, comment_id: int):
    url = f"{BASE_URL}/comments/{comment_id}"
    resp = requests.delete(url, headers=get_headers(token))
    resp.raise_for_status()
    print("删除评论:", resp.json())


def test_list_comments(token: str, article_id: int):
    url = f"{BASE_URL}/comments/article/{article_id}"
    resp = requests.get(url, headers=get_headers(token))
    resp.raise_for_status()
    print("文章评论列表:", resp.json())


# ---------------------------
#   点赞系统
# ---------------------------
def test_like_article(token: str, article_id: int):
    url = f"{BASE_URL}/likes/article/{article_id}"
    resp = requests.post(url, headers=get_headers(token))
    resp.raise_for_status()
    print("点赞:", resp.json())


def test_unlike_article(token: str, article_id: int):
    url = f"{BASE_URL}/likes/article/{article_id}"
    resp = requests.delete(url, headers=get_headers(token))
    resp.raise_for_status()
    print("取消点赞:", resp.json())


def test_get_likes(token: str, article_id: int):
    url = f"{BASE_URL}/likes/article/{article_id}"
    resp = requests.get(url, headers=get_headers(token))
    resp.raise_for_status()
    print("点赞情况:", resp.json())


# ---------------------------
#   主流程测试
# ---------------------------
if __name__ == "__main__":
    # 1. 登录获取 token
    token = login("1@1.com", "1")

    # # 2. 指定一个已有的文章ID
    # article_id = 13
    #
    # # --- 评论测试 ---
    # comment_id = test_create_comment(token, article_id)
    # test_get_comment(token, comment_id)
    # test_update_comment(token, comment_id)
    # test_list_comments(token, article_id)
    # test_delete_comment(token, comment_id)

    # # --- 点赞测试 ---
    # test_like_article(token, article_id)
    # test_get_likes(token, article_id)
    # test_unlike_article(token, article_id)
    # test_get_likes(token, article_id)
