
import requests

# 导入我们刚刚编写的日志工具
from utils.logger import logger


class ApiClient:

    def __init__(self, base_url):
        # 去掉基础地址末尾的斜杠，避免拼接出双斜杠
        self.base_url = base_url.rstrip("/")

        # 初始化 Token
        # 刚开始没有登录，所以为空
        self.token = None

    def get_headers(self):
        """
        自动生成请求头

        如果已经登录：
        自动加入 Token

        如果没有登录：
        返回空请求头
        """

        # 创建一个空字典
        headers = {}

        # 判断当前对象有没有 Token
        if self.token:
            # 添加 Authorization 请求头
            headers["Authorization"] = (
                f"Bearer {self.token}"
            )

        return headers

    def get(self, path, headers=None, params=None):
        # 如果调用接口时没有传 headers
        # 自动使用对象里的 Token 生成请求头
        if headers is None:
            headers = self.get_headers()

        # 拼接完整 URL，同时兼容 path 是否以 / 开头
        url = f"{self.base_url}/{path.lstrip('/')}"

        # 记录请求方法和地址，不记录密码或 Token
        logger.info("发送 GET 请求：%s", url)

        try:
            # 发送 GET 请求，设置 10 秒超时
            response = requests.get(
                url=url,
                headers=headers,
                params=params,
                timeout=10
            )

            # 记录服务器返回的 HTTP 状态码
            logger.info(
                "GET 响应状态码：%s",
                response.status_code
            )

            # 返回响应对象，供测试用例继续断言
            return response

        except requests.RequestException:
            # 记录网络异常及详细错误信息
            logger.exception("GET 请求异常：%s", url)

            # 继续抛出异常，避免把请求失败误判成正常返回
            raise

    def post(self, path, json=None, headers=None):
        # 如果调用接口时没有传 headers
        # 自动使用对象里的 Token 生成请求头
        if headers is None:
            headers = self.get_headers()

        # 拼接 POST 请求的完整 URL
        url = f"{self.base_url}/{path.lstrip('/')}"

        # 记录请求方法和地址
        logger.info("发送 POST 请求：%s", url)

        try:
            # 发送 POST 请求，json 参数会自动序列化为 JSON
            response = requests.post(
                url=url,
                json=json,
                headers=headers,
                timeout=10
            )

            # 记录响应状态码
            logger.info(
                "POST 响应状态码：%s",
                response.status_code
            )

            # 返回响应对象，供测试用例校验
            return response

        except requests.RequestException:
            # 记录请求异常，方便后续排查
            logger.exception("POST 请求异常：%s", url)

            # 将异常继续交给 pytest 处理
            raise