let selectedImages = [];

function resetUpload() {
    console.log('重置上传状态...');
    selectedImages = [];
    const grid = document.getElementById('imageGrid');
    if (grid) {
        grid.innerHTML = '';
        console.log('图片网格已清空');
    }
    const fileInput = document.getElementById('fileInput');
    if (fileInput) {
        fileInput.value = '';
        fileInput.files = new DataTransfer().files;
        console.log('文件输入已清空');
    }
    const countEl = document.getElementById('imageCount');
    if (countEl) {
        countEl.textContent = '0';
        console.log('计数已重置');
    }
    const analyzeBtn = document.getElementById('analyzeBtn');
    if (analyzeBtn) {
        analyzeBtn.disabled = true;
        console.log('分析按钮已禁用');
    }
}

function showPage(pageId) {
    console.log('切换到页面:', pageId);
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    document.getElementById(pageId).classList.add('active');
    
    if (pageId === 'upload') {
        setTimeout(() => {
            resetUpload();
        }, 0);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    setupUpload();
});

function setupUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');

    uploadArea.addEventListener('click', () => fileInput.click());

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        handleFiles(e.dataTransfer.files);
    });

    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });
}

function handleFiles(files) {
    Array.from(files).forEach(file => {
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = (e) => {
                selectedImages.push({
                    file: file,
                    dataUrl: e.target.result
                });
                renderImageGrid();
                updateCount();
            };
            reader.readAsDataURL(file);
        }
    });
}

function renderImageGrid() {
    const grid = document.getElementById('imageGrid');
    grid.innerHTML = '';
    
    selectedImages.forEach((img, index) => {
        const item = document.createElement('div');
        item.className = 'image-item';
        item.innerHTML = `
            <img src="${img.dataUrl}" alt="图片${index + 1}">
            <button class="image-delete" onclick="removeImage(${index})">×</button>
        `;
        grid.appendChild(item);
    });
}

function removeImage(index) {
    selectedImages.splice(index, 1);
    renderImageGrid();
    updateCount();
}

function updateCount() {
    const count = selectedImages.length;
    document.getElementById('imageCount').textContent = count;
    
    const analyzeBtn = document.getElementById('analyzeBtn');
    analyzeBtn.disabled = count < 5;
}

async function startAnalyze() {
    showPage('analyzing');
    
    const formData = new FormData();
    selectedImages.forEach(img => {
        formData.append('images', img.file);
    });

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            renderResult(result.data);
            showPage('result');
        } else {
            alert(result.error || '分析失败，请重试');
            showPage('upload');
        }
    } catch (error) {
        console.error(error);
        alert('网络错误，请检查网络连接');
        showPage('upload');
    }
}

function renderResult(data) {
    const content = document.getElementById('resultContent');
    
    const character = data.character || {};
    const suggestions = data.suggestions || {};

    content.innerHTML = `
        <div class="result-card">
            <h3>人物画像</h3>
            <div class="character-grid">
                <div class="character-item">
                    <h4>性格特点</h4>
                    <p>${character.personality || '暂无分析'}</p>
                </div>
                <div class="character-item">
                    <h4>兴趣爱好</h4>
                    <p>${character.interests || '暂无分析'}</p>
                </div>
                <div class="character-item">
                    <h4>生活习惯</h4>
                    <p>${character.lifestyle || '暂无分析'}</p>
                </div>
                <div class="character-item">
                    <h4>价值观</h4>
                    <p>${character.values || '暂无分析'}</p>
                </div>
            </div>
        </div>

        <div class="result-card">
            <h3>聊天话题推荐</h3>
            <ul class="suggestion-list">
                ${(suggestions.topics || []).map(topic => `<li>${topic}</li>`).join('')}
            </ul>
        </div>

        <div class="result-card">
            <h3>约会建议</h3>
            <ul class="suggestion-list">
                ${(suggestions.dates || []).map(date => `<li>${date}</li>`).join('')}
            </ul>
        </div>

        <div class="result-card">
            <h3>注意事项</h3>
            <ul class="suggestion-list">
                ${(suggestions.tips || []).map(tip => `<li>${tip}</li>`).join('')}
            </ul>
        </div>

        <div class="result-card">
            <h3>如何让对方产生好感</h3>
            <p style="font-size: 15px; line-height: 1.8; color: #333;">
                ${suggestions.howToImpress || '真诚是最好的方式～'}
            </p>
        </div>
    `;
}
