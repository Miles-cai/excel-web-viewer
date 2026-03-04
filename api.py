# api.py
from flask import Blueprint, request, jsonify
import os
import json
import pandas as pd
from datetime import datetime
# 导入项目配置和账单解析类（与app.py保持一致）
from bill_parser import BillParser

# ==================== 核心配置 ====================
# 创建API蓝图（与Web路由隔离，前缀/api）
api_bp = Blueprint('api', __name__, url_prefix='/api')
# 上传目录（与app.py的UPLOAD_FOLDER保持一致）
UPLOAD_FOLDER = 'uploads'
# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==================== 复用核心计算逻辑 ====================
def calculate_carbon(diesel, electricity):
    """
    碳排放量计算核心函数（与app.py完全一致）
    :param diesel: 柴油消耗量 (升)
    :param electricity: 电网用电量 (千瓦时)
    :return: 各维度碳排放量[吨CO₂e]
    """
    # 柴油碳排放因子: 3.64 kg CO₂/L -> 转换为吨 (除以1000)
    diesel_carbon = diesel * 3.64 / 1000
    # 电网用电碳排放因子: 0.53 kg CO₂/kWh -> 转换为吨
    electricity_carbon = electricity * 0.53 / 1000
    # 总排放量
    total_carbon = diesel_carbon + electricity_carbon

    return {
        "scope1": round(diesel_carbon, 2),    # Scope 1 (燃料燃烧)
        "scope2": round(electricity_carbon, 2),# Scope 2 (电网用电)
        "total": round(total_carbon, 2)       # 总排放量
    }

# ==================== 核心API：文件解析+碳核算 ====================
@api_bp.route('/parse_carbon', methods=['POST'])
def parse_carbon():
    """
    API接口：上传文件 → 自动解析 → 核算碳排放量 → 返回结果
    请求方式：POST
    请求格式：multipart/form-data（file字段传Excel/CSV/PDF文件）
    返回格式：JSON
    """
    # 1. 校验文件是否存在
    if 'file' not in request.files:
        return jsonify({
            'code': 400,
            'msg': '未上传文件，请在file字段中上传账单文件',
            'data': None
        }), 400
    
    file = request.files['file']
    # 2. 校验文件名
    if file.filename == '':
        return jsonify({
            'code': 400,
            'msg': '文件名不能为空',
            'data': None
        }), 400
    
    try:
        # 3. 保存上传的文件
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        # 4. 解析账单数据
        parser = BillParser()
        parsed_data = parser.parse(file_path)
        
        # 5. 提取解析结果并计算碳排放
        diesel = parsed_data.get('diesel_consumption', 0.0)
        electricity = parsed_data.get('electricity_consumption', 0.0)
        carbon_result = calculate_carbon(diesel, electricity)
        
        # 6. 组装返回结果
        response_data = {
            'file_name': file.filename,
            'file_path': file_path,
            'parse_data': parsed_data,
            'carbon_calculation': carbon_result,
            'parse_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return jsonify({
            'code': 200,
            'msg': '文件解析+碳核算成功',
            'data': response_data
        }), 200
    
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'处理失败：{str(e)}',
            'data': None
        }), 500

# ==================== 核心同步API：本地JSON文件同步（方式1） ====================
@api_bp.route('/sync_results', methods=['POST'])
def sync_results():
    """
    API接口：将指定文件的核算结果同步为本地JSON文件（供外部系统读取）
    请求方式：POST
    请求格式：form-data（file_name字段传要同步的文件名）
    返回格式：JSON
    """
    # 1. 获取请求参数
    file_name = request.form.get('file_name')
    if not file_name:
        return jsonify({
            'code': 400,
            'msg': '缺少必要参数：file_name（要同步的账单文件名）',
            'data': None
        }), 400
    
    try:
        # 2. 校验文件是否存在
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        if not os.path.exists(file_path):
            return jsonify({
                'code': 404,
                'msg': f'文件不存在：{file_name}',
                'data': None
            }), 404
        
        # 3. 重新解析+核算（保证数据最新）
        parser = BillParser()
        parsed_data = parser.parse(file_path)
        diesel = parsed_data.get('diesel_consumption', 0.0)
        electricity = parsed_data.get('electricity_consumption', 0.0)
        carbon_result = calculate_carbon(diesel, electricity)
        
        # 4. 组装同步数据
        sync_data = {
            'file_name': file_name,
            'sync_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'parse_data': parsed_data,
            'carbon_calculation': carbon_result,
            'sync_file_path': ''  # 后续填充JSON文件路径
        }
        
        # 5. 生成JSON同步文件（命名规则：原文件名_carbon_result.json）
        sync_file_name = f"{os.path.splitext(file_name)[0]}_carbon_result.json"
        sync_file_path = os.path.join(UPLOAD_FOLDER, sync_file_name)
        
        # 6. 写入JSON文件（格式化输出，便于外部系统读取）
        with open(sync_file_path, 'w', encoding='utf-8') as f:
            json.dump(sync_data, f, ensure_ascii=False, indent=4)
        
        # 7. 补充同步文件路径并返回结果
        sync_data['sync_file_path'] = sync_file_path
        
        return jsonify({
            'code': 200,
            'msg': '核算结果已同步为本地JSON文件',
            'data': sync_data
        }), 200
    
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'同步失败：{str(e)}',
            'data': None
        }), 500

# ==================== 辅助API：获取已处理文件记录 ====================
@api_bp.route('/get_records', methods=['GET'])
def get_records():
    """
    API接口：获取上传目录下所有已处理的账单文件和同步结果文件
    请求方式：GET
    返回格式：JSON
    """
    try:
        # 遍历上传目录，分类获取文件
        bill_files = []  # 原始账单文件（Excel/CSV/PDF）
        sync_files = []  # 同步生成的JSON文件
        
        for file in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, file)
            # 获取文件基本信息
            file_info = {
                'file_name': file,
                'file_size': os.path.getsize(file_path),  # 文件大小（字节）
                'modify_time': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # 分类：账单文件
            if file.endswith(('.xlsx', '.xls', '.csv', '.pdf')):
                bill_files.append(file_info)
            # 分类：同步JSON文件
            elif file.endswith('_carbon_result.json'):
                sync_files.append(file_info)
        
        return jsonify({
            'code': 200,
            'msg': '获取记录成功',
            'data': {
                'total_bill_files': len(bill_files),
                'total_sync_files': len(sync_files),
                'bill_files': bill_files,
                'sync_files': sync_files
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'获取记录失败：{str(e)}',
            'data': None
        }), 500