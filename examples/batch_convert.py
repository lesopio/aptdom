"""
批量转换脚本
用于批量将PPT文件转换为Docx/Markdown格式
"""

import os
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import logging

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import main as ppt_converter_main


def setup_logging(verbose=False):
    """设置日志"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def convert_single_file(ppt_path, args):
    """转换单个文件"""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"开始转换: {ppt_path}")
        
        # 构建命令行参数
        cmd_args = [
            'ppt-converter',
            str(ppt_path),
            '--format', args.format,
            '--ai', args.ai,
            '--model', args.model
        ]
        
        if args.api_key:
            cmd_args.extend(['--api-key', args.api_key])
        
        if args.base_url:
            cmd_args.extend(['--base-url', args.base_url])
        
        if args.ocr:
            cmd_args.append('--ocr')
        
        if args.verbose:
            cmd_args.append('--verbose')
        
        # 保存原始sys.argv
        original_argv = sys.argv.copy()
        
        try:
            # 设置新的sys.argv
            sys.argv = cmd_args
            
            # 执行转换
            ppt_converter_main()
            
            logger.info(f"转换成功: {ppt_path}")
            return True, ppt_path, None
            
        finally:
            # 恢复sys.argv
            sys.argv = original_argv
            
    except Exception as e:
        logger.error(f"转换失败 {ppt_path}: {e}")
        return False, ppt_path, str(e)


def batch_convert(input_dir, output_format='docx', ai_service='ollama', model='llama2',
                 api_key=None, base_url=None, enable_ocr=False, max_workers=4, verbose=False):
    """
    批量转换PPT文件
    
    Args:
        input_dir: 输入目录
        output_format: 输出格式 (docx 或 markdown)
        ai_service: AI服务 (ollama 或 openai)
        model: 模型名称
        api_key: API密钥
        base_url: API基础URL
        enable_ocr: 是否启用OCR
        max_workers: 最大并发数
        verbose: 详细输出
    """
    setup_logging(verbose)
    logger = logging.getLogger(__name__)
    
    input_path = Path(input_dir)
    if not input_path.exists():
        logger.error(f"输入目录不存在: {input_path}")
        return
    
    # 查找PPT文件
    ppt_extensions = ['.ppt', '.pptx']
    ppt_files = []
    
    for ext in ppt_extensions:
        ppt_files.extend(input_path.rglob(f'*{ext}'))
        ppt_files.extend(input_path.rglob(f'*{ext.upper()}'))
    
    if not ppt_files:
        logger.warning(f"在目录中未找到PPT文件: {input_path}")
        return
    
    logger.info(f"找到 {len(ppt_files)} 个PPT文件")
    
    # 创建参数对象
    class Args:
        def __init__(self):
            self.format = output_format
            self.ai = ai_service
            self.model = model
            self.api_key = api_key
            self.base_url = base_url
            self.ocr = enable_ocr
            self.verbose = verbose
    
    args = Args()
    
    # 批量转换
    success_count = 0
    failure_count = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_file = {
            executor.submit(convert_single_file, ppt_file, args): ppt_file 
            for ppt_file in ppt_files
        }
        
        # 处理结果
        for future in as_completed(future_to_file):
            success, ppt_file, error = future.result()
            
            if success:
                success_count += 1
            else:
                failure_count += 1
                logger.error(f"转换失败 {ppt_file}: {error}")
    
    # 输出统计
    logger.info(f"批量转换完成!")
    logger.info(f"成功: {success_count}")
    logger.info(f"失败: {failure_count}")
    logger.info(f"总计: {len(ppt_files)}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="批量PPT转换器")
    
    parser.add_argument("input_dir", help="输入目录路径")
    parser.add_argument("--format", choices=["docx", "markdown"], default="docx",
                       help="输出格式 (默认: docx)")
    parser.add_argument("--ai", choices=["ollama", "openai"], default="ollama",
                       help="AI服务选择 (默认: ollama)")
    parser.add_argument("--model", default="llama2",
                       help="AI模型名称 (默认: llama2)")
    parser.add_argument("--api-key", help="API密钥 (可选)")
    parser.add_argument("--base-url", help="API基础URL (可选)")
    parser.add_argument("--ocr", action="store_true", 
                       help="启用OCR处理PPT中的图像内容")
    parser.add_argument("--workers", type=int, default=4,
                       help="最大并发数 (默认: 4)")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="详细输出")
    
    args = parser.parse_args()
    
    batch_convert(
        input_dir=args.input_dir,
        output_format=args.format,
        ai_service=args.ai,
        model=args.model,
        api_key=args.api_key,
        base_url=args.base_url,
        enable_ocr=args.ocr,
        max_workers=args.workers,
        verbose=args.verbose
    )


if __name__ == "__main__":
    main()
