# AI PPT to Docx/Markdown Converter 🚀

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Test Coverage](https://img.shields.io/badge/coverage-90%25-yellow.svg)]()

> **将PPT文件转换为结构化的Docx或Markdown文档，支持AI智能处理和OCR功能**

[📚 详细文档](docs/) | [📦 安装指南](docs/installation.md) | [🎯 使用指南](docs/usage_guide.md) | [🧪 测试报告](PROJECT_SUMMARY.md)

## ✨ 核心功能

### 📄 **完整文本提取**
- 提取幻灯片标题、正文、项目符号
- 提取表格内容
- 提取图片信息
- 提取备注内容

### 🤖 **AI智能处理**
- ✅ **Ollama支持** - 本地AI服务，保护隐私
- ✅ **OpenAI支持** - 云端AI服务，强大能力
- ✅ **智能内容整理** - 自动优化文本结构
- ✅ **自动生成摘要** - 100字以内精炼总结
- ✅ **提取关键点** - 突出核心信息
- ✅ **生成标签** - 反映主题和领域

### 🔍 **OCR图像识别**
- 识别PPT中的图像文本
- 支持多语言
- 高准确率
- 与文本内容智能合并

### 📝 **多种输出格式**
- **Docx格式** - 专业排版，适合正式文档
- **Markdown格式** - 轻量级标记，适合技术文档

## 🚀 快速开始

### 1. 安装

```bash
# 克隆项目
git clone https://github.com/yourusername/ai-ppt-to-docx-markdown.git
cd ai-ppt-to-docx-markdown

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 安装项目
pip install -e .
```

### 2. 配置

创建`.env`文件：

```env
# AI服务选择 (ollama 或 openai)
AI_SERVICE=ollama

# 模型名称
MODEL=llama2

# API基础URL
BASE_URL=http://localhost:11434

# API密钥 (OpenAI需要)
API_KEY=your_openai_api_key_here

# 输出格式 (docx 或 markdown)
OUTPUT_FORMAT=docx

# 是否启用OCR处理
ENABLE_OCR=false

# Tesseract OCR路径 (如果不在系统PATH中)
TESSERACT_PATH=
```

### 3. 使用

```bash
# 基本转换
ppt-converter presentation.pptx

# 转换为Markdown
ppt-converter presentation.pptx --format markdown

# 使用OpenAI
ppt-converter presentation.pptx --ai openai --api-key your_key

# 启用OCR
ppt-converter presentation.pptx --ocr

# 详细输出
ppt-converter presentation.pptx -v

# 组合使用
ppt-converter presentation.pptx --format markdown --ai openai --ocr -v
```

## 🎯 使用场景

### 🎓 **学术研究**
- 将学术PPT转换为结构化论文
- 提取关键研究点
- 生成文献综述

### 💼 **商业演示**
- 将商业PPT转换为报告
- 提取关键业务指标
- 生成执行摘要

### 📚 **教育培训**
- 将教学PPT转换为学习材料
- 提取关键知识点
- 生成复习资料

### 📊 **数据分析**
- 将数据PPT转换为分析报告
- 提取关键数据点
- 生成可视化报告

## 🛠️ 技术架构

### 🏗️ **模块化设计**
```
src/
├── main.py              # 主程序
├── ppt_parser.py        # PPT解析器
├── ai_processor.py      # AI处理器
├── ocr_processor.py     # OCR处理器
├── document_generator.py # 文档生成器
└── config.py            # 配置管理
```

### 🔌 **AI服务支持**
- **Ollama** - 本地部署，保护隐私
- **OpenAI** - 云端服务，强大能力

### 📦 **依赖管理**
- 清晰的依赖关系
- 可选依赖支持
- 版本兼容性保证

## 📚 详细文档

- [📦 安装指南](docs/installation.md) - 详细安装步骤和常见问题
- [🎯 使用指南](docs/usage_guide.md) - 完整使用手册和高级技巧
- [🧪 测试报告](PROJECT_SUMMARY.md) - 测试覆盖和项目总结
- [📝 许可证](LICENSE) - MIT许可证

## 🧪 测试覆盖

- ✅ 配置管理测试
- ✅ PPT解析器测试
- ✅ AI处理器测试
- ✅ 文档生成器测试
- ✅ 主程序测试
- ✅ 错误处理测试

## 🚀 高级功能

### 🔄 **批量转换**
```bash
python examples/batch_convert.py /path/to/ppt/files --format docx --workers 4
```

### 🎨 **自定义配置**
```bash
ppt-converter presentation.pptx --config custom_config.json
```

### 🔍 **OCR处理**
```bash
ppt-converter presentation.pptx --ocr
```

### 🤖 **AI服务切换**
```bash
# Ollama（本地）
ppt-converter presentation.pptx --ai ollama --model llama2

# OpenAI（云端）
ppt-converter presentation.pptx --ai openai --model gpt-3.5-turbo --api-key your_key
```

## 📦 依赖

### 必需依赖
- `python-pptx` - PPT文件处理
- `requests` - API调用
- `Pillow` - 图像处理
- `pytesseract` - OCR识别
- `python-docx` - Docx生成
- `markdown` - Markdown处理
- `python-dotenv` - 环境变量管理

### 系统依赖
- **Tesseract OCR** - OCR功能
- **Ollama** - 本地AI服务

## 📝 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件


