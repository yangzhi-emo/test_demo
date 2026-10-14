import yaml
import os


def get_config():
    """
    读取 yaml 配置文件

    根据环境变量 TEST_ENV 选择环境（默认 dev），
    返回当前环境的配置内容
    """

    # 读取环境变量，没设置就用 dev
    env = os.getenv("TEST_ENV", "dev")

    # 获取当前项目根目录（往上两级：test_demo）
    base_dir = os.path.dirname(
        os.path.dirname(__file__)
    )

    # 拼接配置文件路径
    config_path = os.path.join(
        base_dir,
        "config",
        "config.yaml"
    )

    # 打开 yaml 文件
    with open(
        config_path,
        "r",
        encoding="utf-8"
    ) as f:
        config = yaml.safe_load(f)

    # 返回当前环境的配置
    return config[env]
