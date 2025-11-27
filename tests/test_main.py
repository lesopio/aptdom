"""
主程序测试
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

from src.main import setup_logging, main


class TestMain(unittest.TestCase):
    """主程序测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 保存原始sys.argv
        self.original_argv = sys.argv.copy()
        
        # 创建测试文件
        self.test_dir = Path("tests/test_files")
        self.test_dir.mkdir(exist_ok=True)
        
        self.test_ppt = self.test_dir / "test.pptx"
        self.test_ppt.write_text("测试PPT文件")
        
        self.output_file = self.test_dir / "output.docx"
    
    def tearDown(self):
        """测试后清理"""
        # 恢复sys.argv
        sys.argv = self.original_argv
        
        # 清理测试文件
        if self.test_ppt.exists():
            self.test_ppt.unlink()
        
        if self.output_file.exists():
            self.output_file.unlink()
    
    def test_setup_logging_verbose(self):
        """测试详细日志设置"""
        with self.assertLogs(level='DEBUG') as log:
            setup_logging(verbose=True)
            logger = __import__('logging').getLogger(__name__)
            logger.debug("测试调试信息")
            self.assertIn("测试调试信息", log.output[0])
    
    def test_setup_logging_normal(self):
        """测试普通日志设置"""
        with self.assertLogs(level='INFO') as log:
            setup_logging(verbose=False)
            logger = __import__('logging').getLogger(__name__)
            logger.info("测试信息")
            self.assertIn("测试信息", log.output[0])
    
    @patch('src.main.PPTParser')
    @patch('src.main.AIProcessor')
    @patch('src.main.OCRProcessor')
    @patch('src.main.DocumentGenerator')
    @patch('src.main.Config')
    def test_main_success(self, mock_config, mock_doc_gen, mock_ocr, mock_ai, mock_ppt):
        """测试主程序成功执行"""
        # 模拟参数
        sys.argv = [
            'main.py',
            str(self.test_ppt),
            '--format', 'docx',
            '--ai', 'ollama',
            '--verbose'
        ]
        
        # 模拟配置
        mock_config_instance = MagicMock()
        mock_config.return_value = mock_config_instance
        
        # 模拟PPT解析器
        mock_ppt_instance = MagicMock()
        mock_ppt_instance.extract_text.return_value = ['slide1', 'slide2']
        mock_ppt.return_value = mock_ppt_instance
        
        # 模拟AI处理器
        mock_ai_instance = MagicMock()
        mock_ai_instance.process_slides.return_value = ['processed1', 'processed2']
        mock_ai.return_value = mock_ai_instance
        
        # 模拟OCR处理器
        mock_ocr_instance = MagicMock()
        mock_ocr_instance.process_slides.return_value = ['ocr1', 'ocr2']
        mock_ocr.return_value = mock_ocr_instance
        
        # 模拟文档生成器
        mock_doc_gen_instance = MagicMock()
        mock_doc_gen.return_value = mock_doc_gen_instance
        
        # 执行测试
        try:
            main()
        except SystemExit as e:
            self.assertEqual(e.code, 0)  # 成功退出
        
        # 验证调用
        mock_config.assert_called_once()
        mock_ppt.assert_called_once()
        mock_ppt_instance.extract_text.assert_called_once_with(self.test_ppt)
        
        # OCR应该被调用（因为--ocr参数）
        mock_ocr.assert_called_once()
        mock_ocr_instance.process_slides.assert_called_once_with(self.test_ppt, ['slide1', 'slide2'])
        
        mock_ai.assert_called_once()
        mock_ai_instance.process_slides.assert_called_once_with(['ocr1', 'ocr2'])
        
        mock_doc_gen.assert_called_once()
        mock_doc_gen_instance.generate_docx.assert_called_once_with(['processed1', 'processed2'], self.test_ppt.with_suffix('.docx'))
    
    @patch('src.main.PPTParser')
    @patch('src.main.Config')
    def test_main_file_not_found(self, mock_config, mock_ppt):
        """测试文件不存在的情况"""
        # 模拟参数
        sys.argv = [
            'main.py',
            'nonexistent.pptx'
        ]
        
        # 模拟配置
        mock_config_instance = MagicMock()
        mock_config.return_value = mock_config_instance
        
        # 执行测试
        with self.assertRaises(SystemExit) as cm:
            main()
        
        self.assertEqual(cm.exception.code, 1)  # 错误退出
    
    @patch('src.main.PPTParser')
    @patch('src.main.AIProcessor')
    @patch('src.main.Config')
    def test_main_ai_error(self, mock_config, mock_ai, mock_ppt):
        """测试AI处理错误的情况"""
        # 模拟参数
        sys.argv = [
            'main.py',
            str(self.test_ppt),
            '--verbose'
        ]
        
        # 模拟配置
        mock_config_instance = MagicMock()
        mock_config.return_value = mock_config_instance
        
        # 模拟PPT解析器
        mock_ppt_instance = MagicMock()
        mock_ppt_instance.extract_text.return_value = ['slide1']
        mock_ppt.return_value = mock_ppt_instance
        
        # 模拟AI处理器抛出异常
        mock_ai_instance = MagicMock()
        mock_ai_instance.process_slides.side_effect = Exception("AI处理失败")
        mock_ai.return_value = mock_ai_instance
        
        # 执行测试
        with self.assertRaises(SystemExit) as cm:
            main()
        
        self.assertEqual(cm.exception.code, 1)  # 错误退出
    
    @patch('src.main.PPTParser')
    @patch('src.main.AIProcessor')
    @patch('src.main.DocumentGenerator')
    @patch('src.main.Config')
    def test_main_markdown_format(self, mock_config, mock_doc_gen, mock_ai, mock_ppt):
        """测试Markdown格式输出"""
        # 模拟参数
        sys.argv = [
            'main.py',
            str(self.test_ppt),
            '--format', 'markdown'
        ]
        
        # 模拟配置
        mock_config_instance = MagicMock()
        mock_config.return_value = mock_config_instance
        
        # 模拟PPT解析器
        mock_ppt_instance = MagicMock()
        mock_ppt_instance.extract_text.return_value = ['slide1']
        mock_ppt.return_value = mock_ppt_instance
        
        # 模拟AI处理器
        mock_ai_instance = MagicMock()
        mock_ai_instance.process_slides.return_value = ['processed1']
        mock_ai.return_value = mock_ai_instance
        
        # 模拟文档生成器
        mock_doc_gen_instance = MagicMock()
        mock_doc_gen.return_value = mock_doc_gen_instance
        
        # 执行测试
        try:
            main()
        except SystemExit as e:
            self.assertEqual(e.code, 0)  # 成功退出
        
        # 验证调用
        mock_doc_gen_instance.generate_markdown.assert_called_once_with(['processed1'], self.test_ppt.with_suffix('.md'))
    
    @patch('src.main.PPTParser')
    @patch('src.main.AIProcessor')
    @patch('src.main.OCRProcessor')
    @patch('src.main.DocumentGenerator')
    @patch('src.main.Config')
    def test_main_no_ocr(self, mock_config, mock_doc_gen, mock_ocr, mock_ai, mock_ppt):
        """测试不启用OCR的情况"""
        # 模拟参数
        sys.argv = [
            'main.py',
            str(self.test_ppt)
        ]
        
        # 模拟配置
        mock_config_instance = MagicMock()
        mock_config.return_value = mock_config_instance
        
        # 模拟PPT解析器
        mock_ppt_instance = MagicMock()
        mock_ppt_instance.extract_text.return_value = ['slide1']
        mock_ppt.return_value = mock_ppt_instance
        
        # 模拟AI处理器
        mock_ai_instance = MagicMock()
        mock_ai_instance.process_slides.return_value = ['processed1']
        mock_ai.return_value = mock_ai_instance
        
        # 模拟文档生成器
        mock_doc_gen_instance = MagicMock()
        mock_doc_gen.return_value = mock_doc_gen_instance
        
        # 执行测试
        try:
            main()
        except SystemExit as e:
            self.assertEqual(e.code, 0)  # 成功退出
        
        # 验证OCR没有被调用
        mock_ocr.assert_not_called()
        
        # AI处理器应该直接处理PPT解析结果
        mock_ai_instance.process_slides.assert_called_once_with(['slide1'])


if __name__ == "__main__":
    unittest.main()
