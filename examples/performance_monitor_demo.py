"""
性能监控工具使用示例
"""
from pathlib import Path
from src.performance_utils import monitor_performance, PerformanceMonitor, get_system_stats
from src.logging_config import get_logger

logger = get_logger(__name__)

@monitor_performance
def process_large_file(file_path: Path):
    """模拟处理大文件的操作"""
    logger.info(f"开始处理文件: {file_path}")
    # 模拟耗时操作
    data = b" " * 1024 * 1024 * 100  # 100MB数据
    processed = data.upper()
    return len(processed)

def main():
    """主函数"""
    # 示例1: 使用装饰器监控函数性能
    file_size = process_large_file(Path("large_file.bin"))
    logger.info(f"处理完成，文件大小: {file_size/1024/1024:.2f}MB")
    
    # 示例2: 使用上下文管理器监控代码块性能
    with PerformanceMonitor("batch_processing"):
        results = []
        for i in range(5):
            results.append(i * i)
            # 模拟耗时操作
            _ = [x for x in range(1000000)]
    
    # 示例3: 获取系统统计信息
    stats = get_system_stats()
    logger.info(f"系统统计: CPU使用率={stats['cpu_percent']}%, 内存使用={stats['memory_rss_mb']:.2f}MB")

if __name__ == "__main__":
    main()