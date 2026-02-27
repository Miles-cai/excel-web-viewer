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
### 环境准备
确保本地已安装 Python（3.8+ 推荐）。

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动服务
```bash
python app.py
```

### 访问使用
启动后，打开浏览器访问 `http://localhost:5000`（默认端口，可在 `config.py` 中修改），按照页面指引上传并查看 Excel 文件。

## 项目结构
```
excel-web-viewer/
├── templates/        # 前端页面模板
├── .gitignore        # Git 忽略规则配置
├── app.py            # 项目主入口，实现核心服务逻辑
├── config.py         # 配置文件（端口、路径等）
├── requirements.txt  # 项目依赖清单
├── test.py           # 功能测试文件
└── README.md         # 项目说明文档
```

## 自定义配置
可在 `config.py` 中修改以下核心配置：
- `PORT`：服务启动端口（默认 5000）
- `UPLOAD_FOLDER`：Excel 文件上传目录
- `ALLOWED_EXTENSIONS`：支持的文件格式（默认 .xlsx/.xls）

## 贡献指南
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交代码 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证
本项目采用 MIT 许可证，详情见 LICENSE 文件（可自行添加）。