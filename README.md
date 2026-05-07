# 朋友圈分析交友助手

## 项目简介

一个基于 H5 的社交分析工具，通过分析用户上传的朋友圈截图，利用豆包大模型生成个性化的交友策略建议。

## 项目结构

```
.
├── app.py             # Python 后端（推荐）
├── requirements.txt   # Python 依赖
├── package.json       # Node.js 配置
├── server.js          # Node.js 后端
├── .env.example       # 环境变量模板
├── .env               # 环境变量（需自行创建）
├── .gitignore
├── PRD.md
├── README.md
└── public/
    ├── index.html     # 首页
    ├── style.css      # 样式
    └── app.js         # 前端逻辑
```

## 使用步骤

### 方式一：Python 版本（推荐）

#### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

#### 2. 配置环境变量

编辑 `.env` 文件，填入你的火山引擎 ARK API Key：

```
ARK_API_KEY=your_api_key_here
PORT=3000
```

#### 3. 获取 API Key

1. 访问 https://console.volcengine.com/ark/region:ark+cn-beijing/apikey
2. 创建新的 API Key
3. 将 Key 填入 `.env` 文件

#### 4. 启动服务

```bash
python app.py
```

#### 5. 访问应用

在浏览器中打开：http://localhost:3000

---

### 方式二：Node.js 版本

#### 1. 安装依赖

```bash
npm install
```

#### 2. 配置环境变量

编辑 `.env` 文件，填入你的火山引擎 ARK API Key

#### 3. 启动服务

```bash
npm start
```

#### 4. 访问应用

在浏览器中打开：http://localhost:3000

## 功能说明

1. **首页**：产品介绍和功能展示
2. **上传页面**：支持拖拽或点击上传图片，至少需要5张
3. **分析中**：AI 分析过程中的加载状态
4. **结果页面**：展示人物画像和交友建议

## 分析维度

- 人物画像：性格特点、兴趣爱好、生活习惯、价值观
- 交友建议：聊天话题、约会建议、注意事项、如何产生好感

## 技术栈

- 后端：Node.js + Express
- 前端：HTML5 + CSS3 + JavaScript（原生）
- AI：火山引擎豆包大模型（doubao-seed-2.0-lite-260215）
