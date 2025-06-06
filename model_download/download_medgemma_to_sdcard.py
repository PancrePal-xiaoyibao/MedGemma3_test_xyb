#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MedGemma模型下载脚本
将MedGemma模型下载到移动硬盘指定目录
"""

import os
from modelscope import snapshot_download

def download_medgemma_models():
    """
    下载MedGemma模型到移动硬盘
    """
    # 目标目录：移动硬盘的modelscope目录
    target_dir = "/Volumes/win2 1/hub/models/"
    
    # 确保目标目录存在
    os.makedirs(target_dir, exist_ok=True)
    print(f"📁 目标目录: {target_dir}")
    
    # 模型列表
    models = [
        {
            "name": "MedGemma-4B-IT",
            "model_id": "google/medgemma-4b-it",
            "description": "4B参数指令调优版本"
        },
        {
            "name": "MedGemma-27B-Text-IT", 
            "model_id": "google/medgemma-27b-text-it",
            "description": "27B参数文本指令调优版本"
        }
    ]
    
    print("=== MedGemma模型下载器 ===")
    print(f"将下载 {len(models)} 个模型到移动硬盘")
    print()
    
    # 逐个下载模型
    for i, model in enumerate(models, 1):
        print(f"[{i}/{len(models)}] 开始下载: {model['name']}")
        print(f"📝 描述: {model['description']}")
        print(f"🔗 模型ID: {model['model_id']}")
        
        try:
            # 下载模型到指定目录
            model_dir = snapshot_download(
                model['model_id'],
                cache_dir=target_dir,  # 指定缓存目录为移动硬盘
                revision='master'  # 使用最新版本
            )
            
            print(f"✅ {model['name']} 下载完成")
            print(f"📂 保存位置: {model_dir}")
            
            # 显示下载的文件大小
            if os.path.exists(model_dir):
                total_size = get_directory_size(model_dir)
                print(f"💾 模型大小: {format_size(total_size)}")
            
        except Exception as e:
            print(f"❌ {model['name']} 下载失败: {str(e)}")
            continue
        
        print("-" * 50)
    
    print("🎉 所有模型下载任务完成！")
    print(f"📁 模型保存在: {target_dir}")

def get_directory_size(directory):
    """
    计算目录大小
    """
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
    except Exception as e:
        print(f"计算目录大小时出错: {e}")
    return total_size

def format_size(size_bytes):
    """
    格式化文件大小显示
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def check_disk_space(target_dir):
    """
    检查磁盘空间
    """
    try:
        import shutil
        total, used, free = shutil.disk_usage(target_dir)
        print(f"💽 磁盘空间信息:")
        print(f"   总容量: {format_size(total)}")
        print(f"   已使用: {format_size(used)}")
        print(f"   可用空间: {format_size(free)}")
        
        # 估算需要的空间（27B模型约50GB，4B模型约8GB）
        estimated_need = 60 * 1024 * 1024 * 1024  # 60GB估算
        if free < estimated_need:
            print(f"⚠️  警告: 可用空间可能不足，建议至少有60GB空间")
        else:
            print(f"✅ 磁盘空间充足")
        print()
    except Exception as e:
        print(f"检查磁盘空间时出错: {e}")

if __name__ == "__main__":
    print("🚀 启动MedGemma模型下载器")
    
    # 检查目标目录
    target_dir = "/Volumes/win2 1/hub/models"
    if not os.path.exists("/Volumes/win2 1/hub/models"):
        print("❌ 错误: 找不到移动硬盘挂载点 /Volumes/win2 1/hub/models")
        print("请确保移动硬盘已正确挂载到 /Volumes/win2 1/hub/models目录")
        exit(1)
    
    # 检查磁盘空间
    check_disk_space(target_dir)
    
    # 开始下载
    try:
        download_medgemma_models()
    except KeyboardInterrupt:
        print("\n⏹️  用户中断下载")
    except Exception as e:
        print(f"❌ 下载过程中出现错误: {e}")
        import traceback
        traceback.print_exc()