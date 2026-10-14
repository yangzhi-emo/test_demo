import pytest
import allure

from utils.data_reader import get_login_cases


@allure.feature("登录模块")
@allure.story("登录接口")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.parametrize("case", get_login_cases())
def test_login(api, case):
    # 通过 Fixture 提供的 api 客户端发送登录请求
    with allure.step("发送登录请求"):
        response = api.post(
            "/login",
            json={
                "username": case["username"],
                "password": case["password"]
            }
        )

    # 检查实际 HTTP 状态码是否符合预期
    with allure.step("校验状态码"):
        assert response.status_code == case["expected_status"]

    # 如果登录成功，进一步验证响应中存在 Token
    if case["expected_status"] == 200:
        with allure.step("校验 Token 存在"):
            assert response.json()["token"]


# 现在自动传请求头
@allure.feature("用户模块")
@allure.story("用户接口")
@allure.severity(allure.severity_level.NORMAL)
def test_user_without_token(api):
    # 不传 Authorization 请求头，模拟未登录访问
    response = api.get("/user")

    # 预期服务器拒绝访问
    assert response.status_code == 200
    assert response.json()["data"]["username"] == "test"


@allure.feature("用户模块")
@allure.story("用户接口")
@allure.severity(allure.severity_level.CRITICAL)
def test_user_with_wrong_token(api):
    # 构造错误的 Token
    headers = {
        "Authorization": "Bearer wrong-token"
    }

    # 携带错误 Token 查询用户
    response = api.get("/user", headers=headers)

    # 预期认证失败
    assert response.status_code == 401
    assert response.json()["message"] == "未授权"


@allure.feature("用户模块")
@allure.story("用户接口")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_then_get_user(api):
    # 第一步：使用正确账号密码登录
    login_response = api.post(
        "/login",
        json={
            "username": "test",
            "password": "123456"
        }
    )

    # 登录必须成功，否则不应继续查询用户
    assert login_response.status_code == 200

    # 第二步：访问受保护的用户接口
    user_response = api.get("/user")

    # 第五步：校验状态码和用户信息
    assert user_response.status_code == 200
    assert user_response.json()["data"]["username"] == "test"


@allure.feature("用户模块")
@allure.story("用户接口")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_user_with_token(api):
    # 不需要写 headers，ApiClient 会自动添加 Token
    response = api.get("/user")

    # 校验结果
    assert response.status_code == 200

    # 校验用户
    assert response.json()["data"]["username"] == "test"
