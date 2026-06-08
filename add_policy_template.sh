#!/bin/bash
# 病退政策快速添加脚本

API_BASE="https://illnessrefundpolicy-production.up.railway.app/api"

# ═══════════════════════════════════════════════
# ⚙️  配置区域 - 修改下面的值
# ═══════════════════════════════════════════════

AIRLINE_CODE="MU"                    # 改成你的航司代码
AIRLINE_NAME="中国东方航空"          # 改成航司名称
TICKET_DESK_TYPE="all"              # all / counter / app / online
REFUND_SUPPORT="支持"               # 支持 / 否 / 支持(条件)
REBOOKING_SUPPORT="否"              # 支持 / 否 / 支持(条件)
CANCEL_SEAT=true                    # true / false
ADVANCE_HOURS="4"                   # 数字 或 "起飞前"
MATERIAL_DEADLINE="客票有效期内"    # 材料最晚时限

# ═══════════════════════════════════════════════
# 快速验证
# ═══════════════════════════════════════════════

echo "📌 创建政策："
echo "  代码: $AIRLINE_CODE"
echo "  名称: $AIRLINE_NAME"
echo "  类型: $TICKET_DESK_TYPE"
echo ""

# ═══════════════════════════════════════════════
# 创建政策
# ═══════════════════════════════════════════════

POLICY_RESPONSE=$(curl -s -X POST "$API_BASE/policies" \
  -H "Content-Type: application/json" \
  -d "{
    \"airline_code\": \"$AIRLINE_CODE\",
    \"airline_name\": \"$AIRLINE_NAME\",
    \"ticket_desk_type\": \"$TICKET_DESK_TYPE\",
    \"raw_policy\": \"政策原文...\",
    \"breakdown_json\": {
      \"applicability\": {
        \"refund\": \"$REFUND_SUPPORT\",
        \"rebooking\": \"$REBOOKING_SUPPORT\"
      },
      \"time_limits\": {
        \"cancel_seat\": $CANCEL_SEAT,
        \"advance_hours\": \"$ADVANCE_HOURS\",
        \"material_deadline\": \"$MATERIAL_DEADLINE\"
      }
    }
  }")

POLICY_ID=$(echo $POLICY_RESPONSE | grep -o '"id":[0-9]*' | head -1 | cut -d: -f2)

if [ -z "$POLICY_ID" ]; then
  echo "❌ 创建失败！"
  echo "$POLICY_RESPONSE"
  exit 1
fi

echo "✅ Policy ID: $POLICY_ID"
echo ""
echo "🌐 前端验证："
echo "   https://illnessrefund.netlify.app"
echo "   搜索航司: $AIRLINE_CODE"
