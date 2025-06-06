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

---
# 社区介绍

## 关于社区
#小胰宝 是一个病友自助开始的项目，23年创立，24年中开源发展，24年底捐献给天工开物基金会，25年升级为社区化，由基金会和社区管理委员会CMC管理，构建纯血版的AI类公益开源项目- #小X宝社区，积极推动跨社区合作，专业推动社区规范管理，目前生态人群180+。社区目的是推动AI技术和RAG应用的普及化，集合力量助力25+癌种患者，并延伸至280+罕见病领域，立足患者公益服务，通过技术+任务，有效减少医患信息差，推动患者/家属规范治疗，减低焦虑。目前已经推出了小胰宝助手，小肺宝助手，小萌宝助手，小粉宝助手，小胃宝，小妍宝，小飞侠助手（首个罕见病领域应用）等项目。<br>

## 了解社区

社区具备公益x开源双重属性,属于AI社区中的创新社区<br>
👀 了解社区, 可以点击 [社区介绍](https://hi.xiao-x-bao.com.cn) <br>
‼️ 了解更多志愿者的责任，点击 [志愿者FAQ](https://faq.xiao-x-bao.com.cn)<br>
❤️ 考虑好了，click "i am in", 点击加入我们 [加入页面](https://iamin.xiao-x-bao.com.cn)<br>
😊 社区任务全透明化，不仅开放阅读，也开放了创建，鼓励志愿者加入自己的梦想项目 [任务中心](https://task.xiaoyibao.com.cn)<br>
👌 首个贡献：您的辅导员，会和您一起沟通介绍，帮助您在第一周确定首个贡献计划 [First Good Issue](https://myfirst.xiao-x-bao.com.cn)<br>

欢迎体验demo: <br>
⭐️ 小胰宝3个版本：<br> - [科普版](https://chat.xiaoyibao.com.cn)<br>- [Pro版](https://pro.xiaoyibao.com.cn)<br> - [Deepseek版](https://deepseek.xiaoyibao.com.cn)<br>
⭐️ 小肺宝: [小肺宝](https://chat.xiaofeibao.com.cn)<br>
⭐️ 小萌宝: [小萌宝](https://pro.xiaomengbao.cn/)<br>
⭐️ 小粉宝：[小粉宝](https://xfb.xiaoyibao.com.cn) (后续会有独立域名)<br>
⭐️ 小胃宝: [科普版](https://chat.xiaoweibao.com.cn)<br>、[专业版](https://pro.xiaoweibao.com.cn) (首个社区合作项目)<br>

欢迎加入社区贡献项目：
👏 [小X宝社区"AI探宝计划"](https://wiki.xiao-x-bao.com.cn) - 为推广患者个人掌握智能体构建<br>
👏 [小X宝社区"Genie-x-Pal"提示词仓库](https://github.com/PancrePal-xiaoyibao/Genie-X-PAL-prompts-center) - 汇集有效的患者智能体提示词 <br>


👏 标准的github/gitcode上的代码和项目贡献 我们已经开源了3个项目仓库，包括：<br>
- [小胰宝](https://github.com/PancrePal-xiaoyibao/miniapp-uniapp)<br>
- [肿瘤患者心理助手提示词](https://github.com/hhx465453939/MedicRAG) <br>:一个将医学与大生命领域专业研究转化为面向实际问题AI提示词的开源项目，旨在建立基于临床需求的AI知识库智能体生产流程；通过自然语言引导与路径设计，帮助医学与生命科学背景研究者更快融入小胰宝AI社区，并更好地利用医学与生命科学背景实现对AI应用的有效监督约束
- [MinerU-xyb](https://github.com/PancrePal-xiaoyibao/miniapp-uniapp)<br>
- [fastgpt-on-wechat](https://github.com/hanfangyuan4396/fastgpt-on-wechat)<br>
- [Gemini-2.0病情demo](https://github.com/PancrePal-xiaoyibao/gemini2.0-xiaoyibao)<br>
- [DOW-GEWE优化Docker版](https://github.com/PancrePal-xiaoyibao/dow_gewe_optimized_docker)<br>
- [DOW-GEWE优化版本](https://github.com/PancrePal-xiaoyibao/dow-gewe-optimized)<br>
- [中国肿瘤临床试验查询](https://github.com/PancrePal-xiaoyibao/search_china_trials)<br>
- [Fastgpt xxx-bot插件](https://github.com/PancrePal-xiaoyibao/fastgpt_xiaoyibao_xxxbot)<br>
- [小x宝通用AI助手小程序](https://github.com/PancrePal-xiaoyibao/miniapp-uniapp)<br>
- [JWT weather xxx-bot插件](https://github.com/PancrePal-xiaoyibao/xxxbot-GetWeather)<br>
- 期待更多开源加入完善社区，提供开源能力；

👏 [小X宝社区"胰腺肿瘤并发症病友共创宝典"](https://bfz.xiao-x-bao.com.cn) - 开放病友共创的第一个标准wiki<br>
