"""
统一的日志配置模块
"""
import logging
import sys
from pathlib import Path
from typing import Optional

def setup_logging(
    log_level: int = logging.INFO,
    log_file: Optional[Path] = None,
    console_output: bool = True
) -> logging.Logger:
    """
    设置统一的日志配置
    
    Args:
        log_level: 日志级别
        log_file: 日志文件路径
        console_output: 是否输出到控制台
        
    Returns:
        配置好的根日志器
    """
    # 获取根日志器
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # 清除现有的处理器
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # 创建日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台输出
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # 文件输出
    if log_file:
        # 确保日志目录存在
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """
    获取配置好的日志器
    
    Args:
        name: 日志器名称
        
    Returns:
        配置好的日志器
    """
    logger = logging.getLogger(name)
    
    # 如果根日志器没有处理器，设置默认配置
    if not logging.getLogger().handlers:
        setup_logging()
    
    return logger