# 配置文件：所有可配置的参数都放这里，不用改主代码
import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 上传文件夹路径
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

# 允许的文件类型
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# 文件大小限制（10MB）
MAX_CONTENT_LENGTH = 10 * 1024 * 1024

# Flask 调试模式（生产环境要改成 False）
DEBUG = True

# 服务端口
PORT = 5000