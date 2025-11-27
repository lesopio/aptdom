"""
AI PPT to Docx/Markdown Converter - 安装脚本
"""

import os
from setuptools import setup, find_packages

# 读取README
def read_readme():
    here = os.path.abspath(os.path.dirname(__file__))
    readme_path = os.path.join(here, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# 读取版本
def read_version():
    here = os.path.abspath(os.path.dirname(__file__))
    version_path = os.path.join(here, "src", "__init__.py")
    if os.path.exists(version_path):
        with open(version_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"\'')
    return "0.1.0"

setup(
    name="ai_ppt_to_docx_markdown",
    version=read_version(),
    description="AI PPT to Docx/Markdown Converter - 将PPT文件转换为Docx或Markdown格式，支持AI处理和OCR功能",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="AI Assistant",
    author_email="",
    url="https://github.com/yourusername/ai-ppt-to-docx-markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "python-pptx>=0.6.21",
        "requests>=2.31.0",
        "Pillow>=10.0.0",
        "pytesseract>=0.3.10",
        "python-docx>=0.8.11",
        "markdown>=3.4.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.0",
        "psutil>=5.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "windows": [
            "comtypes>=1.2.0",
        ],
        "pdf": [
            "pdf2image>=1.16.3",
        ],
    },
    entry_points={
        "console_scripts": [
            "ppt-converter=main:main",
            "ai-ppt-converter=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Office Suites",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    keywords="ppt, docx, markdown, converter, ai, ocr, ollama, openai",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ai-ppt-to-docx-markdown/issues",
        "Source": "https://github.com/yourusername/ai-ppt-to-docx-markdown",
    },
)
