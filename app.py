from flask import Flask, request, jsonify, render_template
import os
from bill_parser import BillParser  # 导入账单解析类（确保该文件存在）

# 初始化Flask应用
app = Flask(__name__)

# 配置上传目录
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
# 确保上传目录存在，不存在则创建
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ========== 核心修复：导入并注册api蓝图（解决404关键） ==========
from api import api_bp  # 导入api.py中的蓝图对象
app.register_blueprint(api_bp, url_prefix='/api')  # 注册蓝图，指定/api前缀
# ==============================================================

# 碳排放量计算核心函数
def calculate_carbon(diesel_consumption, electricity_consumption):
    """
    计算碳排放量（吨CO₂e）
    :param diesel_consumption: 柴油消耗量（L）
    :param electricity_consumption: 电网用电量（kWh）
    :return: 碳排放核算结果字典
    """
    # 碳排放因子（kg CO₂e / 单位）
    DIESEL_FACTOR = 3.64  # 柴油：3.64 kg/L
    ELECTRICITY_FACTOR = 0.53  # 电网用电：0.53 kg/kWh
    
    # 计算各范围碳排放（转换为吨，保留2位小数）
    scope1 = round(diesel_consumption * DIESEL_FACTOR / 1000, 2)  # 柴油排放（Scope1）
    scope2 = round(electricity_consumption * ELECTRICITY_FACTOR / 1000, 2)  # 用电排放（Scope2）
    total = round(scope1 + scope2, 2)  # 总排放量
    
    return {
        "scope1": scope1,
        "scope2": scope2,
        "total": total
    }

# 文件上传与解析接口
@app.route('/upload', methods=['POST'])
def upload_file():
    """通用文件上传接口：上传→解析→核算→返回结果"""
    try:
        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({
                "code": 400,
                "msg": "未上传文件",
                "data": None
            }), 400
        
        file = request.files['file']
        # 检查文件名是否为空
        if file.filename == '':
            return jsonify({
                "code": 400,
                "msg": "文件名不能为空",
                "data": None
            }), 400
        
        # 保存文件到上传目录
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # 解析账单数据
        parser = BillParser()
        parsed_data = parser.parse(file_path)
        
        # 提取消耗量（默认0.0，防止解析失败）
        diesel = parsed_data.get('diesel_consumption', 0.0)
        electricity = parsed_data.get('electricity_consumption', 0.0)
        
        # 计算碳排放量
        carbon_result = calculate_carbon(diesel, electricity)
        
        # 返回成功结果
        return jsonify({
            "code": 200,
            "msg": "文件解析与碳核算成功",
            "data": {
                "file_name": file.filename,
                "file_path": file_path,
                "parsed_data": parsed_data,
                "carbon_calculation": carbon_result
            }
        }), 200
    
    except Exception as e:
        # 异常捕获，返回错误信息
        return jsonify({
            "code": 500,
            "msg": f"处理失败：{str(e)}",
            "data": None
        }), 500

# 主页路由（渲染上传页面，需配套templates/index.html）
@app.route('/')
def index():
    return render_template('index.html')

# 启动服务
if __name__ == '__main__':
    # debug=True 便于开发调试，生产环境需改为False
    app.run(debug=True, port=5000, host='127.0.0.1')