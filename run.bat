@echo off
echo 正在启动 BNBU EAP Teaching Assistant...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.7或更高版本
    pause
    exit /b 1
)

REM 检查是否已创建虚拟环境
if not exist "venv\" (
    echo 创建虚拟环境...
    python -m venv venv
    echo.
)

REM 激活虚拟环境并安装依赖，然后启动应用
echo 激活虚拟环境并准备启动...
call venv\Scripts\activate.bat & echo 安装依赖包... & pip install -r requirements.txt & echo. & echo 启动Flask应用... & echo 应用将在 http://localhost:5000 运行 & echo 按 Ctrl+C 停止应用 & echo. & python app.py

pause