import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import requests

app = Flask(__name__, static_folder='public')
CORS(app)

print("="*70)
print("启动简化版服务")
print("="*70)

# 加载配置
load_dotenv(override=True)
api_key = os.getenv('ARK_API_KEY')
if api_key:
    api_key = api_key.strip('"\'')

model_id = os.getenv('MODEL_ID', 'doubao-seed-2-0-lite-260215')
print(f"API Key: {api_key[:10] if api_key else '未设置'}...")
print(f"Model: {model_id}")

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/test.html')
def test_page():
    return send_from_directory('public', 'test.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('public', path)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    print("\n" + "="*70)
    print("📥 收到分析请求")
    print("="*70)
    
    try:
        # 1. 检查上传
        print("  检查文件...")
        if 'images' not in request.files:
            print("  ❌ 没有上传图片")
            return jsonify({'error': '请上传图片'}), 400
        
        images = request.files.getlist('images')
        print(f"  ✅ 收到 {len(images)} 张图片")
        
        if len(images) < 5:
            print(f"  ❌ 图片不够: {len(images)} < 5")
            return jsonify({'error': '请至少上传5张图片'}), 400
        
        # 2. 准备简单的分析（先不调用复杂API）
        print("  🎯 使用模拟分析结果")
        
        analysis_result = {
            'character': {
                'personality': '性格开朗，善于社交',
                'interests': '喜欢旅行、美食、拍照',
                'lifestyle': '生活规律，喜欢户外活动',
                'values': '重视家庭，追求生活品质'
            },
            'suggestions': {
                'topics': ['旅行经历', '美食分享', '周末计划', '生活日常'],
                'dates': ['咖啡探店', '公园散步', '看展览'],
                'tips': ['真诚沟通', '保持耐心', '尊重对方隐私'],
                'howToImpress': '通过共同兴趣建立连接，展现真诚的一面。从对方朋友圈内容寻找话题切入点。'
            }
        }
        
        print("  ✅ 分析完成，返回结果")
        print("="*70)
        return jsonify({'success': True, 'data': analysis_result})
        
    except Exception as e:
        print(f"  ❌ 异常: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    print("="*70)
    print(f"服务运行: http://localhost:{port}")
    print(f"测试页面: http://localhost:{port}/test.html")
    print("="*70)
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
