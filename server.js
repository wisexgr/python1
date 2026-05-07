require('dotenv').config();
const express = require('express');
const cors = require('cors');
const multer = require('multer');
const axios = require('axios');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

const upload = multer({
  dest: 'uploads/',
  limits: { fileSize: 10 * 1024 * 1024 },
  fileFilter: (req, file, cb) => {
    const allowedTypes = /jpeg|jpg|png|gif|webp/;
    const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
    const mimetype = allowedTypes.test(file.mimetype);
    if (extname && mimetype) {
      return cb(null, true);
    }
    cb(new Error('只允许上传图片文件'));
  }
});

app.post('/api/analyze', upload.array('images', 20), async (req, res) => {
  try {
    if (!req.files || req.files.length < 5) {
      return res.status(400).json({ error: '请至少上传5张图片' });
    }

    const apiKey = process.env.ARK_API_KEY;
    if (!apiKey) {
      return res.status(500).json({ error: '服务器配置错误，请联系管理员' });
    }

    const imageDescriptions = [];
    for (const file of req.files) {
      const imageBase64 = fs.readFileSync(file.path, 'base64');
      const mimeType = file.mimetype;
      imageDescriptions.push({
        type: 'image_url',
        image_url: {
          url: `data:${mimeType};base64,${imageBase64}`
        }
      });
      fs.unlinkSync(file.path);
    }

    const prompt = `请分析以下朋友圈截图，从以下维度进行全面分析：

1. 【人物画像】
   - 性格特点分析
   - 兴趣爱好总结
   - 生活习惯描述
   - 价值观倾向

2. 【交友策略建议】
   - 推荐3-5个适合的聊天话题
   - 推荐2-3个约会地点或活动
   - 互动中的注意事项和禁忌
   - 如何让对方产生好感的具体建议

请用友好、温暖的语气，以JSON格式返回分析结果，格式如下：
{
  "character": {
    "personality": "性格特点描述",
    "interests": "兴趣爱好描述",
    "lifestyle": "生活习惯描述",
    "values": "价值观描述"
  },
  "suggestions": {
    "topics": ["话题1", "话题2", "话题3"],
    "dates": ["约会建议1", "约会建议2"],
    "tips": ["注意事项1", "注意事项2"],
    "howToImpress": "如何产生好感的建议"
  }
}

请确保返回的是纯粹的JSON格式，不要包含任何其他文字说明。`;

    const messages = [
      {
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          ...imageDescriptions
        ]
      }
    ];

    const response = await axios.post(
      'https://ark.cn-beijing.volces.com/api/v3/chat/completions',
      {
        model: 'doubao-seed-2-0-lite-260215',
        messages: messages,
        temperature: 0.7,
        max_tokens: 2000
      },
      {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json'
        }
      }
    );

    let analysisResult = response.data.choices[0].message.content;
    
    try {
      const jsonMatch = analysisResult.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        analysisResult = JSON.parse(jsonMatch[0]);
      } else {
        analysisResult = JSON.parse(analysisResult);
      }
    } catch (e) {
      analysisResult = {
        character: {
          personality: "分析完成",
          interests: "请查看详细内容",
          lifestyle: "",
          values: ""
        },
        suggestions: {
          topics: ["深入了解对方兴趣", "分享生活日常", "共同规划活动"],
          dates: ["一起喝咖啡", "看电影", "散步聊天"],
          tips: ["真诚沟通", "尊重对方", "保持耐心"],
          howToImpress: analysisResult
        }
      };
    }

    res.json({ success: true, data: analysisResult });

  } catch (error) {
    console.error('分析错误:', error.response?.data || error.message);
    res.status(500).json({ 
      error: '分析过程中出现错误', 
      details: error.message 
    });
  }
});

app.listen(PORT, () => {
  console.log(`服务器运行在 http://localhost:${PORT}`);
});
