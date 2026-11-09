
# -*- coding: utf-8 -*-
# 声明当前 Python 文件使用 UTF-8 编码，保证中文注释和中文字符串正常显示。

"""
断言封装工具
================

把 testcases 测试用例中重复编写的 assert 断言统一封装到 Assert 类中。

以前每个测试用例都要自己写：
    assert response.status_code == 200
    assert response.json()["code"] == 200

现在只需要调用：
    from utils.assertions import Assert
    Assert.assert_success(response)

就可以自动检查：
    1. HTTP 状态码是否为 200
    2. 业务 code 是否为 200

为什么要封装断言？

1. 简化测试用例：用例只需要调用一个方法，不需要重复写断言。
2. 统一错误提示：断言失败时，自动输出实际值、预期值等信息。
3. 方便后期维护：如果接口返回格式发生变化，只需要修改这个文件。
"""

import allure
# 导入 allure 模块。
# Allure 是自动化测试报告工具。
# 后面使用 @allure.step() 装饰器，可以把断言方法记录到测试报告中。


class Assert:
    # 定义一个名为 Assert 的类。
    # 可以把这个类理解为一个断言工具箱。
    # 所有常用的断言方法都放在这个类里面。
    # 以后通过 Assert.方法名() 就能直接使用，不需要创建对象。


    @staticmethod
    # 静态方法装饰器。
    # 表示这个方法不依赖类的实例对象。
    # 所以可以直接通过 Assert._extract_json() 调用。

    def _extract_json(response):
        # 定义一个方法，名称叫 _extract_json。
        # response：接收接口返回的响应对象。
        # 前面的下划线 _ 是一种命名习惯，表示这是类内部使用的辅助方法。

        """
        把接口响应体解析成 Python 字典。
        如果解析失败，就返回空字典，避免程序因为 JSON 解析失败而直接报错。
        """

        try:
            # try 表示尝试执行下面的代码。
            # 如果下面的代码发生异常，就会进入 except。

            return response.json()
            # response.json()：将接口返回的 JSON 数据解析成 Python 对象。
            # 例如接口返回 {"code": 200}，解析后得到 Python 字典。
            # return：将解析结果返回给调用这个方法的地方。

        except Exception:
            # except：如果 try 中的代码执行失败，就执行这里。
            # Exception：捕获普通异常。

            return {}
            # 返回一个空字典。
            # 例如服务器返回 HTML、普通文本，导致 JSON 解析失败。
            # 这里就返回 {}，避免解析异常直接向外抛出。


    @staticmethod
    # 声明下面的方法是静态方法，可以直接通过类名调用。

    @allure.step("断言 HTTP 状态码 == {expected}")
    # Allure 步骤装饰器。
    # 执行这个方法时，Allure 测试报告会记录当前断言步骤。
    # {expected} 会显示预期的 HTTP 状态码。

    def assert_status(response, expected=200):
        # 定义 HTTP 状态码断言方法。
        # response：接口返回的响应对象。
        # expected=200：预期状态码，默认值为 200。
        # 如果调用时不传 expected，就默认检查 HTTP 200。

        """校验 HTTP 状态码，比如 200 / 401 / 404"""

        actual = response.status_code
        # 获取接口实际返回的 HTTP 状态码。
        # status_code 是 requests 响应对象的属性。
        # 例如实际返回 200，就把 200 保存到 actual 变量中。

        body = Assert._extract_json(response)
        # 调用上面封装的 _extract_json() 方法。
        # 将接口返回的 JSON 数据解析出来。
        # 保存到 body 变量中，方便断言失败时打印响应内容。

        assert actual == expected, (
            # assert 是 Python 的断言语句。
            # 判断 actual 是否等于 expected。
            # 如果相等，断言通过，程序继续执行。
            # 如果不相等，断言失败，输出后面的错误信息。

            f"❌ 状态码不对：期望 {expected}，实际 {actual}；返回体={body}"
            # f 表示格式化字符串。
            # 可以直接在字符串中使用 {} 插入变量的值。
            # expected：预期状态码。
            # actual：实际状态码。
            # body：接口返回的数据。
        )


    @staticmethod
    # 声明静态方法，可以直接通过 Assert.assert_biz_code() 调用。

    @allure.step("断言业务 code == {expected}")
    # 在 Allure 测试报告中记录业务状态码断言步骤。

    def assert_biz_code(response, expected=200):
        # 定义业务状态码断言方法。
        # response：接口返回的响应对象。
        # expected=200：预期业务状态码，默认是 200。

        """
        校验业务 code。
        这里检查的是 Flask 返回 JSON 中的 code 字段，
        不是 HTTP 状态码。

        接口返回格式示例：
        {
            "code": 200,
            "message": "请求成功",
            "data": {}
        }
        """

        body = Assert._extract_json(response)
        # 调用 JSON 解析方法。
        # 将接口响应内容转换成 Python 字典。
        # 例如 {"code": 200} 就变成 {"code": 200} 这个字典对象。

        actual = body.get("code")
        # 使用字典的 get() 方法获取 code 字段的值。
        # body.get("code") 相当于从字典中读取 code 对应的数据。
        # 如果 code 字段不存在，默认返回 None。
        # 将获取到的值保存到 actual 变量中。

        assert actual == expected, (
            # 判断实际业务 code 是否等于预期业务 code。
            # 如果相等，断言通过。
            # 如果不相等，断言失败。

            f"❌ 业务 code 不对：期望 {expected}，实际 {actual}；"
            # 输出预期业务状态码和实际业务状态码。

            f"message={body.get('message')}"
            # 继续输出接口返回的 message 字段。
            # 例如 message="密码错误"。
            # 这里使用两个 f 字符串相邻的方式拼接内容。
        )


    @staticmethod
    # 声明静态方法。

    @allure.step("断言接口调用成功（HTTP 200 且业务 code 200）")
    # 在 Allure 报告中记录接口成功断言步骤。

    def assert_success(response):
        # 定义接口成功断言方法。
        # response：接口返回的响应对象。
        # 这个方法不需要传入 expected，因为这里固定要求两个状态码都是 200。

        """最常用：成功接口一口气校验完（HTTP 200 + 业务 code 200）"""

        Assert.assert_status(response, 200)
        # 调用 assert_status() 方法。
        # 检查 HTTP 状态码是否等于 200。
        # 如果不是 200，就会断言失败。

        Assert.assert_biz_code(response, 200)
        # 调用 assert_biz_code() 方法。
        # 检查业务 code 是否等于 200。
        # 两项检查都通过，才代表这个方法执行成功。


    @staticmethod
    # 声明静态方法。

    @allure.step("断言业务失败：HTTP {http_status} 且 code == {biz_code}")
    # 在 Allure 报告中记录失败断言步骤。
    # {http_status} 和 {biz_code} 分别表示预期 HTTP 状态码和业务状态码。

    def assert_fail(response, http_status=401, biz_code=401):
        # 定义接口失败断言方法。
        # response：接口返回的响应对象。
        # http_status=401：默认预期 HTTP 状态码为 401。
        # biz_code=401：默认预期业务 code 为 401。
        # 两个参数都可以在调用时修改。

        """最常用：失败接口一口气校验完"""

        Assert.assert_status(response, http_status)
        # 调用 HTTP 状态码断言方法。
        # 检查实际 HTTP 状态码是否等于传入的 http_status。
        # 默认检查是否为 401。

        Assert.assert_biz_code(response, biz_code)
        # 调用业务状态码断言方法。
        # 检查实际业务 code 是否等于传入的 biz_code。
        # 默认检查是否为 401。


    @staticmethod
    # 声明静态方法。

    @allure.step("断言相等：{msg}")
    # 在 Allure 报告中记录相等性断言步骤。
    # msg 是调用时传入的提示信息。

    def assert_equal(actual, expected, msg=""):
        # 定义一个通用的相等断言方法。
        # actual：实际值。
        # expected：预期值。
        # msg=""：自定义提示信息，默认是空字符串。
        # 例如可以比较商品名称、用户名、订单金额等。

        """通用相等断言，比如 商品名 == '机械键盘'"""

        assert actual == expected, (
            # 判断实际值是否等于预期值。
            # 相等则通过，不相等则失败。

            f"❌ 期望={expected}，实际={actual}；{msg}"
            # 断言失败时输出预期值、实际值和自定义提示信息。
        )


    @staticmethod
    # 声明静态方法。

    @allure.step("断言字段 {field} 在返回 data 里")
    # 在 Allure 报告中记录字段存在性检查步骤。
    # {field} 会显示本次检查的字段名称。

    def assert_field_in_data(response, field):
        # 定义一个检查 data 中是否存在指定字段的方法。
        # response：接口返回的响应对象。
        # field：需要检查的字段名称。
        # 例如 field="token"，就是检查 data 中有没有 token。

        """校验 data 里有某个字段"""

        body = Assert._extract_json(response)
        # 解析接口返回的 JSON 数据。
        # 将解析结果保存到 body 变量中。

        data = body.get("data") or {}
        # 从 body 字典中获取 data 字段。
        # 如果 data 不存在、值为 None 或其他空值，就使用空字典 {}。
        # 这样可以避免后面检查字段时出现 NoneType 错误。

        assert field in data, (
            # 判断 field 是否存在于 data 中。
            # in 是 Python 的成员判断运算符。
            # 例如 "token" in data，就是检查 data 中有没有 token 这个键。
            # 如果存在，断言通过；不存在，断言失败。

            f"❌ data 里没找到字段 {field}；data={data}"
            # 断言失败时输出缺少的字段名称以及当前 data 内容。
        )

# Assert 类一共有 7 个方法：
#
# 1. _extract_json(response)
#    解析接口返回的 JSON 数据。
#
# 2. assert_status(response)
#    断言 HTTP 状态码是否正确。
#
# 3. assert_biz_code(response)
#    断言业务 code 是否正确。
#
# 4. assert_success(response)
#    组合断言：HTTP 200 + 业务 code 200。
#
# 5. assert_fail(response)
#    组合断言：接口是否按预期失败。
#
# 6. assert_equal(actual, expected)
#    通用相等断言，比较实际值和预期值。
#
# 7. assert_field_in_data(response, field)
#    检查接口返回的 data 中是否存在指定字段。
