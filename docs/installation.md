# 安装指南

## 系统要求

- Python 3.8 或更高版本
- 操作系统：Windows, macOS, Linux
- 内存：至少 4GB RAM（推荐 8GB+）
- 磁盘空间：至少 500MB 可用空间

## 安装步骤

### 1. 安装Python

确保已安装Python 3.8或更高版本：

```bash
# 检查Python版本
python --version
# 或
python3 --version
```

如果未安装Python，请从[Python官网](https://www.python.org/downloads/)下载并安装。

### 2. 安装Tesseract OCR（可选，但推荐）

OCR功能需要Tesseract OCR引擎：

#### Windows
1. 下载并安装 [Tesseract OCR for Windows](https://github.com/UB-Mannheim/tesseract/wiki)
2. 将安装路径添加到系统PATH环境变量
3. 验证安装：
   ```cmd
   tesseract --version
   ```

#### macOS
```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get install tesseract-ocr
```

### 3. 安装Ollama（可选）

如果使用本地AI服务，需要安装Ollama：

1. 访问 [Ollama官网](https://ollama.ai) 下载并安装
2. 启动Ollama服务：
   ```bash
   ollama serve
   ```
3. 下载模型：
   ```bash
   ollama pull llama2
   # 或其他模型
   ollama pull mistral
   ```

### 4. 安装项目依赖

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

### 5. 配置环境变量

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

# 详细输出
VERBOSE=false
```

### 6. 验证安装

```bash
# 检查是否安装成功
ppt-converter --help

# 运行测试
python -m pytest tests/
```

## 常见问题

### 1. Tesseract OCR未找到

**错误信息**：
```
pytesseract.pytesseract.TesseractNotFoundError: tesseract is not installed or it's not in your path
```

**解决方案**：
- 确保已正确安装Tesseract OCR
- 将Tesseract安装路径添加到系统PATH环境变量
- 或在`.env`文件中设置`TESSERACT_PATH`

### 2. python-pptx库安装失败

**错误信息**：
```
ERROR: Could not find a version that satisfies the requirement python-pptx
```

**解决方案**：
- 确保使用Python 3.8+
- 尝试使用pip的--upgrade选项：
  ```bash
  pip install --upgrade python-pptx
  ```

### 3. Ollama服务连接失败

**错误信息**：
```
requests.exceptions.ConnectionError: HTTPConnectionPool(host='localhost', port=11434)
```

**解决方案**：
- 确保Ollama服务正在运行：`ollama serve`
- 检查防火墙设置
- 验证BASE_URL配置

### 4. OpenAI API密钥无效

**错误信息**：
```
openai.AuthenticationError: Incorrect API key provided
```

**解决方案**：
- 检查API密钥是否正确
- 确保API密钥未过期
- 验证OpenAI账户余额

## 卸载

```bash
# 卸载项目
pip uninstall ai_ppt_to_docx_markdown

# 删除虚拟环境
rm -rf venv  # Linux/Mac
# 或
rmdir /s venv  # Windows
```

## 更新

```bash
# 更新项目
git pull origin main

# 更新依赖
pip install -r requirements.txt --upgrade

# 重新安装项目
pip install -e .
