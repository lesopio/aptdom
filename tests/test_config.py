"""
配置模块测试
"""

import os
import tempfile
import unittest
from pathlib import Path

from src.config import Config, get_config


class TestConfig(unittest.TestCase):
    """配置测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时配置文件
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_file = Path(self.temp_dir.name) / "test_config.json"
        
        # 保存原始环境变量
        self.original_env = {}
        for key in ["AI_SERVICE", "MODEL", "BASE_URL", "API_KEY"]:
            self.original_env[key] = os.getenv(key)
    
    def tearDown(self):
        """测试后清理"""
        self.temp_dir.cleanup()
        
        # 恢复环境变量
        for key, value in self.original_env.items():
            if value is not None:
                os.environ[key] = value
            elif key in os.environ:
                del os.environ[key]
    
    def test_default_config(self):
        """测试默认配置"""
        config = Config()
        
        self.assertEqual(config.get("ai_service"), "ollama")
        self.assertEqual(config.get("model"), "llama2")
        self.assertEqual(config.get("base_url"), "http://localhost:11434")
        self.assertEqual(config.get("api_key"), "")
        self.assertEqual(config.get("output_format"), "docx")
        self.assertFalse(config.get("enable_ocr"))
        self.assertFalse(config.get("verbose"))
    
    def test_config_file(self):
        """测试配置文件加载"""
        # 创建测试配置文件
        config_data = {
            "ai_service": "openai",
            "model": "gpt-3.5-turbo",
            "base_url": "https://api.openai.com/v1",
            "api_key": "test_key",
            "output_format": "markdown",
            "enable_ocr": True,
            "verbose": True
        }
        
        with open(self.config_file, "w", encoding="utf-8") as f:
            import json
            json.dump(config_data, f)
        
        config = Config(str(self.config_file))
        
        self.assertEqual(config.get("ai_service"), "openai")
        self.assertEqual(config.get("model"), "gpt-3.5-turbo")
        self.assertEqual(config.get("base_url"), "https://api.openai.com/v1")
        self.assertEqual(config.get("api_key"), "test_key")
        self.assertEqual(config.get("output_format"), "markdown")
        self.assertTrue(config.get("enable_ocr"))
        self.assertTrue(config.get("verbose"))
    
    def test_env_variables(self):
        """测试环境变量加载"""
        os.environ["AI_SERVICE"] = "openai"
        os.environ["MODEL"] = "gpt-4"
        os.environ["BASE_URL"] = "https://custom.api.com"
        os.environ["API_KEY"] = "env_key"
        os.environ["ENABLE_OCR"] = "true"
        os.environ["VERBOSE"] = "true"
        
        config = Config()
        
        self.assertEqual(config.get("ai_service"), "openai")
        self.assertEqual(config.get("model"), "gpt-4")
        self.assertEqual(config.get("base_url"), "https://custom.api.com")
        self.assertEqual(config.get("api_key"), "env_key")
        self.assertTrue(config.get("enable_ocr"))
        self.assertTrue(config.get("verbose"))
    
    def test_config_override(self):
        """测试配置覆盖"""
        # 创建配置文件
        config_data = {
            "ai_service": "openai",
            "model": "gpt-3.5-turbo"
        }
        
        with open(self.config_file, "w", encoding="utf-8") as f:
            import json
            json.dump(config_data, f)
        
        # 设置环境变量
        os.environ["MODEL"] = "gpt-4"
        
        config = Config(str(self.config_file))
        
        # 环境变量应该覆盖配置文件
        self.assertEqual(config.get("ai_service"), "openai")  # 来自配置文件
        self.assertEqual(config.get("model"), "gpt-4")  # 来自环境变量
    
    def test_config_save(self):
        """测试配置保存"""
        config = Config()
        config.set("ai_service", "openai")
        config.set("model", "gpt-4")
        config.set("api_key", "test_key")
        
        config.save(str(self.config_file))
        
        # 重新加载配置
        new_config = Config(str(self.config_file))
        
        self.assertEqual(new_config.get("ai_service"), "openai")
        self.assertEqual(new_config.get("model"), "gpt-4")
        self.assertEqual(new_config.get("api_key"), "test_key")
    
    def test_get_config_singleton(self):
        """测试全局配置单例"""
        config1 = get_config()
        config2 = get_config()
        
        self.assertIs(config1, config2)
        
        config1.set("test_key", "test_value")
        self.assertEqual(config2.get("test_key"), "test_value")


if __name__ == "__main__":
    unittest.main()
