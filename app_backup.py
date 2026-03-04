# 导入所有必要模块
import os
import io
import pdfkit
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd

# 创建Flask应用（必须在所有@app.route之前）
app = Flask(__name__)

# 全局变量：存储最新计算结果
latest_calc_result = None

# 配置上传文件夹
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 主页/文件上传页面
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global latest_calc_result
    if request.method == 'POST':
        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({'status': 'error', 'message': '未选择文件'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'status': 'error', 'message': '文件名为空'})
        
        # 验证文件格式
        if file and file.filename.endswith(('.xlsx', '.xls')):
            try:
                # 读取Excel文件
                df = pd.read_excel(file)
                
                # ======================
                # 碳核算核心计算逻辑（示例，可根据你的需求调整）
                # ======================
                # 1. 计算Scope1和Scope2总排放（示例数据，替换为你的实际逻辑）
                scope1_total = df['scope1_emission'].sum() if 'scope1_emission' in df.columns else 0
                scope2_total = df['scope2_emission'].sum() if 'scope2_emission' in df.columns else 0
                total_emission = scope1_total + scope2_total
                
                # 2. 读取营收数据
                revenue = df['revenue'].sum() if 'revenue' in df.columns else 0  # 营收（令吉）
                
                # 3. 计算排放强度（tCO₂e/百万令吉）
                million_revenue = revenue / 1000000
                scope1_intensity = scope1_total / million_revenue if million_revenue != 0 else 0
                scope2_intensity = scope2_total / million_revenue if million_revenue != 0 else 0
                total_intensity = total_emission / million_revenue if million_revenue != 0 else 0
                
                # 存储计算结果到全局变量
                latest_calc_result = {
                    'scope1_total': round(scope1_total, 4),
                    'scope2_total': round(scope2_total, 4),
                    'total_emission': round(total_emission, 4),
                    'revenue': round(revenue, 2),
                    'intensity': {
                        'scope1_intensity': round(scope1_intensity, 4),
                        'scope2_intensity': round(scope2_intensity, 4),
                        'total_intensity': round(total_intensity, 4)
                    }
                }
                
                # 返回计算结果
                return jsonify({
                    'status': 'success',
                    'data': latest_calc_result
                })
            
            except Exception as e:
                return jsonify({'status': 'error', 'message': f'计算失败：{str(e)}'})
        else:
            return jsonify({'status': 'error', 'message': '仅支持.xlsx/.xls格式的Excel文件'})
    
    # GET请求：返回上传页面
    return render_template('upload.html')

# 生成HTML报告接口
@app.route('/generate-html-report')
def generate_html_report():
    global latest_calc_result
    if not latest_calc_result:
        return jsonify({
            'status': 'error',
            'message': '请先完成碳核算计算（上传Excel并执行计算）'
        }), 400
    
    # 渲染HTML报告模板并返回
    return render_template('report.html', **latest_calc_result)

# 生成PDF报告接口（基于pdfkit，适配环境变量）
@app.route('/generate-pdf-report')
def generate_pdf_report():
    global latest_calc_result
    if not latest_calc_result:
        return jsonify({
            'status': 'error',
            'message': '请先完成碳核算计算（上传Excel并执行计算）'
        }), 400
    
    try:
        # 1. 渲染HTML模板
        html_content = render_template('report.html', **latest_calc_result)
        
        # 2. PDF生成参数（适配马来西亚报告格式）
        options = {
            'page-size': 'A4',
            'encoding': 'UTF-8',
            'no-outline': None,
            'margin-top': '10mm',
            'margin-right': '10mm',
            'margin-bottom': '10mm',
            'margin-left': '10mm'
        }
        
        # 3. 生成PDF到内存缓冲区
        pdf_buffer = io.BytesIO()
        pdfkit.from_string(html_content, pdf_buffer, options=options)
        pdf_buffer.seek(0)
        
        # 4. 生成安全文件名并返回下载
        safe_filename = f'Malaysia_SME_Carbon_Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        response = send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=safe_filename,
            mimetype='application/pdf'
        )
        
        # 禁止缓存
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'PDF生成失败：{str(e)}',
            'detail': '请检查：1.wkhtmltopdf是否安装 2.report.html模板是否存在 3.计算结果是否完整'
        }), 500

# 程序入口
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)