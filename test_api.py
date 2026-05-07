#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试火山方舟 API 连接
"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('ARK_API_KEY')

print("="*60)
print("火山方舟 API 测试工具")
print("="*60)
print(f"API Key: {api_key[:10] if api_key else '未设置'}{'...' if api_key and len(api_key) > 10 else ''}")
print()

if not api_key or api_key == 'your_api_key_here':
    print("❌ 请先在 .env 文件中配置 ARK_API_KEY")
    print("获取方法：")
    print("1. 访问 https://console.volcengine.com/ark/region:ark+cn-beijing/apikey")
    print("2. 创建 API Key")
    print("3. 将 Key 填入 .env 文件")
    exit(1)

# 测试 1: 简单文本请求
print("📝 测试 1: 简单文本请求")
print("-"*60)

test_url = "https://ark.cn-beijing.volces.com/api/v3/responses"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "ark-beta-image-process": "true"
}

payload = {
    "model": "doubao-seed-2-0-lite-260215",  # 先用这个测试，可能需要替换为你的模型ID
    "input": "你好，请用一句话回复"
}

try:
    response = requests.post(test_url, json=payload, headers=headers, timeout=30)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 连接成功！")
        print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)[:500]}")
    else:
        print(f"❌ 错误: {response.status_code}")
        print(f"响应: {response.text}")
        
except Exception as e:
    print(f"❌ 请求异常: {e}")

print()
print("="*60)
print("📋 完整配置步骤：")
print("="*60)
print("1. 获取 API Key")
print("   访问: https://console.volcengine.com/ark/region:ark+cn-beijing/apikey")
print()
print("2. 部署模型，获取模型 ID")
print("   步骤:")
print("   - 访问火山方舟控制台")
print("   - 进入 '在线推理' 服务")
print("   - 选择 doubao-seed-2-0 模型")
print("   - 创建推理接入点")
print("   - 复制生成的接入点 ID (格式类似: ep-xxxxxxxxxxxxxx)")
print()
print("3. 更新 .env 文件")
print("   添加: MODEL_ID=你的模型ID")
print()
print("="*60)
