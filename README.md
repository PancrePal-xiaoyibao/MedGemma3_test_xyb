# MedGemma 医学AI工具套件

这是一个完整的MedGemma医学AI模型工具套件，包含模型下载、问答系统等功能，帮助你在本地环境中使用MedGemma模型进行医学问答。

## 🚀 主要功能

### 📥 模型下载工具
- ✅ **本地下载**: 下载模型到本地ModelScope缓存目录
- ✅ **移动硬盘下载**: 下载模型到指定的移动硬盘目录
- ✅ **多模型支持**: 支持 `medgemma-27b-text-it` 和 `medgemma-4b-it` 两个模型
- ✅ **断点续传**: 支持下载中断后继续
- ✅ **交互式选择**: 友好的用户界面
- ✅ **磁盘空间检查**: 自动检查可用空间

### 🤖 智能问答系统
- ✅ **自动问答**: 从Markdown文件读取问题，自动生成医学专业回答
- ✅ **批量处理**: 支持批量处理多个问题
- ✅ **答案标识**: 自动标记已处理的问题，避免重复
- ✅ **灵活配置**: 支持不同模型和量化选项
- ✅ **分离存储**: 支持问题和答案分别存储

## 🚀 快速开始

### 1. 安装依赖

```bash
# 使用 requirements.txt 安装所有依赖
pip install -r requirements.txt

# 或者手动安装核心依赖
pip install modelscope torch transformers accelerate bitsandbytes
```

### 2. 配置 HuggingFace Token

创建 `config.json` 文件：
```json
{
    "HF_TOKEN": "your_huggingface_token_here"
}
```

### 3. 下载模型

```bash
# 下载到本地
python model_download/download_medgemma_local.py

# 或下载到移动硬盘
python model_download/download_medgemma_to_sdcard.py
```

### 4. 开始问答

```bash
# 准备问题文件 question.md，然后运行
python medgemma_qa.py
```

## 配置 Hugging Face Token

### 方法1: 使用config.json文件（推荐）

在项目目录下创建 `config.json` 文件：

```json
HF_TOKEN = "your_huggingface_token_here"
```

或者使用标准JSON格式：

```json
{
  "HF_TOKEN": "your_huggingface_token_here"
}
```

### 方法2: 设置环境变量

```bash
# 在 ~/.zshrc 或 ~/.bash_profile 中添加
export HF_TOKEN="your_huggingface_token_here"

# 重新加载配置
source ~/.zshrc
```

### 方法3: 运行时输入

脚本运行时会提示输入Token（如果以上配置都未设置）

## 📖 使用方法

### 🔧 模型下载

#### 本地下载（推荐用于开发）

```bash
# 交互式运行
python model_download/download_medgemma_local.py

# 命令行参数
python model_download/download_medgemma_local.py medgemma-4b    # 下载 4B 模型
python model_download/download_medgemma_local.py medgemma-27b   # 下载 27B 模型
```

#### 移动硬盘下载（推荐用于存储）

```bash
# 下载到移动硬盘（自动下载两个模型）
python model_download/download_medgemma_to_sdcard.py
```

**注意**: 移动硬盘下载脚本会自动下载 4B-IT 和 27B-Text-IT 两个模型到 `/Volumes/win2 1/hub/models/` 目录。

### 🤖 问答系统使用

#### 基本使用

1. **准备问题文件** (`question.md`):
```markdown
Q1: 胰腺癌病人出现黄疸，检查确诊为胆管高位梗阻，应该以什么方式治疗？
A1: 

Q2: 糖尿病的主要症状有哪些？
A2: 
```

2. **运行问答系统**:
```bash
python medgemma_qa.py
```

3. **查看结果**: 答案会自动填入文件并标记 `[Gemma3 reply]`

#### 高级配置

详细的问答系统配置和使用方法请参考 [README_QA.md](README_QA.md)

## 下载目录

模型将被下载到以下目录：

```
/Users/qinxiaoqiang/.cache/modelscope/hub/models/google/
├── medgemma-27b-text-it/    # 27B模型文件
└── medgemma-4b-it/          # 4B模型文件
```

## ⚠️ 注意事项

### 💾 存储空间要求
- **medgemma-27b-text-it**: 约 54GB
- **medgemma-4b-it**: 约 9GB
- **总计**: 约 63GB（如果下载所有模型）
- 请确保有足够的磁盘空间，建议预留额外 10GB 空间

### 🌐 网络要求
- 需要稳定的网络连接
- 下载速度取决于网络带宽
- 建议在网络稳定时进行下载
- 支持断点续传，可以中断后继续

### 🔐 权限要求
- 确保对目标目录有写入权限
- 移动硬盘需要正确挂载到指定路径
- 如果遇到权限问题，可能需要使用 `sudo`

### 🔑 Token要求
- 必须有有效的 HuggingFace Token
- Token 需要有访问 MedGemma 模型的权限
- 需要先在 HuggingFace 上接受模型的使用条款

### 🖥️ 硬件要求（问答系统）
- **MedGemma 4B**: 至少 8GB GPU 内存（推荐）
- **MedGemma 27B**: 至少 16GB GPU 内存（需要量化）
- **CPU 运行**: 可能非常慢，不推荐
- 支持量化以减少内存使用

## 获取 Hugging Face Token

1. 访问 [Hugging Face Settings](https://huggingface.co/settings/tokens)
2. 点击 "New token"
3. 选择 "Read" 权限
4. 复制生成的Token

## 故障排除

### 常见错误

1. **Token错误**: 确保Token正确且有读取权限
2. **网络错误**: 检查网络连接，可以重新运行脚本（支持断点续传）
3. **空间不足**: 确保有足够的磁盘空间
4. **权限错误**: 确保已在Hugging Face网站同意模型使用条款

### 重新下载

如果下载中断或需要重新下载：

```bash
# 使用 --force 参数强制重新下载
python download_medgemma_local.py medgemma-27b --force
```

## 📁 文件说明

### 🔧 核心脚本
- **`medgemma_qa.py`**: MedGemma 问答系统主脚本
- **`model_download/download_medgemma_local.py`**: 本地模型下载脚本（交互式/命令行）
- **`model_download/download_medgemma_to_sdcard.py`**: 移动硬盘模型下载脚本
- **`quick_start_with_hugging_face.py`**: 快速开始脚本
- **`setup_environment.sh`**: 环境设置脚本

### ⚙️ 配置文件
- **`config.json`**: 配置文件（存储 HuggingFace Token）
- **`question.md`**: 问题文件（问答系统输入）
- **`question-answer.md`**: 问答文件（问答系统输出）

### 📚 文档文件
- **`README.md`**: 主要说明文档（本文件）
- **`README_QA.md`**: 问答系统详细文档
- **`requirements.txt`**: Python 依赖列表（如果存在）