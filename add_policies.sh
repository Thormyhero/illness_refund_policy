#!/bin/bash

# ════════════════════════════════════════════════════════════
# 病退政策管理系统 - 安全的政策添加脚本
# 
# 用途：安全地添加和更新政策，不影响系统部署
# 用法：bash add_policies.sh
# ════════════════════════════════════════════════════════════

set -e

API_BASE="https://illnessrefundpolicy-production.up.railway.app/api"
FAILED=0
SUCCESS=0

echo "🚀 病退政策添加脚本 v1.0"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 函数：添加政策
add_policy() {
    local code=$1
    local name=$2
    local refund=$3
    local rebooking=$4
    local hours=$5
    
    echo "📌 添加政策: $name ($code)"
    
    local response=$(curl -s -X POST "$API_BASE/policies" \
        -H "Content-Type: application/json" \
        -d "{
            \"airline_code\": \"$code\",
            \"airline_name\": \"$name\",
            \"ticket_desk_type\": \"all\",
            \"raw_policy\": \"病退政策\",
            \"breakdown_json\": {
                \"applicability\": {
                    \"refund\": \"$refund\",
                    \"rebooking\": \"$rebooking\"
                },
                \"time_limits\": {
                    \"cancel_seat\": true,
                    \"advance_hours\": \"$hours\",
                    \"material_deadline\": \"客票有效期内\"
                }
            }
        }")
    
    local id=$(echo $response | grep -o '"id":[0-9]*' | head -1 | cut -d: -f2)
    
    if [ ! -z "$id" ]; then
        echo "   ✅ 成功！Policy ID: $id"
        ((SUCCESS++))
        return 0
    else
        echo "   ❌ 失败！响应: $response"
        ((FAILED++))
        return 1
    fi
}

# ════════════════════════════════════════════════════════════
# 添加航司政策 - 修改这里添加你的政策
# ════════════════════════════════════════════════════════════

# 格式: add_policy "代码" "名称" "退票支持" "改期支持" "提前小时"

add_policy "FD/XJ/D7/AK/QZ/Z2/KT" "亚航集团(Airasia Group)" "支持(条件)" "否" "起飞前"
add_policy "MU" "中国东方航空" "支持" "否" "4"
add_policy "CA" "中国国际航空" "支持" "否" "3"
add_policy "CZ" "中国南方航空" "支持" "支持" "2"

# ════════════════════════════════════════════════════════════
# 总结
# ════════════════════════════════════════════════════════════

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 添加结果:"
echo "   ✅ 成功: $SUCCESS"
echo "   ❌ 失败: $FAILED"
echo ""
echo "🌐 验证: https://illnessrefund.netlify.app"
echo "   → 刷新前端页面，搜索航司代码"
echo ""

if [ $FAILED -gt 0 ]; then
    exit 1
else
    exit 0
fi
