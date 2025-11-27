"""
AI处理器测试
"""

import unittest
from unittest.mock import patch, MagicMock
import json

from src.ai_processor import AIProcessor, ProcessedSlide
from src.config import Config


class TestAIProcessor(unittest.TestCase):
    """AI处理器测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.config = Config()
        self.config.set("ai_service", "ollama")
        self.config.set("model", "llama2")
        self.config.set("base_url", "http://localhost:11434")
        self.config.set("api_key", "")
        
        self.processor = AIProcessor(self.config)
        
        # 创建测试幻灯片数据
        self.test_slide = MagicMock()
        self.test_slide.slide_index = 1
        self.test_slide.title = "测试幻灯片"
        self.test_slide.text_content = "这是测试内容"
        self.test_slide.bullet_points = ["要点1", "要点2"]
        self.test_slide.tables = []
        self.test_slide.images = []
        self.test_slide.notes = "备注内容"
    
    def test_init(self):
        """测试初始化"""
        self.assertEqual(self.processor.ai_service, "ollama")
        self.assertEqual(self.processor.model, "llama2")
        self.assertEqual(self.processor.base_url, "http://localhost:11434")
        self.assertEqual(self.processor.api_key, "")
    
    def test_validate_config_ollama(self):
        """测试Ollama配置验证"""
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {"models": []}
            
            # 不应该抛出异常
            self.processor._validate_config()
    
    def test_validate_config_openai(self):
        """测试OpenAI配置验证"""
        self.config.set("ai_service", "openai")
        self.config.set("api_key", "test_key")
        self.processor = AIProcessor(self.config)
        
        # 不应该抛出异常
        self.processor._validate_config()
        
        # 测试缺少API密钥
        self.config.set("api_key", "")
        self.processor = AIProcessor(self.config)
        
        with self.assertLogs(level='WARNING') as log:
            self.processor._validate_config()
            self.assertIn("OpenAI服务需要API密钥", log.output[0])
    
    def test_build_prompt(self):
        """测试构建提示"""
        prompt = self.processor._build_prompt(self.test_slide)
        
        self.assertIn("测试幻灯片", prompt)
        self.assertIn("这是测试内容", prompt)
        self.assertIn("要点1", prompt)
        self.assertIn("要点2", prompt)
        self.assertIn("备注内容", prompt)
        self.assertIn("JSON格式", prompt)
    
    @patch('requests.post')
    def test_call_ollama_api(self, mock_post):
        """测试调用Ollama API"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response": '{"content": "处理后的内容", "summary": "摘要", "key_points": ["点1", "点2"], "tags": ["标签1"]}'
        }
        mock_post.return_value = mock_response
        
        result = self.processor._call_ollama_api("测试提示")
        
        self.assertEqual(result, '{"content": "处理后的内容", "summary": "摘要", "key_points": ["点1", "点2"], "tags": ["标签1"]}')
        mock_post.assert_called_once()
    
    @patch('requests.post')
    def test_call_openai_api(self, mock_post):
        """测试调用OpenAI API"""
        self.config.set("ai_service", "openai")
        self.config.set("api_key", "test_key")
        self.processor = AIProcessor(self.config)
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": '{"content": "处理后的内容", "summary": "摘要", "key_points": ["点1", "点2"], "tags": ["标签1"]}'
                    }
                }
            ]
        }
        mock_post.return_value = mock_response
        
        result = self.processor._call_openai_api("测试提示")
        
        self.assertEqual(result, '{"content": "处理后的内容", "summary": "摘要", "key_points": ["点1", "点2"], "tags": ["标签1"]}')
        mock_post.assert_called_once()
    
    def test_parse_ai_response_json(self):
        """测试解析JSON格式的AI响应"""
        ai_response = '{"content": "处理后的内容", "summary": "摘要", "key_points": ["点1", "点2"], "tags": ["标签1"]}'
        
        result = self.processor._parse_ai_response(self.test_slide, ai_response)
        
        self.assertIsInstance(result, ProcessedSlide)
        self.assertEqual(result.slide_index, 1)
        self.assertEqual(result.title, "测试幻灯片")
        self.assertEqual(result.content, "处理后的内容")
        self.assertEqual(result.summary, "摘要")
        self.assertEqual(result.key_points, ["点1", "点2"])
        self.assertEqual(result.tags, ["标签1"])
        self.assertEqual(result.metadata["ai_service"], "ollama")
        self.assertEqual(result.metadata["model"], "llama2")
    
    def test_parse_ai_response_text(self):
        """测试解析文本格式的AI响应"""
        ai_response = "处理后的内容\n\n摘要：这是一个摘要\n\n关键点：\n- 点1\n- 点2\n\n标签：标签1, 标签2"
        
        result = self.processor._parse_ai_response(self.test_slide, ai_response)
        
        self.assertIsInstance(result, ProcessedSlide)
        self.assertEqual(result.slide_index, 1)
        self.assertEqual(result.title, "测试幻灯片")
        self.assertEqual(result.content, ai_response)
        self.assertEqual(result.summary, "AI处理完成，但解析失败")
        self.assertEqual(result.key_points, ["要点1", "要点2"])  # 原始数据
        self.assertEqual(result.tags, [])
    
    def test_extract_json(self):
        """测试提取JSON"""
        text = """
        这是前面的文本
        {
            "content": "处理后的内容",
            "summary": "摘要",
            "key_points": ["点1", "点2"],
            "tags": ["标签1"]
        }
        这是后面的文本
        """
        
        result = self.processor._extract_json(text)
        
        expected = """{
            "content": "处理后的内容",
            "summary": "摘要",
            "key_points": ["点1", "点2"],
            "tags": ["标签1"]
        }"""
        
        self.assertEqual(result, expected)
    
    @patch.object(AIProcessor, '_call_ai_api')
    def test_process_slides(self, mock_call_ai):
        """测试处理幻灯片"""
        mock_call_ai.return_value = '{"content": "处理后的内容", "summary": "摘要", "key_points": ["点1", "点2"], "tags": ["标签1"]}'
        
        slides_data = [self.test_slide]
        result = self.processor.process_slides(slides_data)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].slide_index, 1)
        self.assertEqual(result[0].title, "测试幻灯片")
        self.assertEqual(result[0].content, "处理后的内容")
        self.assertEqual(result[0].summary, "摘要")
        self.assertEqual(result[0].key_points, ["点1", "点2"])
        self.assertEqual(result[0].tags, ["标签1"])
        
        mock_call_ai.assert_called_once()


if __name__ == "__main__":
    unittest.main()
