#!/usr/bin/env python3
"""
Markdown生成器模块
负责将PPT内容转换为Markdown文档
"""

import logging
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass

from ppt_parser import SlideContent

logger = logging.getLogger(__name__)


class MarkdownGenerator:
    """Markdown生成器类"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate(self, slides: List[SlideContent], output_path: Path) -> None:
        """
        生成Markdown文档
        
        Args:
            slides: 幻灯片内容列表
            output_path: 输出文件路径
        """
        self.logger.info(f"开始生成Markdown文档: {output_path}")
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                self._generate_markdown(slides, f)
            self.logger.info(f"成功生成Markdown文档: {output_path}")
        except Exception as e:
            self.logger.error(f"生成Markdown文档失败: {e}")
            raise
    
    def _generate_markdown(self, slides: List[SlideContent], file_handle) -> None:
        """生成Markdown内容"""
        # 添加标题
        file_handle.write("# PPT转换文档\n\n")
        
        # 处理每页幻灯片
        for i, slide in enumerate(slides, 1):
            # 添加幻灯片标题
            if slide.title:
                file_handle.write(f"## {slide.title}\n\n")
            
            # 添加文本内容
            if slide.text_content:
                file_handle.write(f"{slide.text_content}\n\n")
            
            # 添加项目符号
            for bullet in slide.bullet_points:
                file_handle.write(f"- {bullet}\n")
            
            if slide.bullet_points:
                file_handle.write("\n")
            
            # 添加表格
            for table_data in slide.tables:
                self._add_table_to_markdown(file_handle, table_data)
            
            # 添加图片信息
            if slide.images:
                file_handle.write("### 图片\n\n")
                for img in slide.images:
                    file_handle.write(f"- 图片: {img['name']} (尺寸: {img['width']}x{img['height']})\n")
                file_handle.write("\n")
            
            # 添加备注
            if slide.notes:
                file_handle.write("### 备注\n\n")
                file_handle.write(f"{slide.notes}\n\n")
            
            # 添加分隔符（最后一页除外）
            if i < len(slides):
                file_handle.write("---\n\n")
    
    def _add_table_to_markdown(self, file_handle, table_data: Dict[str, Any]) -> None:
        """添加表格到Markdown"""
        if not table_data["data"]:
            return
        
        # 添加表格标题
        file_handle.write("### 表格\n\n")
        
        # 添加表头
        headers = table_data["data"][0]
        file_handle.write("| " + " | ".join(headers) + " |\n")
        file_handle.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
        
        # 添加表格内容
        for row_data in table_data["data"][1:]:
            file_handle.write("| " + " | ".join(row_data) + " |\n")
        
        file_handle.write("\n")
