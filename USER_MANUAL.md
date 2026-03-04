# 马来西亚SME碳核算系统 v1.0.0 使用手册
## 一、系统概述
支持马来西亚中小企业Scope1/Scope2碳核算的自动化系统，适配马来西亚能源局规范，实现Excel账单上传-解析-核算-同步-查询全链路自动化。

## 二、部署步骤
1. 环境要求：Python 3.8+、Flask 2.0+
2. 克隆仓库：git clone [你的GitHub仓库地址]
3. 安装依赖：pip install -r requirements.txt
4. 配置文件：修改config.py中的端口、上传目录等参数
5. 启动系统：python app.py

## 三、API接口清单
### 1. 文件上传+解析+核算
- 请求方式：POST
- 请求地址：/upload
- 请求参数：file（Excel文件）
- 返回示例：{"code":200,"msg":"成功","data":{"file_id":"xxx","carbon_result":xxx}}

### 2. 自动化解析+核算
- 请求方式：POST
- 请求地址：/api/parse_carbon
- 请求参数：file_key（文件标识）
- 返回示例：{"code":200,"msg":"成功","data":{"carbon_result":xxx}}

### 3. 核算结果同步
- 请求方式：POST
- 请求地址：/api/sync_results
- 请求参数：file_id（文件ID）
- 返回示例：{"code":200,"msg":"同步成功","data":{"json_path":"xxx"}}

### 4. 查询已处理记录
- 请求方式：GET
- 请求地址：/api/get_records
- 请求参数：无
- 返回示例：{"code":200,"msg":"成功","data":[{"file_name":"xxx","upload_time":"xxx","carbon_result":xxx}]}

## 四、全流程演示
1. 上传Excel账单文件（energy_data_input.xlsx）；
2. 调用/upload接口完成解析和核算；
3. 调用/api/sync_results同步核算结果到本地JSON文件；
4. 调用/api/get_records查询所有处理记录。

## 五、常见问题
1. 中文显示乱码：修改config.py中的编码为utf-8；
2. 文件上传失败：检查文件格式是否为xlsx，文件大小是否超过配置限制；
3. 核算结果异常：检查Excel账单的字段是否符合模板要求。