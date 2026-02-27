# app.py
# 加载 .env 文件（放在最顶部，确保后续代码能读取环境变量）
import os
from dotenv import load_dotenv
load_dotenv()  # 这行是关键，会读取项目根目录下的 .env 文件

# 导入所需依赖库
from flask import Flask, render_template_string, request
from werkzeug.utils import secure_filename
import pandas as pd
import platform
import urllib.parse

# 初始化 Flask 应用
app = Flask(__name__)

# 配置项（现在可以从环境变量读取，比如上传路径、文件大小限制等）
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', './uploads')  # 从.env读取，默认值为./uploads
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 从.env读取，默认16MB
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}
MAX_READ_ROWS = 1000

# 确保上传文件夹存在并处理权限
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
if platform.system() in ['Linux', 'Darwin']:
    import subprocess
    subprocess.run(['chmod', '777', app.config['UPLOAD_FOLDER']])

# 定义首页路由
@app.route('/')
def index():
    return '''
    <h1>Excel Web 应用已启动！✅</h1>
    <p>这是一个用于处理 Excel 文件的 Flask 应用。</p>
    <p>你可以在这里添加文件上传和数据处理功能。</p>
    '''

    # -------------------- 启动入口 --------------------
if __name__ == "__main__":
    # 可选：打印环境变量，用于验证加载是否成功
    print("=== 环境变量验证 ===")
    print(f"上传目录: {app.config['UPLOAD_FOLDER']}")
    print(f"最大文件大小: {app.config['MAX_CONTENT_LENGTH']} bytes")
    # 启动 Flask 应用
    app.run(debug=True, host='0.0.0.0', port=5000)