#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MedGemma模型本地下载脚本
适用于Mac本地环境，下载模型到指定的ModelScope缓存目录

使用前请确保：
1. 已安装必要的Python包：pip install huggingface_hub transformers
2. 已设置环境变量 HF_TOKEN 或在脚本中直接配置
3. 已在Hugging Face网站同意medgemma模型的使用条款
"""

import os
import sys
import json
from pathlib import Path
from huggingface_hub import snapshot_download, login

# ===================================================================
# 配置部分
# ===================================================================

# 模型配置 - 可以下载的两个模型
MODELS = {
    "medgemma-27b": "google/medgemma-27b-text-it",
    "medgemma-4b": "google/medgemma-4b-it"
}

# 本地保存目录配置
BASE_CACHE_DIR = "/Users/qinxiaoqiang/.cache/modelscope/hub/models/google"

# ===================================================================
# 辅助函数
# ===================================================================

def get_hf_token():
    """获取Hugging Face Token"""
    # 方法1: 从config.json文件获取
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                # 处理简单的键值对格式: HF_TOKEN = "value"
                if '=' in content:
                    for line in content.split('\n'):
                        line = line.strip()
                        if line.startswith('HF_TOKEN'):
                            token = line.split('=', 1)[1].strip().strip('"').strip("'")
                            if token:
                                print("✅ 从config.json文件获取到 HF_TOKEN")
                                return token
                # 处理JSON格式
                else:
                    config = json.loads(content)
                    token = config.get('HF_TOKEN')
                    if token:
                        print("✅ 从config.json文件获取到 HF_TOKEN")
                        return token
        except Exception as e:
            print(f"⚠️  读取config.json失败: {e}")
    
    # 方法2: 从环境变量获取
    token = os.getenv('HF_TOKEN')
    if token:
        print("✅ 从环境变量获取到 HF_TOKEN")
        return token
    
    # 方法3: 从用户输入获取
    print("\n⚠️  未找到HF_TOKEN配置")
    print("请选择配置方式:")
    print("1. 手动输入Token")
    print("2. 查看config.json配置说明")
    
    choice = input("请选择 (1-2): ").strip()
    
    if choice == '2':
        print("\n📋 config.json配置说明:")
        print("在项目目录下创建config.json文件，内容如下:")
        print('HF_TOKEN = "your_huggingface_token_here"')
        print("\n或者JSON格式:")
        print('{"HF_TOKEN": "your_huggingface_token_here"}')
        print("\n🔗 获取Token: https://huggingface.co/settings/tokens")
        sys.exit(0)
    
    print("\n请输入你的 Hugging Face Token:")
    print("(可以在 https://huggingface.co/settings/tokens 获取)")
    token = input("Token: ").strip()
    
    if not token:
        raise ValueError("必须提供有效的 Hugging Face Token")
    
    return token

def setup_hf_login():
    """设置Hugging Face登录"""
    try:
        token = get_hf_token()
        login(token=token)
        print("✅ 成功登录 Hugging Face")
        return True
    except Exception as e:
        print(f"❌ Hugging Face 登录失败: {e}")
        return False

def download_model(model_key, force_download=False):
    """下载指定的模型
    
    Args:
        model_key: 模型键名 ('medgemma-27b' 或 'medgemma-4b')
        force_download: 是否强制重新下载
    """
    if model_key not in MODELS:
        print(f"❌ 不支持的模型: {model_key}")
        print(f"支持的模型: {list(MODELS.keys())}")
        return False
    
    repo_id = MODELS[model_key]
    save_directory = os.path.join(BASE_CACHE_DIR, model_key.replace('-', '-').replace('medgemma-', 'medgemma-').replace('-text-it', '-text-it'))
    
    # 根据用户需求设置正确的目录名
    if model_key == "medgemma-27b":
        save_directory = os.path.join(BASE_CACHE_DIR, "medgemma-27b-text-it")
    elif model_key == "medgemma-4b":
        save_directory = os.path.join(BASE_CACHE_DIR, "medgemma-4b-it")
    
    # 检查目录是否已存在
    if os.path.exists(save_directory) and not force_download:
        print(f"\n📁 模型目录已存在: {save_directory}")
        print("如需重新下载，请使用 --force 参数")
        return True
    
    # 确保目标文件夹存在
    os.makedirs(save_directory, exist_ok=True)
    
    print(f"\n🚀 开始下载模型 {repo_id}")
    print(f"📍 保存路径: {save_directory}")
    print("⏳ 这个过程可能需要较长时间，请耐心等待...")
    
    try:
        snapshot_download(
            repo_id=repo_id,
            local_dir=save_directory,
            local_dir_use_symlinks=False,  # 直接下载文件，而不是链接
            resume_download=True  # 支持断点续传
        )
        
        print(f"\n🎉 模型 {model_key} 下载成功！")
        print(f"📁 保存位置: {save_directory}")
        
        # 显示下载的文件
        print("\n📋 下载的文件列表:")
        for root, dirs, files in os.walk(save_directory):
            level = root.replace(save_directory, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files[:10]:  # 只显示前10个文件
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                size_mb = file_size / (1024 * 1024)
                print(f"{subindent}{file} ({size_mb:.1f} MB)")
            if len(files) > 10:
                print(f"{subindent}... 还有 {len(files) - 10} 个文件")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 下载过程中出现错误: {e}")
        print("\n🔍 请检查以下事项:")
        print("1. 网络连接是否正常")
        print("2. 是否已在 Hugging Face 网站同意 medgemma 的使用条款")
        print("3. Hugging Face Token 是否正确且有读取权限")
        print("4. 本地磁盘空间是否充足 (27B模型约需50GB+，4B模型约需8-10GB)")
        return False

def main():
    """主函数"""
    print("🤖 MedGemma 模型本地下载工具")
    print("=" * 50)
    
    # 检查并安装依赖
    try:
        import huggingface_hub
        import transformers
    except ImportError as e:
        print(f"❌ 缺少必要的依赖包: {e}")
        print("请运行: pip install huggingface_hub transformers")
        sys.exit(1)
    
    # 登录 Hugging Face
    if not setup_hf_login():
        sys.exit(1)
    
    # 处理命令行参数
    force_download = '--force' in sys.argv
    
    if len(sys.argv) > 1 and sys.argv[1] in MODELS:
        # 下载指定模型
        model_key = sys.argv[1]
        success = download_model(model_key, force_download)
    else:
        # 交互式选择模型
        print("\n📋 可下载的模型:")
        for i, (key, repo) in enumerate(MODELS.items(), 1):
            print(f"{i}. {key} ({repo})")
        print("3. 下载所有模型")
        
        try:
            choice = input("\n请选择要下载的模型 (1-3): ").strip()
            
            if choice == '1':
                success = download_model('medgemma-27b', force_download)
            elif choice == '2':
                success = download_model('medgemma-4b', force_download)
            elif choice == '3':
                print("\n🚀 开始下载所有模型...")
                success1 = download_model('medgemma-27b', force_download)
                success2 = download_model('medgemma-4b', force_download)
                success = success1 and success2
            else:
                print("❌ 无效的选择")
                sys.exit(1)
                
        except KeyboardInterrupt:
            print("\n\n⚠️  用户取消操作")
            sys.exit(0)
    
    if success:
        print("\n✅ 所有操作完成！")
        print(f"📁 模型保存在: {BASE_CACHE_DIR}")
    else:
        print("\n❌ 操作失败")
        sys.exit(1)

if __name__ == "__main__":
    main()