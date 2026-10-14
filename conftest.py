
import pytest

# 导入公共请求客户端
from utils.api_client import ApiClient

# 导入配置文件读取方法
from utils.config_reader import get_config
from utils.logger import logger

@pytest.fixture
def api():
    """
    创建公共接口客户端。

    测试函数只要声明 api 参数，
    pytest 就会自动调用这个 Fixture，
    并把返回的客户端传给测试函数。
    """
    # 获取yaml配置
    config = get_config()
    # 从配置文件获取基础 URL
    base_url = config["base_url"]
    logger.info("当前环境 base_url：%s", base_url)

    # 创建客户端并提供给测试用例
    client = ApiClient(base_url)

    return client

# 告诉 pytest：这是一个测试前置准备函数，需要的时候自动执行
@pytest.fixture(autouse=True)
def token(api):
    """
    自动登录并获取 Token

    流程：
    1. 调用登录接口
    2. 获取返回 JSON
    3. 提取 token
    4. 返回给测试用例
    """

    # 登录接口
    response = api.post(
        "/login",
        json={
            "username": "test",
            "password": "123456"
        }
    )

    # 判断登录成功
    assert response.status_code == 200

    # 获取 token
    token = response.json()["token"]

    # 保存到 api 对象
    # 后续 api.get() 会自动携带
    api.token = token