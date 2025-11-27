"""
AI处理器模块
支持Ollama和OpenAI API，用于处理PPT内容
"""

import logging
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from .logging_config import get_logger

try:
    import requests
except ImportError:
    get_logger(__name__).warning("requests库未安装，API功能将受限")

logger = get_logger(__name__)


@dataclass
class ProcessedSlide:
    """处理后的幻灯片内容"""
    slide_index: int
    title: str
    content: str
    summary: str
    key_points: List[str]
    tags: List[str]
    metadata: Dict[str, Any]


class AIProcessor:
    """AI处理器类"""
    
    def __init__(self, config):
        self.config = config
        self.logger = get_logger(__name__)
        self.ai_service = config.get("ai_service", "ollama")
        self.model = config.get("model", "llama2" if self.ai_service == "ollama" else "gpt-3.5-turbo")
        self.api_key = config.get("api_key")
        self.base_url = config.get("base_url", 
                                  "http://localhost:11434" if self.ai_service == "ollama" 
                                  else "https://api.openai.com/v1")
        
        # 验证配置
        self._validate_config()
    
    def _validate_config(self):
        """验证AI配置"""
        if self.ai_service == "openai" and not self.api_key:
            self.logger.warning("OpenAI服务需要API密钥，请设置api_key")
        
        if self.ai_service == "ollama":
            # 检查Ollama服务是否可用
            try:
                response = requests.get(f"{self.base_url}/api/tags")
                if response.status_code != 200:
                    self.logger.warning(f"Ollama服务可能不可用: {response.status_code}")
            except Exception as e:
                self.logger.warning(f"无法连接到Ollama服务: {e}")
    
    def process_slides(self, slides_data: List[Any]) -> List[ProcessedSlide]:
        """
        处理幻灯片内容
        
        Args:
            slides_data: 原始幻灯片数据
            
        Returns:
            处理后的幻灯片数据
        """
        processed_slides = []
        
        for slide in slides_data:
            self.logger.debug(f"处理第{slide.slide_index}页幻灯片")
            
            # 构建提示
            prompt = self._build_prompt(slide)
            
            # 调用AI API
            try:
                ai_response = self._call_ai_api(prompt)
                
                # 解析响应
                processed_slide = self._parse_ai_response(slide, ai_response)
                processed_slides.append(processed_slide)
                
            except Exception as e:
                self.logger.error(f"处理第{slide.slide_index}页幻灯片时出错: {e}")
                # 创建基本处理结果
                processed_slide = ProcessedSlide(
                    slide_index=slide.slide_index,
                    title=slide.title,
                    content=slide.text_content,
                    summary=f"AI处理失败: {str(e)}",
                    key_points=slide.bullet_points,
                    tags=[],
                    metadata={"error": str(e)}
                )
                processed_slides.append(processed_slide)
        
        return processed_slides
    
    def _build_prompt(self, slide: Any) -> str:
        """构建AI提示"""
        prompt = f"""你是一个专业的PPT内容分析助手。请分析以下PPT幻灯片内容，并生成结构化的知识点。

幻灯片标题: {slide.title}

幻灯片文本内容:
{slide.text_content}

项目符号列表:
"""
        
        for i, point in enumerate(slide.bullet_points, 1):
            prompt += f"{i}. {point}\n"
        
        if slide.tables:
            prompt += "\n表格内容:\n"
            for table in slide.tables:
                prompt += f"表格 ({table['rows']}x{table['cols']}):\n"
                for row in table['data']:
                    prompt += " | ".join(row) + "\n"
        
        if slide.notes:
            prompt += f"\n备注内容:\n{slide.notes}"
        
        prompt += """
请按照以下JSON格式返回结果:
{
  "content": "整理后的完整内容，保持原意但更清晰",
  "summary": "100字以内的摘要",
  "key_points": ["关键点1", "关键点2", ...],
  "tags": ["标签1", "标签2", ...]
}

要求:
1. 内容要专业、准确、完整
2. 摘要要简洁明了
3. 关键点要突出核心信息
4. 标签要反映主题和领域
5. 保持原始信息的完整性
"""
        
        return prompt
    
    def _call_ai_api(self, prompt: str) -> str:
        """调用AI API"""
        if self.ai_service == "ollama":
            return self._call_ollama_api(prompt)
        else:
            return self._call_openai_api(prompt)
    
    def _call_ollama_api(self, prompt: str) -> str:
        """调用Ollama API"""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        self.logger.debug(f"调用Ollama API: {url}")
        response = requests.post(url, json=payload, timeout=60)
        
        if response.status_code != 200:
            raise Exception(f"Ollama API错误: {response.status_code} - {response.text}")
        
        result = response.json()
        return result.get("response", "")
    
    def _call_openai_api(self, prompt: str) -> str:
        """调用OpenAI API"""
        url = f"{self.base_url}/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "你是一个专业的PPT内容分析助手，擅长将PPT内容转换为结构化的知识点。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 2000
        }
        
        self.logger.debug(f"调用OpenAI API: {url}")
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code != 200:
            raise Exception(f"OpenAI API错误: {response.status_code} - {response.text}")
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    def _parse_ai_response(self, original_slide: Any, ai_response: str) -> ProcessedSlide:
        """解析AI响应"""
        try:
            # 尝试解析JSON
            json_str = self._extract_json(ai_response)
            data = json.loads(json_str)
            
            return ProcessedSlide(
                slide_index=original_slide.slide_index,
                title=original_slide.title,
                content=data.get("content", original_slide.text_content),
                summary=data.get("summary", ""),
                key_points=data.get("key_points", original_slide.bullet_points),
                tags=data.get("tags", []),
                metadata={
                    "original_text": original_slide.text_content,
                    "original_bullets": original_slide.bullet_points,
                    "ai_service": self.ai_service,
                    "model": self.model
                }
            )
        except Exception as e:
            self.logger.warning(f"解析AI响应失败: {e}")
            # 回退到基本处理
            return ProcessedSlide(
                slide_index=original_slide.slide_index,
                title=original_slide.title,
                content=ai_response if ai_response else original_slide.text_content,
                summary="AI处理完成，但解析失败",
                key_points=original_slide.bullet_points,
                tags=[],
                metadata={
                    "original_text": original_slide.text_content,
                    "ai_response": ai_response,
                    "parse_error": str(e)
                }
            )
    
    def _extract_json(self, text: str) -> str:
        """从文本中提取JSON部分"""
        # 查找JSON开始和结束
        start = text.find("{")
        end = text.rfind("}")
        
        if start != -1 and end != -1:
            return text[start:end+1]
        
        # 如果没有找到JSON，返回原始文本
        return text
