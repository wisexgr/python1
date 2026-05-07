#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
from dotenv import load_dotenv

print("="*70)
print("完整API连接测试")
print("="*70)

# 1. 加载环境变量
load_dotenv(override=True)
api_key = os.getenv('ARK_API_KEY')
if api_key:
    api_key = api_key.strip('"\'')

model_id = os.getenv('MODEL_ID', 'doubao-seed-2-0-lite-260215')

print(f"\n1. 环境变量：")
print(f"   API Key: {api_key[:15] if api_key else '未设置'}...")
print(f"   Model ID: {model_id}")

if not api_key:
    print("\n❌ 错误：API Key 未设置！")
    exit(1)

# 2. 测试简单文本请求
print(f"\n2. 测试简单文本请求...")
test_url = "https://ark.cn-beijing.volces.com/api/v3/responses"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "ark-beta-image-process": "true"
}

payload = {
    "model": model_id,
    "input": "你好，请用一句话回复"
}

try:
    response = requests.post(test_url, json=payload, headers=headers, timeout=60)
    print(f"   状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 成功！响应: {str(result)[:300]}...")
    else:
        print(f"❌ 失败！响应: {response.text}")
        
except Exception as e:
    print(f"❌ 异常: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("测试完成")
print("="*70)
