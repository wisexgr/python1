import os
import base64
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import requests

# 配置日志
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("="*60)
print("正在启动服务...")
print("="*60)

# 加载环境变量
try:
    load_dotenv(override=True)
    api_key = os.getenv('ARK_API_KEY')
    if api_key:
        api_key = api_key.strip('"\'')
        os.environ['ARK_API_KEY'] = api_key
    
    print(f"当前目录: {os.getcwd()}")
    print(f".env 文件: {'存在' if os.path.exists('.env') else '不存在'}")
    print(f"API Key: {api_key[:10] if api_key else '未设置'}...")
    print(f"Model ID: {os.getenv('MODEL_ID')}")
except Exception as e:
    print(f"环境变量加载错误: {e}")

app = Flask(__name__, static_folder='public')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('public', path)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        logger.info("收到分析请求")
        
        # 1. 检查图片上传
        if 'images' not in request.files:
            return jsonify({'error': '请上传图片'}), 400
        
        images = request.files.getlist('images')
        if len(images) < 5:
            return jsonify({'error': '请至少上传5张图片'}), 400
        
        # 限制图片数量（最多6张）
        if len(images) > 6:
            images = images[:6]
            logger.info(f'限制到前{len(images)}张图片')
        
        # 2. 获取API Key
        api_key = os.getenv('ARK_API_KEY')
        if api_key:
            api_key = api_key.strip('"\'')
        
        if not api_key or api_key == 'your_api_key_here':
            return jsonify({'error': '请先配置 ARK_API_KEY'}), 500
        
        logger.info(f'使用 API Key: {api_key[:10]}...')
        
        # 3. 处理图片
        image_contents = []
        for idx, img in enumerate(images):
            try:
                img_data = img.read()
                # 限制大小为1MB
                if len(img_data) > 1 * 1024 * 1024:
                    logger.info(f'图片 {idx+1} 过大，跳过')
                    continue
                img_base64 = base64.b64encode(img_data).decode('utf-8')
                image_contents.append({
                    'type': 'image_url',
                    'image_url': {
                        'url': f'data:{img.content_type};base64,{img_base64}'
                    }
                })
                logger.info(f'图片 {idx+1} 处理成功')
            except Exception as e:
                logger.error(f'图片 {idx+1} 处理失败: {e}')
                continue
        
        if len(image_contents) < 5:
            return jsonify({'error': '有效图片不足5张'}), 400
        
        # 4. 准备请求内容
        prompt = """分析以下朋友圈截图，生成分析结果。用JSON格式返回：
{
  "character": {
    "personality": "性格特点",
    "interests": "兴趣爱好",
    "lifestyle": "生活习惯",
    "values": "价值观"
  },
  "suggestions": {
    "topics": ["话题1", "话题2", "话题3"],
    "dates": ["约会1", "约会2"],
    "tips": ["建议1", "建议2"],
    "howToImpress": "如何产生好感"
  }
}"""
        
        content = [{'type': 'text', 'text': prompt}] + image_contents
        
        # 5. 调用API
        model_id = os.getenv('MODEL_ID', 'doubao-seed-2-0-lite-260215')
        logger.info(f'调用 API，模型: {model_id}')
        
        try:
            response = requests.post(
                'https://ark.cn-beijing.volces.com/api/v3/responses',
                json={
                    'model': model_id,
                    'input': content
                },
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json',
                    'ark-beta-image-process': 'true'
                },
                timeout=180
            )
        except Exception as e:
            logger.error(f'API 请求失败: {e}')
            return jsonify({'error': f'API 请求失败: {str(e)}'}), 500
        
        logger.info(f'API 响应状态: {response.status_code}')
        
        if response.status_code != 200:
            logger.error(f'API 错误: {response.text}')
            return jsonify({'error': f'API 错误: {response.status_code}'}), 500
        
        # 6. 解析响应
        result = response.json()
        logger.info(f'响应: {str(result)[:500]}...')
        
        # 提取文本内容
        analysis_text = ''
        if 'output' in result:
            output = result['output']
            if isinstance(output, list) and len(output) > 0:
                for item in output:
                    if isinstance(item, dict) and 'summary' in item:
                        for s in item['summary']:
                            if s.get('type') == 'summary_text':
                                analysis_text = s.get('text', '')
                                break
                    if analysis_text:
                        break
            else:
                analysis_text = str(output)
        
        if not analysis_text:
            analysis_text = str(result)
        
        # 7. 尝试解析JSON，失败则使用原始内容
        try:
            json_match = analysis_text.find('{')
            if json_match != -1:
                analysis_result = json.loads(analysis_text[json_match:])
            else:
                analysis_result = json.loads(analysis_text)
        except Exception as e:
            logger.warning(f'JSON 解析失败，使用默认内容: {e}')
            analysis_result = {
                'character': {
                    'personality': '性格分析完成',
                    'interests': '查看详细内容',
                    'lifestyle': '',
                    'values': ''
                },
                'suggestions': {
                    'topics': ['深入了解', '分享日常', '规划活动'],
                    'dates': ['喝咖啡', '看电影', '散步'],
                    'tips': ['真诚沟通', '尊重对方', '耐心'],
                    'howToImpress': analysis_text[:500]
                }
            }
        
        logger.info('分析完成')
        return jsonify({'success': True, 'data': analysis_result})
        
    except Exception as e:
        logger.error(f'分析错误: {e}')
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'分析出错: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    print("="*60)
    print(f"服务启动成功: http://localhost:{port}")
    print("="*60)
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
