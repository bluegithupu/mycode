import os
import logging
import datetime
from pathlib import Path
from rich.logging import RichHandler
from rich.console import Console
from rich.traceback import install

# 安装 Rich 的异常处理器
install(show_locals=True)

# 创建日志目录
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# 从环境变量获取日志级别，默认为 INFO
DEFAULT_LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
LOG_LEVEL = getattr(logging, DEFAULT_LOG_LEVEL, logging.INFO)


def setup_logger(name: str, level=None, log_to_file=True):
    """
    设置并返回一个配置好的logger实例

    Args:
        name: logger的名称
        level: 日志级别，如果为None则使用环境变量中的设置
        log_to_file: 是否将日志写入文件，默认为True

    Returns:
        logging.Logger: 配置好的logger实例
    """
    # 使用传入的级别或环境变量中的级别
    log_level = level if level is not None else LOG_LEVEL

    # 创建logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # 如果logger已经有处理器，说明已经被配置过，直接返回
    if logger.handlers:
        return logger

    # 创建控制台处理器（使用Rich）
    console_handler = RichHandler(
        rich_tracebacks=True,
        console=Console(force_terminal=True),
        tracebacks_show_locals=True,
        show_time=True,
        show_path=True
    )
    console_handler.setLevel(log_level)

    # 设置控制台日志格式
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # 如果需要，添加文件处理器
    if log_to_file:
        # 生成日志文件名（包含日期）
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = LOG_DIR / f"{name}_{current_time}.log"

        # 创建文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(log_level)

        # 设置文件日志格式（更详细的格式）
        file_formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)-8s %(name)s: '
            '%(message)s (%(filename)s:%(lineno)d)'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        logger.info(f"日志文件创建于: {log_file}")

    return logger
