"""
文档生成器测试
"""

import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.document_generator import DocumentGenerator
from src.ai_processor import ProcessedSlide


class TestDocumentGenerator(unittest.TestCase):
    """文档生成器测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.generator = DocumentGenerator()
        
        # 创建测试数据
        self.test_slides = [
            ProcessedSlide(
                slide_index=1,
                title="标题1",
                content="这是第一页的内容。\n\n包含多行文本。",
                summary="第一页摘要",
                key_points=["要点1", "要点2", "要点3"],
                tags=["标签1", "标签2"],
                metadata={
                    "ai_service": "ollama",
                    "model": "llama2",
                    "original_text": "原始文本1"
                }
            ),
            ProcessedSlide(
                slide_index=2,
                title="标题2",
                content="这是第二页的内容。",
                summary="第二页摘要",
                key_points=["要点A", "要点B"],
                tags=["标签A"],
                metadata={
                    "ai_service": "ollama",
                    "model": "llama2",
                    "original_text": "原始文本2"
                }
            )
        ]
        
        # 创建临时目录
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_dir = Path(self.temp_dir.name)
    
    def tearDown(self):
        """测试后清理"""
        self.temp_dir.cleanup()
    
    @patch('docx.Document')
    def test_generate_docx(self, mock_document):
        """测试生成Docx文档"""
        # 模拟Document对象
        mock_doc = MagicMock()
        mock_document.return_value = mock_doc
        
        # 执行测试
        output_path = self.output_dir / "test_output.docx"
        self.generator.generate_docx(self.test_slides, output_path)
        
        # 验证调用
        mock_document.assert_called_once()
        mock_doc.save.assert_called_once_with(str(output_path))
        
        # 验证添加了标题
        mock_doc.add_heading.assert_any_call("PPT转换文档", 0)
        
        # 验证添加了元信息
        mock_doc.add_heading.assert_any_call("文档信息", 1)
        
        # 验证添加了目录
        mock_doc.add_heading.assert_any_call("目录", 1)
        
        # 验证添加了幻灯片内容
        self.assertEqual(mock_doc.add_heading.call_count, 6)  # 标题 + 元信息 + 目录 + 2个幻灯片标题 + 2个摘要
        
        # 验证添加了分页符
        mock_doc.add_page_break.assert_called()
    
    def test_generate_markdown(self):
        """测试生成Markdown文档"""
        # 执行测试
        output_path = self.output_dir / "test_output.md"
        self.generator.generate_markdown(self.test_slides, output_path)
        
        # 验证文件存在
        self.assertTrue(output_path.exists())
        
        # 读取文件内容
        content = output_path.read_text(encoding="utf-8")
        
        # 验证内容
        self.assertIn("# PPT转换文档", content)
        self.assertIn("## 文档信息", content)
        self.assertIn("**生成时间**:", content)
        self.assertIn("**幻灯片数量**: 2", content)
        self.assertIn("**AI服务**: ollama", content)
        self.assertIn("**模型**: llama2", content)
        
        self.assertIn("## 目录", content)
        self.assertIn("1. [标题1](#slide-1)", content)
        self.assertIn("2. [标题2](#slide-2)", content)
        
        self.assertIn("## <a name=\"slide-1\"></a>1. 标题1", content)
        self.assertIn("### 摘要", content)
        self.assertIn("第一页摘要", content)
        self.assertIn("### 主要内容", content)
        self.assertIn("这是第一页的内容。", content)
        self.assertIn("### 关键点", content)
        self.assertIn("- 要点1", content)
        self.assertIn("- 要点2", content)
        self.assertIn("- 要点3", content)
        self.assertIn("### 标签", content)
        self.assertIn("标签1, 标签2", content)
        
        self.assertIn("## <a name=\"slide-2\"></a>2. 标题2", content)
        self.assertIn("第二页摘要", content)
        self.assertIn("这是第二页的内容。", content)
        self.assertIn("- 要点A", content)
        self.assertIn("- 要点B", content)
        self.assertIn("标签A", content)
        
        self.assertIn("---", content)  # 分隔符
    
    def test_add_formatted_text(self):
        """测试添加格式化文本"""
        # 模拟Document对象
        mock_doc = MagicMock()
        
        # 测试普通文本
        self.generator._add_formatted_text(mock_doc, "普通文本")
        mock_doc.add_paragraph.assert_called_with()
        mock_doc.add_paragraph.return_value.add_run.assert_called_with("普通文本")
        
        # 测试标题
        mock_doc.reset_mock()
        self.generator._add_formatted_text(mock_doc, "# 标题")
        mock_doc.add_heading.assert_called_with("标题", 1)
        
        # 测试项目符号
        mock_doc.reset_mock()
        self.generator._add_formatted_text(mock_doc, "- 项目符号")
        mock_doc.add_paragraph.assert_called_with("项目符号", style="List Bullet")
        
        # 测试编号列表
        mock_doc.reset_mock()
        self.generator._add_formatted_text(mock_doc, "1. 编号列表")
        mock_doc.add_paragraph.assert_called_with("编号列表", style="List Number")
        
        # 测试多行文本
        mock_doc.reset_mock()
        self.generator._add_formatted_text(mock_doc, "第一行\n\n第二行")
        self.assertEqual(mock_doc.add_paragraph.call_count, 2)
    
    def test_get_current_time(self):
        """测试获取当前时间"""
        time_str = self.generator._get_current_time()
        
        # 验证格式
        import re
        pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
        self.assertRegex(time_str, pattern)


if __name__ == "__main__":
    unittest.main()
