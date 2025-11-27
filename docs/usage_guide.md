# 使用指南

## 快速开始

### 基本转换

```bash
# 转换为Docx（默认）
ppt-converter presentation.pptx

# 转换为Markdown
ppt-converter presentation.pptx --format markdown

# 指定输出文件
ppt-converter presentation.pptx -o output.docx
```

### 使用AI服务

```bash
# 使用Ollama（本地）
ppt-converter presentation.pptx --ai ollama --model llama2

# 使用OpenAI（云端）
ppt-converter presentation.pptx --ai openai --model gpt-3.5-turbo --api-key your_key
```

### 启用OCR

```bash
# 启用OCR处理PPT中的图像内容
ppt-converter presentation.pptx --ocr
```

## 命令行选项

### 必需参数

| 参数 | 说明 |
|------|------|
| `input` | 输入PPT文件路径 |

### 可选参数

| 参数 | 选项 | 默认值 | 说明 |
|------|------|--------|------|
| `-o, --output` | 文件路径 | 自动生成 | 输出文件路径 |
| `--format` | `docx`, `markdown` | `docx` | 输出格式 |
| `--ai` | `ollama`, `openai` | `ollama` | AI服务选择 |
| `--model` | 模型名称 | `llama2` | AI模型名称 |
| `--api-key` | API密钥 | 空 | API密钥 |
| `--base-url` | URL | `http://localhost:11434` | API基础URL |
| `--ocr` | 无 | `false` | 启用OCR处理 |
| `-v, --verbose` | 无 | `false` | 详细输出 |
| `--config` | 文件路径 | 空 | 配置文件路径 |

## 配置文件

### JSON格式

创建`config.json`文件：

```json
{
  "ai_service": "ollama",
  "model": "llama2",
  "base_url": "http://localhost:11434",
  "api_key": "your_api_key",
  "output_format": "docx",
  "enable_ocr": false,
  "tesseract_path": "",
  "verbose": false,
  "max_tokens": 2000,
  "temperature": 0.3
}
```

### 环境变量

创建`.env`文件：

```env
AI_SERVICE=ollama
MODEL=llama2
BASE_URL=http://localhost:11434
API_KEY=your_api_key
OUTPUT_FORMAT=docx
ENABLE_OCR=false
TESSERACT_PATH=
VERBOSE=false
MAX_TOKENS=2000
TEMPERATURE=0.3
```

## AI服务配置

### Ollama（本地）

