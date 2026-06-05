#!/bin/bash

# 病退政策管理系统 - 快速启动脚本

echo "=================================================="
echo "  病退政策管理系统 - Phase 1"
echo "  Quick Start"
echo "=================================================="
echo ""

# 检查Python版本
echo "🔍 检查Python版本..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Python版本: $python_version"
echo ""

# 检查Node版本
echo "🔍 检查Node版本..."
node_version=$(node --version)
echo "✓ Node版本: $node_version"
echo ""

# 启动后端
echo "🚀 启动后端 API 服务..."
cd backend
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ 后端依赖已安装"

# 在后台启动后端
nohup python app.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "✓ 后端已启动 (PID: $BACKEND_PID)"
echo "   访问地址: http://localhost:8000"
echo "   API文档: http://localhost:8000/docs"
echo ""

# 等待后端启动
echo "⏳ 等待后端启动..."
sleep 3

# 启动前端
echo "🚀 启动前端应用..."
cd ../frontend
npm install > /dev/null 2>&1
echo "✓ 前端依赖已安装"

echo ""
echo "=================================================="
echo "✅ 系统已启动！"
echo "=================================================="
echo ""
echo "📋 打开以下地址:"
echo "   • 应用:     http://localhost:5173"
echo "   • API文档:  http://localhost:8000/docs"
echo "   • 健康检查: http://localhost:8000/health"
echo ""
echo "💡 提示:"
echo "   • 后端日志: backend.log"
echo "   • 按 Ctrl+C 停止"
echo ""

# 启动前端开发服务器
npm run dev
