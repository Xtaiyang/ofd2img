# ofd2img

> 一个轻量级的 OFD/PDF 文档转图片 Python 库

[![PyPI](https://img.shields.io/pypi/v/ofd2img)](https://pypi.org/project/ofd2img/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

Forked from [easyofd](https://github.com/renoyuan/easyofd)，并在其基础上进行了大量改造。本项目遵循 Apache-2.0 许可证。

## 🛠️ 构建与开发

本项目推荐使用 [uv](https://github.com/astral-sh/uv) 进行包管理。

### 本地安装
```bash
uv pip install -e .
```

### 构建项目
```bash
uv build
```

### 发布到 PyPI
```bash
uv publish
```

---

## ✨ 功能特性(部分未实现)

- **多格式支持** — 支持 OFD 文档转换为 PDF 文档、PNG、JPG 图片
- **灵活分页** — 可指定文档的任意页面范围进行转换（单次最多 20 页）
- **长图合并** — 将多个文档页面合并输出为一张长图（最多 10 页）
- **跨平台** — 适用于 macOS、Windows 及 Linux
- **隐私安全** — 纯本地处理，文件不会上传至任何服务器

## 📦 安装

```bash
pip install ofd2img
```

## 🚀 快速开始

```python
from ofd2img import OFD

# 初始化
ofd = OFD("path/to/document.ofd")

# 将文档转为图片（默认转换前 20 页）
ofd.to_image(output_dir="./output")

# 指定页面范围
ofd.to_image(output_dir="./output", pages=[1, 3, 5])

# 指定输出格式
ofd.to_image(output_dir="./output", img_type="jpg")

# 合并多页为一张长图
ofd.to_long_image(output_path="./output/merged.png", pages=[1, 2, 3])
```

## 📖 使用说明

### 基本用法

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `output_dir` | 图片输出目录 | `"./output"` |
| `pages` | 需要转换的页码列表（从 1 开始） | 前 20 页 |
| `img_type` | 输出图片格式，支持 `png` / `jpg` | `"png"` |

### 转换 PDF 文档

```python
from ofd2img import OFD

ofd = OFD("path/to/document.pdf")
ofd.to_image(output_dir="./output")
```

### 输出长图

```python
from ofd2img import OFD

ofd = OFD("path/to/document.ofd")
ofd.to_long_image(output_path="./output/long_image.png", pages=[1, 2, 3, 4, 5])
```

## 📄 许可证

本项目遵循 [Apache-2.0](LICENSE) 许可证。
