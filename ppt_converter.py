#!/usr/bin/env python3
"""
AI PPT to Docx/Markdown Converter - 主入口点
"""

import sys
from pathlib import Path

# 添加当前目录到Python路径（不需要src子目录）
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from src.main import main

if __name__ == "__main__":
    main()
