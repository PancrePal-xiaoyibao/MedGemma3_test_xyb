#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MedGemma 问答系统
基于 MedGemma 模型从 question.md 中提取问题并生成回答
"""

import os
import sys
import re
import json
from typing import List, Tuple

# 导入必要的库
try:
    import torch
    from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    from huggingface_hub import get_token
except ImportError as e:
    print(f"缺少必要的依赖库: {e}")
    print("请运行: pip install torch transformers accelerate bitsandbytes")
    sys.exit(1)

class MedGemmaQA:
    def __init__(self, model_variant="4b-it", use_quantization=False, config_file="config.json"):
        """
        初始化 MedGemma 问答系统
        
        Args:
            model_variant: 模型变体 ("4b-it" 或 "27b-text-it")
            use_quantization: 是否使用量化（默认关闭，避免bitsandbytes依赖问题）
            config_file: 配置文件路径
        """
        self.model_variant = model_variant
        self.model_id = f"google/medgemma-{model_variant}"
        self.use_quantization = use_quantization
        self.config_file = config_file
        
        # 本地模型路径（优先使用）
        self.local_model_path = f"/Users/qinxiaoqiang/.cache/modelscope/hub/models/google/medgemma-{model_variant}"
        
        # 设置设备
        if torch.backends.mps.is_available():
            self.device = "mps"
            print("Device set to use mps")
        elif torch.cuda.is_available():
            self.device = "cuda"
            print("Device set to use cuda")
        else:
            self.device = "cpu"
            print("Device set to use cpu")
        
        # 设置模型加载参数
        self.model_kwargs = {
            "torch_dtype": torch.bfloat16,
            "trust_remote_code": True,
        }
        
        # 对于MPS，不使用device_map auto，手动设置设备
        if self.device != "mps":
            self.model_kwargs["device_map"] = "auto"
        
        # 只有在明确启用量化且bitsandbytes可用时才使用
        if use_quantization:
            try:
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.bfloat16,
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_quant_type="nf4"
                )
                self.model_kwargs["quantization_config"] = quantization_config
                print("✓ 启用4位量化")
            except Exception as e:
                print(f"⚠️ 量化配置失败，将使用标准加载: {e}")
                self.use_quantization = False
        
        # 初始化模型和分词器
        self.pipe = None
        self.model = None
        self.tokenizer = None
        
        # 设置 HuggingFace Token（仅在需要时）
        self._setup_hf_token()
        
    def _setup_hf_token(self):
        """设置 HuggingFace Token（仅在需要时）"""
        # 如果本地模型存在，则不需要强制设置Token
        if os.path.exists(self.local_model_path):
            print("✓ 检测到本地模型，跳过HF Token设置")
            return
        
        print("⚠️ 本地模型不存在，需要HF Token来下载模型")
        
        # 1. 尝试从 config.json 读取
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    
                # 尝试解析为 JSON
                try:
                    config = json.loads(content)
                    if "HF_TOKEN" in config:
                        os.environ["HF_TOKEN"] = config["HF_TOKEN"]
                        print(f"✓ 从 {self.config_file} 读取 HF_TOKEN")
                        return
                except json.JSONDecodeError:
                    # 尝试简单的键值对格式
                    for line in content.split('\n'):
                        if line.strip().startswith('HF_TOKEN'):
                            token = line.split('=', 1)[1].strip().strip('"\'')
                            os.environ["HF_TOKEN"] = token
                            print(f"✓ 从 {self.config_file} 读取 HF_TOKEN")
                            return
            except Exception as e:
                print(f"⚠️ 读取配置文件失败: {e}")
        
        # 2. 检查环境变量
        if os.environ.get("HF_TOKEN"):
            print("✓ 使用环境变量中的 HF_TOKEN")
            return
            
        # 3. 检查是否已登录
        try:
            if get_token() is not None:
                print("✓ 已登录 HuggingFace")
                return
        except:
            pass
            
        # 4. 提示用户输入
        print("\n需要 HuggingFace Token 来下载 MedGemma 模型")
        print("请访问 https://huggingface.co/settings/tokens 获取 Token")
        token = input("请输入您的 HuggingFace Token (或按回车跳过): ").strip()
        if token:
            os.environ["HF_TOKEN"] = token
        else:
            print("⚠️ 未提供 Token，如果本地模型不存在可能会失败")
    
    def load_model(self, use_pipeline=True):
        """加载模型，优先使用本地路径"""
        # 确定模型路径
        model_path = self.local_model_path if os.path.exists(self.local_model_path) else self.model_id
        
        if os.path.exists(self.local_model_path):
            print(f"✓ 使用本地模型: {self.local_model_path}")
        else:
            print(f"⚠️ 本地模型不存在，将从HuggingFace下载: {self.model_id}")
        
        print(f"正在加载模型: {model_path}")
        
        if use_pipeline:
            # 使用 pipeline API
            try:
                self.pipe = pipeline(
                    "text-generation",
                    model=model_path,
                    model_kwargs=self.model_kwargs,
                )
                self.pipe.model.generation_config.do_sample = False
                print("✓ 模型加载完成 (使用 pipeline)")
            except Exception as e:
                print(f"⚠️ Pipeline加载失败: {e}")
                print("尝试直接加载模型...")
                use_pipeline = False
        if not use_pipeline or not hasattr(self, 'pipe') or self.pipe is None:
            # 直接加载模型
            print("使用直接加载模式...")
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                **self.model_kwargs,
            )
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            
            # 对于MPS设备，手动移动模型
            if self.device == "mps":
                self.model = self.model.to(self.device)
                print(f"✓ 模型已移动到 {self.device} 设备")
            
            self.pipe = None  # 确保pipeline为None
            print("✓ 模型加载完成 (直接加载)")
    
    def generate_answer(self, question: str, max_new_tokens: int = 2500) -> str:
        """生成回答"""
        # 构建消息格式
        system_instruction = "你是一位专业的医学专家，请用中文回答医学问题。请详细、准确地回答问题，确保回答完整。"
        
        messages = [
            {
                "role": "system",
                "content": system_instruction
            },
            {
                "role": "user",
                "content": question
            }
        ]
        
        # 设置生成参数
        generation_config = {
            "max_new_tokens": max_new_tokens,
            "do_sample": True,
            "temperature": 0.7,
            "top_p": 0.9,
            "repetition_penalty": 1.1,
            "pad_token_id": self.tokenizer.eos_token_id if hasattr(self, 'tokenizer') else None
        }
        
        if self.pipe:
            # 使用 pipeline
            # 更新pipeline的生成配置
            if hasattr(self.pipe.model, 'generation_config'):
                self.pipe.model.generation_config.update(**generation_config)
            elif hasattr(self.pipe, 'generation_config'):
                self.pipe.generation_config.update(**generation_config)

            output = self.pipe(messages, **generation_config) # 使用新的生成配置
            response = output[0]["generated_text"][-1]["content"]
        else:
            # 直接使用模型
            inputs = self.tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=True,
                tokenize=True,
                return_dict=True,
                return_tensors="pt",
            )
            
            # 确保输入在正确的设备上
            if hasattr(self.model, 'device'):
                inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
            else:
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            input_len = inputs["input_ids"].shape[-1]
            
            with torch.inference_mode():
                generation = self.model.generate(
                    **inputs, 
                    **generation_config  # 使用新的生成配置
                )
                generation = generation[0][input_len:]
            
            response = self.tokenizer.decode(generation, skip_special_tokens=True)
        
        return response.strip()
    
    def parse_questions(self, file_path: str) -> List[Tuple[str, str]]:
        """解析问题文件（只读取问题）"""
        questions = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 使用正则表达式匹配问题（只提取问题部分）
            pattern = r'Q(\d+):\s*([^\n]+)'
            matches = re.findall(pattern, content, re.MULTILINE)
            
            for match in matches:
                q_num, question = match
                questions.append((q_num, question.strip()))
            
            return questions
            
        except FileNotFoundError:
            print(f"❌ 文件不存在: {file_path}")
            return []
        except Exception as e:
            print(f"❌ 解析文件失败: {e}")
            return []
    
    def check_existing_answer(self, qa_file_path: str, q_num: str) -> str:
        """检查Q-A文件中是否已有答案"""
        try:
            if not os.path.exists(qa_file_path):
                return ""
            
            with open(qa_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找对应问题的答案
            pattern = f'A{q_num}:\s*([^\n]*(?:\n(?!Q\d+:|A\d+:)[^\n]*)*)'
            match = re.search(pattern, content, re.MULTILINE)
            
            if match:
                answer = match.group(1).strip()
                # 如果答案不为空且不是占位符，返回答案
                if answer and answer != "[Gemma3 reply]" and "[Gemma3 reply]" not in answer:
                    return answer
            
            return ""
            
        except Exception as e:
            print(f"❌ 检查答案失败: {e}")
            return ""
    
    def write_answer_to_file(self, qa_file_path: str, q_num: str, question: str, answer: str):
        """将答案写入Q-A文件"""
        try:
            # 读取现有内容
            content = ""
            if os.path.exists(qa_file_path):
                with open(qa_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            # 构建新的Q-A条目
            qa_entry = f"Q{q_num}: {question}\nA{q_num}: {answer} [Gemma3 reply]\n\n"
            
            # 检查是否已存在该问题
            pattern = f'Q{q_num}:\s*[^\n]+\s*\nA{q_num}:\s*[^\n]*(?:\n(?!Q\d+:|A\d+:)[^\n]*)*'
            
            if re.search(pattern, content, re.MULTILINE):
                # 更新现有答案
                replacement = f'Q{q_num}: {question}\nA{q_num}: {answer} [Gemma3 reply]'
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            else:
                # 添加新的Q-A条目
                content += qa_entry
            
            # 写入文件
            with open(qa_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✓ 已将 Q{q_num} 的答案写入 {qa_file_path}")
            
        except Exception as e:
            print(f"❌ 写入答案失败: {e}")
    
    def process_questions(self, question_file: str = "question.md", qa_file: str = "question-answer.md"):
        """处理问题文件（新的两文件模式）"""
        print(f"\n开始处理问题文件: {question_file}")
        print(f"答案将写入文件: {qa_file}")
        
        # 解析问题（只读取问题）
        questions = self.parse_questions(question_file)
        
        if not questions:
            print("❌ 未找到问题")
            return
        
        print(f"找到 {len(questions)} 个问题")
        
        # 处理每个问题
        for q_num, question in questions:
            print(f"\n处理 Q{q_num}: {question[:50]}...")
            
            # 检查Q-A文件中是否已有答案
            existing_answer = self.check_existing_answer(qa_file, q_num)
            if existing_answer:
                print(f"Q{q_num} 已有答案，跳过")
                continue
            
            try:
                # 生成答案
                print("正在生成答案...")
                answer = self.generate_answer(question)
                
                # 写入Q-A文件
                self.write_answer_to_file(qa_file, q_num, question, answer)
                
                print(f"Q{q_num} 答案预览: {answer[:100]}...")
                
            except Exception as e:
                print(f"❌ 处理 Q{q_num} 时出错: {e}")
                continue
        
        print("\n✓ 所有问题处理完成")

def main():
    """主函数"""
    print("=== MedGemma 问答系统 ===")
    
    # 文件配置
    current_dir = os.path.dirname(os.path.abspath(__file__))
    question_file = os.path.join(current_dir, "question.md")  # 问题文件（只读）
    qa_file = os.path.join(current_dir, "question-answer.md")  # 问答文件（写入答案）
    
    # 检查问题文件是否存在
    if not os.path.exists(question_file):
        print(f"❌ 问题文件不存在: {question_file}")
        return
    
    print(f"📖 问题文件: {question_file}")
    print(f"📝 答案文件: {qa_file}")
    
    try:
        # 初始化系统
        qa_system = MedGemmaQA(
            model_variant="4b-it",  # 使用4B模型，适合Mac配置
            use_quantization=False  # 默认关闭量化，避免依赖问题
        )
        
        # 加载模型
        qa_system.load_model(use_pipeline=True)
        
        # 处理问题（使用新的两文件模式）
        qa_system.process_questions(question_file, qa_file)
        
    except KeyboardInterrupt:
        print("\n用户中断程序")
    except Exception as e:
        print(f"❌ 程序执行出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()