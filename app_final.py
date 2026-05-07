import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='public')
CORS(app)

print("="*80)
print("朋友圈分析助手 - 最终简化版")
print("="*80)
print("注意：本版本使用模拟分析，不调用外部API")
print("="*80)

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
    print("\n" + "="*80)
    print("收到分析请求")
    print("="*80)
    
    try:
        # 1. 检查图片上传
        print("  检查图片...")
        if 'images' not in request.files:
            print("  没有上传图片")
            return jsonify({'error': '请上传图片'}), 400
        
        images = request.files.getlist('images')
        print(f"  收到 {len(images)} 张图片")
        
        if len(images) < 5:
            print(f"  图片数量不足: {len(images)} < 5")
            return jsonify({'error': '请至少上传5张图片'}), 400
        
        # 2. 返回模拟分析结果（不调用外部API）
        print("  使用模拟分析结果")
        
        analysis_result = {
            'character': {
                'personality': '性格开朗，善于社交，喜欢交朋友',
                'interests': '喜欢旅行、美食、拍照、看电影',
                'lifestyle': '生活规律，喜欢户外活动，注重健康',
                'values': '重视家庭，追求生活品质，真诚待人'
            },
            'suggestions': {
                'topics': ['旅行经历分享', '美食探店推荐', '周末活动计划', '生活日常点滴'],
                'dates': ['特色咖啡店', '城市公园散步', '艺术展览', '电影约会'],
                'tips': ['真诚沟通', '保持耐心', '尊重对方隐私', '多聆听少说教'],
                'howToImpress': '通过共同兴趣建立连接，展现真诚的一面。从对方朋友圈内容寻找话题切入点，分享自己相关的经历，让对方觉得你们有共同点。'
            }
        }
        
        print("  ✅ 分析完成，返回结果")
        print("="*80)
        return jsonify({'success': True, 'data': analysis_result})
        
    except Exception as e:
        print(f"  服务器异常: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

if __name__ == '__main__':
    port = 5000  # 换端口避免缓存问题
    print("="*80)
    print(f"服务运行: http://localhost:{port}")
    print(f"测试页面: http://localhost:{port}/test.html")
    print("="*80)
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
