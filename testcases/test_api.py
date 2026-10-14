import requests


def test_create_user():
    url = "https://jsonplaceholder.typicode.com/posts"

    data = {
        "title": "测试用户",
        "body": "这是自动化测试",
        "userId": 1
    }

    response = requests.post(url, json=data)

    print("状态码：", response.status_code)
    print("返回数据：", response.json())

    assert response.status_code == 201

    result = response.json()

    assert result["title"] == "测试用户"
    assert result["body"] == "这是自动化测试"
    assert result["userId"] == 1