#### 安装Ollama
1. 访问 [Ollama官网](https://ollama.ai) 下载并安装
2. 启动服务：
   ```bash
   ollama serve
   ```

#### 下载模型
```bash
# 下载Llama2模型
ollama pull llama2

# 下载Mistral模型
ollama pull mistral

# 下载CodeLlama模型
ollama pull codellama

# 列出已下载模型
ollama list
```

#### 配置
```env
AI_SERVICE=ollama
MODEL=llama2
BASE_URL=http://localhost:11434
```

### OpenAI（云端）

#### 获取API密钥
1. 访问 [OpenAI平台](https://platform.openai.com/api-keys)
2. 创建新的API密钥
3. 复制API密钥

#### 配置
```env
AI_SERVICE=openai
MODEL=gpt-3.5-turbo
BASE_URL=https://api.openai.com/v1
API_KEY=your_openai_api_key
```

#### 支持的模型
- `gpt-3.5-turbo` - 性价比高
- `gpt-4` - 更强大的模型
- `gpt-4-turbo` - 最新版本

## OCR配置

### Tesseract OCR

#### 安装
- **Windows**: 下载并安装 [Tesseract OCR for Windows](https://github.com/UB-Mannheim/tesseract/wiki)
- **macOS**: `brew install tesseract`
- **Linux**: `sudo apt-get install tesseract-ocr`

#### 语言包
```bash
# 安装中文语言包
# Windows: 在安装时选择中文语言包
# macOS: brew install tesseract-lang
# Linux: sudo apt-get install tesseract-ocr-chi-sim
```

#### 配置
```env
ENABLE_OCR=true
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe  # Windows示例
```

## 输出格式

### Docx格式

#### 特点
- 专业排版
- 支持复杂格式
- 适合正式文档
- 包含元信息

#### 结构
```
标题页
├── 文档信息
├── 目录
├── 幻灯片1
│   ├── 标题
│   ├── 摘要
│   ├── 主要内容
│   ├── 关键点
│   ├── 标签
│   └── 原始文本（可选）
├── 幻灯片2
│   └── ...
└── ...
```

### Markdown格式

#### 特点
- 轻量级标记语言
- 易于版本控制
- 适合技术文档
- 支持GitHub渲染

#### 结构
```markdown
# PPT转换文档

## 文档信息
- **生成时间**: 2024-01-01 12:00:00
- **幻灯片数量**: 5
- **AI服务**: ollama
- **模型**: llama2

## 目录
1. [标题1](#slide-1)
2. [标题2](#slide-2)

## <a name="slide-1"></a>1. 标题1

### 摘要
这是摘要内容

### 主要内容
这是主要内容

### 关键点
- 要点1
- 要点2

### 标签
标签1, 标签2

---

## <a name="slide-2"></a>2. 标题2
...
```

## 高级用法

### 批量转换

使用批量转换脚本：

```bash
# 转换目录中的所有PPT文件
python examples/batch_convert.py /path/to/ppt/files --format docx --workers 4

# 使用OpenAI批量转换
python examples/batch_convert.py /path/to/ppt/files --ai openai --api-key your_key --format markdown
```

### 自定义配置

创建自定义配置文件：

```bash
# 使用自定义配置
ppt-converter presentation.pptx --config custom_config.json

# 保存当前配置
ppt-converter --config save_config.json
```

### 管道处理

结合其他工具使用：

```bash
# 转换后使用pandoc进一步处理
ppt-converter presentation.pptx --format markdown
pandoc output.md -o output.pdf

# 转换后使用grep搜索内容
ppt-converter presentation.pptx --format markdown
grep -i "关键词" output.md
```

## 故障排除

### 常见问题

#### 1. 转换速度慢
- **原因**: AI处理需要时间
- **解决方案**: 
  - 使用更小的模型
  - 减少幻灯片数量
  - 使用本地Ollama服务

#### 2. OCR识别不准确
- **原因**: 图像质量差或语言包不匹配
- **解决方案**:
  - 提高图像质量
  - 安装正确的语言包
  - 调整Tesseract参数

#### 3. AI处理失败
- **原因**: API连接问题或模型错误
- **解决方案**:
  - 检查网络连接
  - 验证API密钥
  - 尝试不同的模型

#### 4. 内存不足
- **原因**: 处理大型PPT文件
- **解决方案**:
  - 增加系统内存
  - 分批处理幻灯片
  - 使用更小的模型

### 日志分析

查看日志文件`ppt_converter.log`：

```bash
# 查看最新日志
tail -f ppt_converter.log

# 搜索错误信息
grep -i "error" ppt_converter.log
```

### 调试模式

启用详细输出：

```bash
ppt-converter presentation.pptx -v
```

## 最佳实践

### 1. 文件准备
- 确保PPT文件可访问
- 检查文件完整性
- 备份原始文件

### 2. 性能优化
- 对于大型PPT，考虑分批处理
- 使用本地Ollama服务提高速度
- 关闭不必要的OCR功能

### 3. 质量控制
- 检查转换结果
- 验证关键点提取
- 调整AI参数

### 4. 安全考虑
- 保护API密钥
- 验证输入文件
- 定期更新依赖
```

## 示例工作流

### 学术PPT转换

```bash
# 转换学术PPT为Markdown
ppt-converter academic_presentation.pptx --format markdown --ai openai --model gpt-4 --ocr

# 使用pandoc生成PDF
pandoc output.md -o academic_paper.pdf --template=academic

# 使用git进行版本控制
git add output.md academic_paper.pdf
git commit -m "添加学术PPT转换结果"
```

### 商业演示转换

```bash
# 转换商业PPT为Docx
ppt-converter business_presentation.pptx --format docx --ai ollama --model mistral --ocr

# 使用Word进行进一步编辑
start output.docx  # Windows
# 或
open output.docx   # macOS
