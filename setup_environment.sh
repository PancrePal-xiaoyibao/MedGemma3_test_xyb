#!/bin/bash

# MedGemma 模型下载环境设置脚本
# 适用于 macOS

echo "🚀 MedGemma 模型下载环境设置"
echo "================================"

# 检查 Python 版本
echo "\n📋 检查 Python 环境..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python3 未安装，请先安装 Python3"
    exit 1
fi

# 检查 pip
echo "\n📋 检查 pip..."
pip3 --version
if [ $? -ne 0 ]; then
    echo "❌ pip3 未安装，请先安装 pip3"
    exit 1
fi

# 安装依赖包
echo "\n📦 安装必要的 Python 包..."
pip3 install huggingface_hub transformers

if [ $? -eq 0 ]; then
    echo "✅ 依赖包安装成功"
else
    echo "❌ 依赖包安装失败"
    exit 1
fi

# 检查目标目录
echo "\n📁 检查目标目录..."
TARGET_DIR="/Users/qinxiaoqiang/.cache/modelscope/hub/models/google"
if [ ! -d "$TARGET_DIR" ]; then
    echo "📁 创建目标目录: $TARGET_DIR"
    mkdir -p "$TARGET_DIR"
    if [ $? -eq 0 ]; then
        echo "✅ 目录创建成功"
    else
        echo "❌ 目录创建失败"
        exit 1
    fi
else
    echo "✅ 目标目录已存在: $TARGET_DIR"
fi

# 检查环境变量
echo "\n🔑 检查 Hugging Face Token..."
if [ -z "$HF_TOKEN" ]; then
    echo "⚠️  环境变量 HF_TOKEN 未设置"
    echo "\n请选择设置方式:"
    echo "1. 现在设置 (仅本次会话有效)"
    echo "2. 添加到 shell 配置文件 (永久有效)"
    echo "3. 跳过 (运行时手动输入)"
    
    read -p "请选择 (1-3): " choice
    
    case $choice in
        1)
            read -p "请输入你的 Hugging Face Token: " token
            export HF_TOKEN="$token"
            echo "✅ Token 已设置 (仅本次会话有效)"
            ;;
        2)
            read -p "请输入你的 Hugging Face Token: " token
            
            # 检测使用的 shell
            if [ -n "$ZSH_VERSION" ]; then
                SHELL_CONFIG="$HOME/.zshrc"
            elif [ -n "$BASH_VERSION" ]; then
                SHELL_CONFIG="$HOME/.bash_profile"
            else
                SHELL_CONFIG="$HOME/.profile"
            fi
            
            echo "\n# Hugging Face Token for MedGemma" >> "$SHELL_CONFIG"
            echo "export HF_TOKEN=\"$token\"" >> "$SHELL_CONFIG"
            
            echo "✅ Token 已添加到 $SHELL_CONFIG"
            echo "请运行以下命令使配置生效:"
            echo "source $SHELL_CONFIG"
            ;;
        3)
            echo "⚠️  跳过 Token 设置，运行时需要手动输入"
            ;;
        *)
            echo "❌ 无效选择"
            exit 1
            ;;
    esac
else
    echo "✅ 环境变量 HF_TOKEN 已设置"
fi

# 检查磁盘空间
echo "\n💾 检查磁盘空间..."
AVAILABLE_SPACE=$(df -h "$TARGET_DIR" | awk 'NR==2 {print $4}' | sed 's/G//')
echo "可用空间: ${AVAILABLE_SPACE}GB"

if [ "${AVAILABLE_SPACE%.*}" -lt 60 ]; then
    echo "⚠️  警告: 可用空间可能不足"
    echo "   - medgemma-27b-text-it 需要约 50GB+"
    echo "   - medgemma-4b-it 需要约 8-10GB"
else
    echo "✅ 磁盘空间充足"
fi

echo "\n🎉 环境设置完成！"
echo "\n📋 下一步:"
echo "1. 确保已在 Hugging Face 网站同意 medgemma 模型的使用条款"
echo "2. 运行下载脚本: python3 download_medgemma_local.py"
echo "\n🔗 相关链接:"
echo "- Hugging Face Token: https://huggingface.co/settings/tokens"
echo "- MedGemma 27B: https://huggingface.co/google/medgemma-27b-text-it"
echo "- MedGemma 4B: https://huggingface.co/google/medgemma-4b-it"