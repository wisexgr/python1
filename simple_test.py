#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('ARK_API_KEY')

print("="*60)
print("Volcano Ark API Test")
print("="*60)

if not api_key or api_key == 'your_api_key_here':
    print("Please set ARK_API_KEY in .env file")
    exit(1)

print(f"API Key: {api_key[:10]}...")
print()

test_url = "https://ark.cn-beijing.volces.com/api/v3/responses"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "ark-beta-image-process": "true"
}

payload = {
    "model": "doubao-seed-2-0-lite-260215",
    "input": "Hello, please reply with one sentence"
}

try:
    response = requests.post(test_url, json=payload, headers=headers, timeout=30)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("SUCCESS!")
        print(f"Response: {json.dumps(result, ensure_ascii=False)[:600]}")
    else:
        print(f"ERROR: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"Request error: {e}")

print()
print("="*60)
print("Setup Steps:")
print("="*60)
print("1. Get API Key: https://console.volcengine.com/ark/region:ark+cn-beijing/apikey")
print()
print("2. Deploy Model and Get Model ID:")
print("   - Go to Volcano Ark Console")
print("   - Enter 'Online Inference' service")
print("   - Select doubao-seed-2.0 model")
print("   - Create inference endpoint")
print("   - Copy the endpoint ID (like: ep-xxxxxxxxxxxxxx)")
print()
print("3. Update .env file:")
print("   Add: MODEL_ID=your-model-id")
print()
