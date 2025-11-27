"""
配置验证模块
负责验证配置的完整性和正确性
"""
from typing import Dict, Any, List, Tuple
import re
from urllib.parse import urlparse

from .logging_config import get_logger

logger = get_logger(__name__)

class ConfigValidator:
    """配置验证器类"""
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate_config(self, config: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """
        验证配置的完整性和正确性
        
        Args:
            config: 要验证的配置字典
            
        Returns:
            (是否有效, 错误列表, 警告列表)
        """
        self.errors.clear()
        self.warnings.clear()
        
        # 基本配置验证
        self._validate_basic_config(config)
        
        # AI服务特定验证
        self._validate_ai_config(config)
        
        # OCR配置验证
        self._validate_ocr_config(config)
        
        # 输出格式验证
        self._validate_output_config(config)
        
        return (len(self.errors) == 0, self.errors.copy(), self.warnings.copy())
    
    def _validate_basic_config(self, config: Dict[str, Any]):
        """验证基本配置"""
        required_fields = ['ai_service', 'model', 'output_format']
        
        for field in required_fields:
            if field not in config or not config[field]:
                self.errors.append(f"必需字段 '{field}' 未设置")
        
        # 验证布尔值字段
        boolean_fields = ['enable_ocr', 'verbose']
        for field in boolean_fields:
            if field in config and not isinstance(config[field], bool):
                self.warnings.append(f"字段 '{field}' 应该是布尔值类型")
        
        # 验证数值字段
        numeric_fields = ['max_tokens', 'temperature']
        for field in numeric_fields:
            if field in config:
                try:
                    float(config[field])
                except (ValueError, TypeError):
                    self.errors.append(f"字段 '{field}' 应该是数值类型")
    
    def _validate_ai_config(self, config: Dict[str, Any]):
        """验证AI服务配置"""
        ai_service = config.get('ai_service')
        
        if ai_service == 'openai':
            api_key = config.get('api_key')
            if not api_key:
                self.errors.append("OpenAI服务需要API密钥")
            elif not self._is_valid_api_key(api_key):
                self.warnings.append("API密钥格式可能无效")
            
            # 验证OpenAI模型
            model = config.get('model', '')
            if model and not model.startswith(('gpt-', 'davinci-', 'curie-', 'babbage-', 'ada-')):
                self.warnings.append(f"模型名称 '{model}' 可能不是有效的OpenAI模型")
        
        elif ai_service == 'ollama':
            base_url = config.get('base_url', '')
            if base_url and not self._is_valid_url(base_url):
                self.errors.append(f"无效的Ollama基础URL: {base_url}")
        
        elif ai_service and ai_service not in ['openai', 'ollama']:
            self.warnings.append(f"未知的AI服务: {ai_service}")
    
    def _validate_ocr_config(self, config: Dict[str, Any]):
        """验证OCR配置"""
        if config.get('enable_ocr'):
            tesseract_path = config.get('tesseract_path', '')
            if tesseract_path and not self._path_exists(tesseract_path):
                self.warnings.append(f"Tesseract路径不存在: {tesseract_path}")
    
    def _validate_output_config(self, config: Dict[str, Any]):
        """验证输出配置"""
        output_format = config.get('output_format')
        if output_format and output_format not in ['docx', 'markdown']:
            self.errors.append(f"不支持的输出格式: {output_format}")
    
    def _is_valid_api_key(self, api_key: str) -> bool:
        """验证API密钥格式"""
        # OpenAI API密钥通常以'sk-'开头，长度为51个字符
        if api_key.startswith('sk-') and len(api_key) == 51:
            return True
        
        # Ollama或其他服务可能有不同的格式
        if len(api_key) >= 10:  # 最小长度检查
            return True
        
        return False
    
    def _is_valid_url(self, url: str) -> bool:
        """验证URL格式"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def _path_exists(self, path: str) -> bool:
        """检查路径是否存在"""
        from pathlib import Path
        return Path(path).exists()

def validate_config(config: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
    """
    便捷函数：验证配置
    
    Args:
        config: 要验证的配置字典
        
    Returns:
        (是否有效, 错误列表, 警告列表)
    """
    validator = ConfigValidator()
    return validator.validate_config(config)

def print_validation_results(is_valid: bool, errors: List[str], warnings: List[str]):
    """打印验证结果"""
    if not is_valid:
        print("❌ 配置验证失败:")
        for error in errors:
            print(f"  错误: {error}")
    else:
        print("✅ 配置验证通过")
    
    if warnings:
        print("⚠️  警告:")
        for warning in warnings:
            print(f"  警告: {warning}")