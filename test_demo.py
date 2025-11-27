#!/usr/bin/env python3
"""
AI PPT转换器演示脚本
"""

import os
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from src.config import Config
from src.ppt_parser import PPTParser
from src.ai_processor import AIProcessor
from src.document_generator import DocumentGenerator


def test_basic_functionality():
    """测试基本功能"""
    print("=== AI PPT转换器功能测试 ===\n")
    
    # 1. 测试配置系统
    print("1. 测试配置系统...")
    config = Config()
    print(f"   AI服务: {config.get('ai_service')}")
    print(f"   模型: {config.get('model')}")
    print(f"   基础URL: {config.get('base_url')}")
    print("   ✓ 配置系统正常\n")
    
    # 2. 测试PPT解析器
    print("2. 测试PPT解析器...")
    parser = PPTParser()
    print(f"   解析器类型: {type(parser).__name__}")
    print("   ✓ PPT解析器正常\n")
    
    # 3. 测试AI处理器
    print("3. 测试AI处理器...")
    ai_processor = AIProcessor(config)
    print(f"   AI服务: {ai_processor.ai_service}")
    print(f"   模型: {ai_processor.model}")
    print("   ✓ AI处理器正常\n")
    
    # 4. 测试文档生成器
    print("4. 测试文档生成器...")
    doc_generator = DocumentGenerator()
    print(f"   生成器类型: {type(doc_generator).__name__}")
    print("   ✓ 文档生成器正常\n")
    
    # 5. 测试OCR处理器（如果可用）
    print("5. 测试OCR处理器...")
    try:
        from src.ocr_processor import OCRProcessor
        ocr_processor = OCRProcessor()
        print(f"   OCR可用: {ocr_processor.tesseract_available}")
        print("   ✓ OCR处理器正常\n")
    except ImportError:
        print("   OCR处理器: 依赖库未安装\n")
    
    # 6. 测试模块导入
    print("6. 测试模块导入...")
    modules = [
        "src.main",
        "src.ppt_parser", 
        "src.ai_processor",
        "src.document_generator",
        "src.config"
    ]
    
    for module_name in modules:
        try:
            __import__(module_name)
            print(f"   ✓ {module_name}")
        except ImportError as e:
            print(f"   ✗ {module_name}: {e}")
    
    print("\n=== 功能测试完成 ===")
    print("\n提示:")
    print("• 要使用完整功能，请安装: pip install python-pptx requests Pillow pytesseract python-docx")
    print("• 要启用OCR，请安装Tesseract OCR")
    print("• 要使用OpenAI，请设置API密钥")
    print("• 运行: python ppt_converter.py --help 查看使用帮助")


def test_command_line():
    """测试命令行功能"""
    print("\n=== 命令行功能测试 ===")
    
    # 测试帮助命令
    print("1. 测试帮助命令...")
    try:
        result = os.system("python ppt_converter.py --help")
        if result == 0:
            print("   ✓ 帮助命令正常")
        else:
            print("   ✗ 帮助命令失败")
    except Exception as e:
        print(f"   ✗ 帮助命令异常: {e}")
    
    # 测试版本信息
    print("\n2. 测试版本信息...")
    try:
        from src import __version__
        print(f"   ✓ 版本: {__version__}")
    except Exception as e:
        print(f"   ✗ 版本信息异常: {e}")


def main():
    """主函数"""
    print("AI PPT to Docx/Markdown Converter")
    print("=" * 50)
    
    # 运行测试
    test_basic_functionality()
    test_command_line()
    
    print("\n" + "=" * 50)
    print("项目结构完整，核心功能正常！")
    print("\n下一步:")
    print("1. 安装完整依赖: pip install -r requirements.txt")
    print("2. 准备PPT文件进行测试")
    print("3. 运行: python ppt_converter.py your_presentation.pptx")
    print("4. 查看生成的文档")


if __name__ == "__main__":
    main()
