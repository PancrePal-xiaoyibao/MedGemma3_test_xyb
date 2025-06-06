# MedGemma 问答系统使用说明

这个脚本基于 MedGemma 模型，可以自动从 `question.md` 文件中提取问题，调用模型生成回答，并将答案写回文件。

## 功能特点

- 🤖 **智能问答**: 基于 MedGemma 医学专用模型生成专业回答
- 📝 **自动处理**: 自动解析问题文件，生成答案并更新
- 🔧 **灵活配置**: 支持不同模型变体和量化选项
- 🔑 **多种认证**: 支持配置文件、环境变量、交互式输入等方式设置 Token
- 📋 **标识管理**: 自动添加 `[Gemma3 reply]` 标识，避免重复处理

## 环境要求

### Python 版本
- Python 3.8 或更高版本

### 硬件要求
- **MedGemma 4B**: 至少 8GB GPU 内存（推荐）
- **MedGemma 27B**: 至少 16GB GPU 内存（需要量化）
- CPU 运行: 可能非常慢，不推荐

### 依赖安装

```bash
# 安装基础依赖
pip install torch transformers accelerate bitsandbytes

# 或者使用 requirements.txt（如果提供）
pip install -r requirements.txt
```

## 配置 HuggingFace Token

### 方法1: 使用 config.json（推荐）

在脚本同目录下创建 `config.json` 文件：

```json
{
    "HF_TOKEN": "your_huggingface_token_here"
}
```

或者使用简单格式：
```
HF_TOKEN=your_huggingface_token_here
```

### 方法2: 环境变量

```bash
# 临时设置（当前会话）
export HF_TOKEN="your_huggingface_token_here"

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export HF_TOKEN="your_huggingface_token_here"' >> ~/.bashrc
source ~/.bashrc
```

### 方法3: 运行时输入

如果没有配置 Token，脚本会提示您输入。

### 获取 HuggingFace Token

1. 访问 [HuggingFace Settings](https://huggingface.co/settings/tokens)
2. 点击 "New token"
3. 选择 "Read" 权限
4. 复制生成的 Token
5. 访问 [MedGemma 模型页面](https://huggingface.co/google/medgemma-4b-it) 并接受使用条款

## 使用方法

### 1. 准备问题文件

确保 `question.md` 文件格式正确：

```markdown
Q1: 胰腺癌病人出现黄疸，检查确诊为胆管高位梗阻，应该以什么方式治疗？
A1: [Gemma3 reply]

Q2: 糖尿病的主要症状有哪些？
A2: 

Q3: 高血压的治疗原则是什么？
A3: 
```

### 2. 运行脚本

```bash
# 基本运行
python medgemma_qa.py

# 或者使其可执行
chmod +x medgemma_qa.py
./medgemma_qa.py
```

### 3. 查看结果

脚本会自动更新 `question.md` 文件，在每个答案后添加 `[Gemma3 reply]` 标识：

```markdown
Q1: 胰腺癌病人出现黄疸，检查确诊为胆管高位梗阻，应该以什么方式治疗？
A1: 胆管高位梗阻的治疗主要包括... [Gemma3 reply]
```

## 配置选项

### 模型变体

在 `medgemma_qa.py` 的 `main()` 函数中修改：

```python
qa_system = MedGemmaQA(
    model_variant="4b-it",      # 或 "27b-text-it"
    use_quantization=True       # 是否使用4位量化
)
```

### 生成参数

在 `generate_answer()` 方法调用时修改：

```python
answer = self.generate_answer(question, max_new_tokens=512)
```

## 工作流程

1. **初始化**: 设置模型参数和 HuggingFace Token
2. **加载模型**: 下载并加载 MedGemma 模型
3. **解析问题**: 从 `question.md` 中提取所有问题
4. **生成答案**: 对每个未回答的问题调用模型生成答案
5. **更新文件**: 将答案写回文件并添加标识
6. **跳过已处理**: 自动跳过已有 `[Gemma3 reply]` 标识的问题

## 注意事项

### 存储空间
- MedGemma 4B: 约 9GB
- MedGemma 27B: 约 54GB
- 确保有足够的磁盘空间

### 网络连接
- 首次运行需要下载模型
- 需要稳定的网络连接
- 下载可能需要较长时间

### 内存使用
- 使用量化可以显著减少内存使用
- 如果内存不足，尝试使用 4B 模型或启用量化

### 处理时间
- 每个问题的处理时间取决于硬件性能
- GPU 比 CPU 快得多
- 复杂问题可能需要更长时间

## 故障排除

### 常见错误

1. **Token 错误**
   ```
   HTTPError: 401 Client Error: Unauthorized
   ```
   - 检查 HuggingFace Token 是否正确
   - 确认已接受 MedGemma 模型的使用条款

2. **内存不足**
   ```
   CUDA out of memory
   ```
   - 启用量化: `use_quantization=True`
   - 使用较小的模型: `model_variant="4b-it"`
   - 关闭其他占用 GPU 的程序

3. **依赖缺失**
   ```
   ModuleNotFoundError: No module named 'transformers'
   ```
   - 安装缺失的依赖: `pip install transformers`

4. **文件格式错误**
   ```
   未找到问题
   ```
   - 检查 `question.md` 文件格式
   - 确保问题编号连续且格式正确

### 调试模式

如果遇到问题，可以在代码中添加调试信息：

```python
# 在 main() 函数开始处添加
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 扩展功能

### 自定义系统提示

修改 `generate_answer()` 方法中的 `system_instruction`：

```python
system_instruction = "你是一位专业的医学专家，请用中文详细回答医学问题，并提供相关的医学依据。"
```

### 批量处理多个文件

可以修改脚本来处理多个问题文件：

```python
question_files = ["question1.md", "question2.md", "question3.md"]
for file in question_files:
    qa_system.process_questions(file)
```

### 导出结果

可以添加功能将结果导出为其他格式（如 JSON、CSV 等）。

## 许可证

本脚本基于 MedGemma 模型，请遵守相关的许可证条款。MedGemma 模型由 Google 提供，受 Apache 2.0 许可证保护。

## 支持

如果遇到问题，请检查：
1. 硬件要求是否满足
2. 依赖是否正确安装
3. HuggingFace Token 是否有效
4. 网络连接是否稳定

更多信息请参考 [MedGemma 官方文档](https://developers.google.com/health-ai-developer-foundations/medgemma)。