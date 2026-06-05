@echo off
REM 病退政策管理系统 - 快速启动脚本 (Windows)

echo ==================================================
echo   病退政策管理系统 - Phase 1
echo   Quick Start
echo ==================================================
echo.

REM 检查Python版本
echo 🔍 检查Python版本...
python --version
echo.

REM 检查Node版本
echo 🔍 检查Node版本...
node --version
echo.

REM 启动后端
echo 🚀 启动后端 API 服务...
cd backend
echo ✓ 安装后端依赖...
pip install -r requirements.txt > nul 2>&1

start "Policy System Backend" /D "%cd%" python app.py
echo ✓ 后端已启动 (在新窗口中)
echo   访问地址: http://localhost:8000
echo   API文档: http://localhost:8000/docs
echo.

REM 等待后端启动
echo ⏳ 等待后端启动...
timeout /t 3 /nobreak

REM 启动前端
echo 🚀 启动前端应用...
cd ../frontend
echo ✓ 安装前端依赖...
call npm install > nul 2>&1

echo.
echo ==================================================
echo ✅ 系统已启动！
echo ==================================================
echo.
echo 📋 打开以下地址:
echo    • 应用:     http://localhost:5173
echo    • API文档:  http://localhost:8000/docs
echo    • 健康检查: http://localhost:8000/health
echo.
echo 💡 提示:
echo    • 后端在独立窗口中运行
echo    • 按 Ctrl+C 停止前端
echo    • 关闭后端窗口停止API
echo.

call npm run dev
pause
