@echo off
chcp 65001 >nul
echo ======================================
echo 正在清理Python缓存文件...
echo ======================================
:: 删除所有__pycache__目录
for /d /r . %%d in (__pycache__) do @if exist "%%d" (
    rd /s /q "%%d"
    echo 已删除目录: %%d
)

:: 删除所有.pyc文件
del /s /q *.pyc >nul 2>&1
if %errorlevel% equ 0 (
    echo 已删除所有.pyc文件
) else (
    echo 未找到.pyc文件
)

:: 删除所有.pyo文件
del /s /q *.pyo >nul 2>&1
if %errorlevel% equ 0 (
    echo 已删除所有.pyo文件
) else (
    echo 未找到.pyo文件
)

echo ======================================
echo 缓存文件清理完成！
echo 3秒后自动关闭窗口...
echo ======================================
timeout /t 3 /nobreak >nul