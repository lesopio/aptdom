"""
配置管理模块
负责管理API密钥、模型选择等配置
"""

import os
import json
from pathlib import Path
from typing import Any, Dict, Optional

import logging
import time
from .logging_config import get_logger

logger = get_logger(__name__)

class Config:
    """配置管理类"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file
        self._config: Dict[str, Any] = {}
        self._config_hash: Optional[str] = None  # 用于缓存验证
        self._last_load_time: float = 0  # 最后加载时间
        
        # 默认配置
        self._default_config = {
            "ai_service": "ollama",
            "model": "llama2",
            "base_url": "http://localhost:11434",
            "api_key": "",
            "output_format": "docx",
            "enable_ocr": False,
            "tesseract_path": "",
            "verbose": False,
            "max_tokens": 2000,
            "temperature": 0.3
        }
        # 加载配置
        self._load_config()
    
    def _load_config(self, force: bool = False):
        """加载配置
        Args:
            force: 是否强制重新加载，忽略缓存
        """
        # 1. 加载默认配置
        self._config = self._default_config.copy()
        
        # 2. 加载环境变量
        self._load_from_env()
        
        # 3. 加载配置文件
        if self.config_file:
            self._load_from_file(self.config_file)
        else:
            # 尝试加载默认配置文件
            default_config_paths = [
                Path("config.json"),
                Path.home() / ".ppt_converter" / "config.json",
                Path(__file__).parent.parent / "config.json"
            ]
            
            for config_path in default_config_paths:
                if config_path.exists():
                    self._load_from_file(str(config_path))
                    break
        
        # 验证配置
        from .config_validator import validate_config
        is_valid, errors, warnings = validate_config(self._config)
        
        if not is_valid:
            for error in errors:
                logger.error(f"配置错误: {error}")
            raise ValueError("配置验证失败，请检查配置")
        
        for warning in warnings:
            logger.warning(f"配置警告: {warning}")
        
        import hashlib
        config_str = json.dumps(self._config, sort_keys=True)
        self._config_hash = hashlib.md5(config_str.encode()).hexdigest()
        self._last_load_time = time.time()
        
        logger.debug(f"配置加载完成: 使用缓存={not force}, 配置哈希={self._config_hash[:8]}")
    
    def _load_from_env(self):
        """从环境变量加载配置"""
        env_mapping = {
            "AI_SERVICE": "ai_service",
            "MODEL": "model",
            "BASE_URL": "base_url",
            "API_KEY": "api_key",
            "OUTPUT_FORMAT": "output_format",
            "ENABLE_OCR": "enable_ocr",
            "TESSERACT_PATH": "tesseract_path",
            "VERBOSE": "verbose",
            "MAX_TOKENS": "max_tokens",
            "TEMPERATURE": "temperature"
        }
        
        for env_key, config_key in env_mapping.items():
            env_value = os.getenv(env_key)
            if env_value is not None:
                # 类型转换
                if config_key in ["enable_ocr", "verbose"]:
                    self._config[config_key] = env_value.lower() in ["true", "1", "yes", "on"]
                elif config_key in ["max_tokens", "temperature"]:
                    self._config[config_key] = float(env_value) if "." in env_value else int(env_value)
                else:
                    self._config[config_key] = env_value
        
        # 特殊处理：从.env文件加载
        self._load_from_dotenv()
    
    def _load_from_dotenv(self):
        """从.env文件加载配置"""
        dotenv_paths = [
            Path(".env"),
            Path.home() / ".ppt_converter" / ".env"
        ]
        
        for dotenv_path in dotenv_paths:
            if dotenv_path.exists():
                try:
                    with open(dotenv_path, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if not line or line.startswith("#") or "=" not in line:
                                continue
                            
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"\'')
                            
                            if key in ["AI_SERVICE", "MODEL", "BASE_URL", "API_KEY", 
                                     "OUTPUT_FORMAT", "ENABLE_OCR", "TESSERACT_PATH"]:
                                config_key = key.lower()
                                if config_key == "enable_ocr":
                                    self._config[config_key] = value.lower() in ["true", "1", "yes", "on"]
                                else:
                                    self._config[config_key] = value
                    
                    logger.debug(f"从{dotenv_path}加载配置")
                    break
                except Exception as e:
                    logger.warning(f"加载.env文件失败 {dotenv_path}: {e}")
    
    def _load_from_file(self, config_file: str):
        """从配置文件加载"""
        config_path = Path(config_file)
        if not config_path.exists():
            logger.warning(f"配置文件不存在: {config_path}")
            return
        
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                file_config = json.load(f)
            
            # 更新配置
            self._config.update(file_config)
            logger.debug(f"从{config_path}加载配置")
            
        except Exception as e:
            logger.error(f"加载配置文件失败 {config_path}: {e}")
    
    def get(self, key: str, default: Any = None, force_reload: bool = False) -> Any:
        """获取配置值
        Args:
            key: 配置键
            default: 默认值
            force_reload: 是否强制重新加载配置
        Returns:
            配置值
        """
        if force_reload:
            self._load_config(force=True)
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        self._config[key] = value
    
    def save(self, config_file: Optional[str] = None):
        """保存配置到文件"""
        save_path = Path(config_file or self.config_file or "config.json")
        
        # 确保目录存在
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
            
            logger.info(f"配置已保存到: {save_path}")
            
        except Exception as e:
            logger.error(f"保存配置失败: {e}")
    
    def get_all(self, force_reload: bool = False) -> Dict[str, Any]:
        """获取所有配置
        Args:
            force_reload: 是否强制重新加载配置
        Returns:
            当前的配置副本
        """
        if force_reload:
            self._load_config(force=True)
        return self._config.copy()
    
    def print_config(self):
        """打印配置"""
        print("当前配置:")
        for key, value in self._config.items():
            # 隐藏敏感信息
            if key == "api_key" and value:
                value = "*" * len(value)
            print(f"  {key}: {value}")


# 全局配置实例
_config_instance = None


def get_config(config_file: Optional[str] = None) -> Config:
    """获取全局配置实例"""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_file)
    return _config_instance


# 便捷函数
def get(key: str, default: Any = None) -> Any:
    """便捷获取配置值"""
    return get_config().get(key, default)


def set(key: str, value: Any):
    """便捷设置配置值"""
    get_config().set(key, value)
