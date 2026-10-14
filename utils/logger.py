import logging
from pathlib import Path

# 获取项目根目录：logger.py 的上两级目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 日志文件统一存放在项目根目录下的 logs 文件夹
LOG_DIR = PROJECT_ROOT / "logs"

# 如果 logs 文件夹不存在，就自动创建
LOG_DIR.mkdir(exist_ok=True)

# 指定日志文件的完整路径
LOG_FILE = LOG_DIR / "test.log"

# 创建一个名为 api_test 的日志记录器
logger = logging.getLogger("api_test")

# 设置最低记录级别为 INFO
# INFO、WARNING、ERROR 等级别会被记录，DEBUG 不会
logger.setLevel(logging.INFO)

# 避免重复添加处理器，导致同一条日志重复输出
if not logger.handlers:

    # 设置日志格式：时间 - 级别 - 内容
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    # 创建文件处理器：把日志写入 test.log
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    # 创建终端处理器：让日志也显示在控制台
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 把文件和终端处理器添加到日志记录器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)