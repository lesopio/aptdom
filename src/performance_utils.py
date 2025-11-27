"""
性能监控和优化工具
"""
import time
import functools
import tracemalloc
from typing import Callable, Any, Dict
import psutil
import os

from .logging_config import get_logger

logger = get_logger(__name__)

def monitor_performance(func: Callable) -> Callable:
    """
    性能监控装饰器，记录函数执行时间和内存使用
    
    Args:
        func: 要监控的函数
        
    Returns:
        包装后的函数
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 开始监控内存
        tracemalloc.start()
        
        # 记录开始时间
        start_time = time.time()
        
        # 记录开始内存
        process = psutil.Process(os.getpid())
        start_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            # 记录结束时间
            end_time = time.time()
            execution_time = end_time - start_time
            
            # 记录结束内存
            end_memory = process.memory_info().rss / 1024 / 1024
            memory_usage = end_memory - start_memory
            
            # 获取内存快照
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            # 记录性能数据
            performance_data = {
                'function': func.__name__,
                'execution_time': round(execution_time, 4),
                'memory_usage_mb': round(memory_usage, 2),
                'peak_memory_mb': round(peak / 1024 / 1024, 2),
                'current_memory_mb': round(current / 1024 / 1024, 2)
            }
            
            # 根据执行时间选择日志级别
            log_level = logging.DEBUG
            if execution_time > 1.0:  # 超过1秒警告
                log_level = logging.WARNING
            elif execution_time > 5.0:  # 超过5秒错误
                log_level = logging.ERROR
            
            logger.log(log_level, 
                      f"性能监控 - {func.__name__}: "
                      f"时间={execution_time:.3f}s, "
                      f"内存使用={memory_usage:.2f}MB, "
                      f"峰值内存={peak/1024/1024:.2f}MB")
            
            return result
    
    return wrapper

class PerformanceMonitor:
    """性能监控器类"""
    
    def __init__(self, name: str = "default"):
        self.name = name
        self.start_time: float = 0
        self.start_memory: float = 0
        self.process = psutil.Process(os.getpid())
    
    def __enter__(self):
        """进入上下文管理器"""
        self.start_time = time.time()
        self.start_memory = self.process.memory_info().rss / 1024 / 1024
        tracemalloc.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文管理器"""
        end_time = time.time()
        end_memory = self.process.memory_info().rss / 1024 / 1024
        
        execution_time = end_time - self.start_time
        memory_usage = end_memory - self.start_memory
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        performance_data = {
            'monitor_name': self.name,
            'execution_time': round(execution_time, 4),
            'memory_usage_mb': round(memory_usage, 2),
            'peak_memory_mb': round(peak / 1024 / 1024, 2)
        }
        
        log_level = logging.DEBUG
        if execution_time > 1.0:
            log_level = logging.WARNING
        elif execution_time > 5.0:
            log_level = logging.ERROR
            
        logger.log(log_level,
                  f"性能监控 [{self.name}]: "
                  f"时间={execution_time:.3f}s, "
                  f"内存使用={memory_usage:.2f}MB, "
                  f"峰值内存={peak/1024/1024:.2f}MB")
        
        return False  # 不处理异常

def get_system_stats() -> Dict[str, Any]:
    """获取系统统计信息"""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    
    return {
        'cpu_percent': psutil.cpu_percent(),
        'memory_rss_mb': memory_info.rss / 1024 / 1024,
        'memory_vms_mb': memory_info.vms / 1024 / 1024,
        'thread_count': process.num_threads(),
        'open_files': len(process.open_files()),
        'connections': len(process.connections())
    }

def optimize_memory_usage():
    """优化内存使用"""
    import gc
    gc.collect()  # 强制垃圾回收
    
    # 清理可能的大对象缓存
    cleared = gc.collect()
    logger.debug(f"内存优化: 清理了 {cleared} 个对象")
    
    return cleared