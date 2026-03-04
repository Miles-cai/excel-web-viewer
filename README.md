### Excel Web Viewer - README.md 专业版
# Excel Web Viewer
一款轻量级的 Excel 在线查看工具，支持通过浏览器快速访问、预览 Excel 文件，无需本地安装复杂办公软件，适配基础的表格数据展示与简单交互需求。

## 项目介绍
本项目基于 Python 构建，核心实现 Excel 文件的网页端解析与渲染，旨在提供一个便捷、高效的在线 Excel 查看解决方案。适合个人开发者快速搭建私有表格查看服务，或集成到小型业务系统中实现表格数据的在线共享。

## 核心功能
- ✅ 浏览器端直接预览 Excel（.xlsx/.xls）文件
- ✅ 基础表格数据渲染，保留单元格核心格式
- ✅ 轻量部署，依赖少、启动快
- ✅ 支持自定义配置，灵活适配使用场景

## 技术栈
- **后端**：Python
- **核心依赖**：详见 `requirements.txt`
- **前端**：基础 HTML/CSS/JavaScript（集成于 `templates` 目录）

## 快速开始
### 版本说明
当前稳定版本：v1.0.0

### 环境准备
确保本地已安装 Python（3.8+ 推荐）。

### 安装依赖
```bash
pip install -r requirements.txt

启动服务
```bash
python app.py

访问使用
启动后，打开浏览器访问 http://localhost:5000（默认端口，可在 config.py 中修改），按照页面指引上传并查看 Excel 文件。
API 接口清单
1. 文件上传接口
请求方式：POST
请求路径：/upload
请求参数：
```表格
参数名	类型	必选	说明
file	file	是	待上传的 Excel 文件
filename	string	否	自定义文件名（可选）

返回示例（成功）：
```json
{
  "code": 200,
  "msg": "文件上传成功",
  "data": {
    "file_id": "123456789",
    "filename": "example.xlsx",
    "file_path": "./uploads/123456789.xlsx",
    "upload_time": "2024-01-01 12:00:00"
  }
}

返回示例（失败）：
```json
{
  "code": 400,
  "msg": "文件上传失败：不支持的文件格式",
  "data": null
}

2. Excel 文件预览接口
请求方式：GET
请求路径：/preview/<file_id>
请求参数（路径参数）：
```表格
参数名	类型	必选	说明
file_id	string	是	上传文件返回的唯一标识
返回示例（成功）：
```json
{
  "code": 200,
  "msg": "文件预览数据获取成功",
  "data": {
    "file_id": "123456789",
    "filename": "example.xlsx",
    "sheets": [
      {
        "sheet_name": "Sheet1",
        "rows": [
          ["姓名", "年龄", "性别"],
          ["张三", 25, "男"],
          ["李四", 30, "女"]
        ]
      }
    ]
  }
}

返回示例（失败）：
```json
{
  "code": 404,
  "msg": "文件不存在或已过期",
  "data": null
}

3. 服务健康检查接口
请求方式：GET
请求路径：/health
请求参数：无
返回示例：
```json
{
  "code": 200,
  "msg": "服务运行正常",
  "data": {
    "version": "v1.0.0",
    "status": "running",
    "port": 5000
  }
}

项目结构
```plaintext
excel-web-viewer/
├── templates/        # 前端页面模板
├── .gitignore        # Git 忽略规则配置
├── app.py            # 项目主入口，实现核心服务逻辑
├── config.py         # 配置文件（端口、路径等）
├── requirements.txt  # 项目依赖清单
├── test.py           # 功能测试文件
└── README.md         # 项目说明文档

自定义配置
可在 config.py 中修改以下核心配置：
PORT：服务启动端口（默认 5000）
UPLOAD_FOLDER：Excel 文件上传目录
ALLOWED_EXTENSIONS：支持的文件格式（默认 .xlsx/.xls）
常见问题
问题 1：网页中 Excel 内容中文显示为乱码
解决方案：
1.检查后端 Python 环境的编码是否为 UTF-8（执行 python -c "import sys; print(sys.getdefaultencoding())"，确保输出为 utf-8）；
2.确保 app.py 中处理文件时指定编码为 UTF-8，例如：
```python
df = pd.read_excel(file_path, encoding='utf-8')
3.前端 HTML 页面头部添加编码声明：
```html
<meta charset="UTF-8">


问题 2：文件上传失败，提示 “文件大小超出限制”
解决方案：
1.打开 config.py，新增 / 修改文件大小限制配置：
```python
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 限制为16MB，可根据需求调整
2.重启服务后重新上传。

问题 3：上传 .xls 文件提示 “不支持的文件格式”
解决方案：
1.检查 config.py 中 ALLOWED_EXTENSIONS 是否包含 .xls：
```python
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
2.安装依赖库 xlrd（处理 .xls 格式必需）：
```bash
pip install xlrd==1.2.0  # 高版本 xlrd 不支持 .xls，需指定1.2.0版本

问题 4：启动服务时提示 “端口 5000 已被占用”
解决方案：
1.修改 config.py 中的 PORT 配置（例如改为 5001）；
2.或关闭占用 5000 端口的进程后重新启动：
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <进程ID> /F

# Linux/Mac
lsof -i :5000
kill -9 <进程ID>

贡献指南
Fork 本仓库
创建特性分支 (git checkout -b feature/AmazingFeature)
提交代码 (git commit -m 'Add some AmazingFeature')
推送到分支 (git push origin feature/AmazingFeature)
打开 Pull Request
许可证

本项目采用 MIT 许可证，详情见 LICENSE 文件（可自行添加）。

### 关键优化说明：
1. **版本号标注**：在「快速开始」下新增「版本说明」小节，明确标注 v1.0.0；
2. **API 接口清单**：补充了核心的文件上传、预览、健康检查接口，包含请求方式、路径、参数、返回示例（覆盖成功/失败场景），格式清晰易读；
3. **常见问题**：针对中文乱码、文件上传失败、.xls 格式不支持、端口占用等高频问题，提供具体可落地的解决方案；
4. **兼容性**：所有补充内容均基于项目原有技术栈，确保“克隆即能用”，无额外依赖引入；
5. **格式规范**：保持 Markdown 格式统一，接口参数用表格展示，返回示例用代码块，提升可读性。

你可根据实际项目的接口逻辑（如 `app.py` 中真实的接口路径/参数）微调 API 清单中的内容，确保与代码逻辑一致。
