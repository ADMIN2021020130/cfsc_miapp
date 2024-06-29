import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path

# 创建logs目录
logs_dir = Path(__file__).resolve().parent.parent.parent / "logs"
os.makedirs(logs_dir, exist_ok=True)

# 配置日志格式
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 创建一个处理器,用于写入应用程序日志文件
app_handler = RotatingFileHandler(logs_dir / "app.log", maxBytes=1024*1024*10, backupCount=10)
app_handler.setFormatter(log_formatter)

# 创建一个处理器,用于写入gunicorn访问日志文件
access_handler = RotatingFileHandler(logs_dir / "gunicorn_access.log", maxBytes=1024*1024*10, backupCount=10)
access_handler.setFormatter(log_formatter)

# 创建一个处理器,用于写入gunicorn错误日志文件
error_handler = RotatingFileHandler(logs_dir / "gunicorn_error.log", maxBytes=1024*1024*10, backupCount=10)
error_handler.setFormatter(log_formatter)

# 创建一个控制台处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

# 函数: 创建或获取logger实例
def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if name == "gunicorn.access":
        if not logger.handlers:
            logger.addHandler(access_handler)
    elif name == "gunicorn.error":
        if not logger.handlers:
            logger.addHandler(error_handler)
    else:
        if not logger.handlers:
            logger.addHandler(app_handler)
            logger.addHandler(console_handler)
    
    return logger