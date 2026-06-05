"""
测试脚本：导入亚航病退政策并验证API
"""
import requests
import json
from datetime import datetime

# API基础URL
BASE_URL = "http://localhost:8000/api"

# 亚航病退政策 - 完整拆解后的数据结构
AIRASIA_POLICY = {
    "airline_code": "AK",
    "airline_name": "AirAsia",
    "ticket_desk_type": "all",
    "raw_policy": """
    前提条件：
    因病退票：
    1、旅客本人重大疾病：可以申请，结果以航司审核为准
    2、旅客直系亲属重大疾病：可以申请，结果以航司审核为准
    因病改期：否

    操作时限：
    如客人确认退票必须在航班起飞前提出申请并提交完成全部材料
    """,
    "breakdown_json": {
        "applicability": {
            "refund": "Yes",
            "conditions": "Self or direct family with critical disease, subject to airline review",
            "rebooking": "No",
        },
        "time_limits": {
            "cancel_seat": True,
            "advance_hours": "Before departure",
            "material_deadline": "Customer ticket validity",
        },
        "materials": [
            "ticketing_document",
            "medical_certificate",
            "hospital_records",
            "inspection_report",
            "medical_invoice",
            "companion_proof",
        ],
    },
}

# 材料详情
MATERIALS = [
    {
        "material_type": "ticketing_document",
        "definition": "所有办理的乘客(含陪同)需提供购票证件照片(含客人证件信息页)",
        "simple_rules": [
            "包含陪同人的购票证明",
            "涵盖购票证件列出的所有条件",
        ],
    },
    {
        "material_type": "medical_certificate",
        "definition": "医疗机构开具的不适宜乘机证明，需包含主治医生签字或盖章且为纸质版，非中国大陆就医旅客需提供英文版",
        "simple_rules": [
            "纸质版诊断证明",
            "材料开具时间在下单时间之后，在航班起飞前",
            "不适宜乘机时间涵盖起飞时间",
            "需要有主治医生签字或医院盖章",
            "非中国大陆就医旅客需提供英文版",
        ],
    },
    {
        "material_type": "hospital_records",
        "definition": "医疗机构出具的有主治医生签签字或医院盖章的英文纸质版出院小结，患病者须乘客之一",
        "simple_rules": [
            "纸质版出院小结",
            "患者需乘客之一",
            "需要有主治医生签字或医院盖章",
            "非中国大陆就医旅客需提供英文版",
        ],
    },
    {
        "material_type": "inspection_report",
        "definition": "医疗机构出具的纸质版检查报告单，如化验/扫描MRI/CT/X-光等，非中国大陆就医旅客需提供英文版",
        "simple_rules": [
            "纸质版检查报告单",
            "包括化验/扫描MRI/CT/X-光等",
            "非中国大陆就医旅客需提供英文版",
        ],
    },
    {
        "material_type": "medical_invoice",
        "definition": "医院开具的纸质版缴费凭证",
        "simple_rules": [
            "医院开具的缴费证明",
            "证明需为纸质版",
            "发票出具医院需与诊断证明出具医院相同",
        ],
    },
    {
        "material_type": "companion_proof",
        "definition": "陪同人与患病旅客需为直系亲属，且同时提出退票，需提供结婚证书，出生证明或其他能证明直系亲属关系的文件",
        "simple_rules": [
            "陪同人需为直系亲属",
            "须同时提出退票",
            "需提供能证明直系亲属关系的文件",
        ],
    },
]


def test_health():
    """测试健康检查"""
    print("🔍 测试健康检查...")
    response = requests.get("http://localhost:8000/health")
    print(f"  ✓ {response.json()}\n")


def test_create_policy():
    """创建政策"""
    print("📝 创建亚航病退政策...")
    response = requests.post(f"{BASE_URL}/policies", json=AIRASIA_POLICY)
    if response.status_code == 200:
        policy = response.json()
        print(f"  ✓ 政策创建成功 (ID: {policy['id']})")
        return policy["id"]
    else:
        print(f"  ✗ 创建失败: {response.text}")
        return None


def test_add_materials(policy_id: int):
    """添加材料要求"""
    print(f"📋 添加材料要求 (政策ID: {policy_id})...")
    for material in MATERIALS:
        response = requests.post(f"{BASE_URL}/policies/{policy_id}/materials", json=material)
        if response.status_code == 200:
            print(f"  ✓ {material['material_type']} 添加成功")
        else:
            print(f"  ✗ {material['material_type']} 添加失败: {response.text}")


def test_get_policy(policy_id: int):
    """获取政策详情"""
    print(f"\n📖 获取政策详情 (ID: {policy_id})...")
    response = requests.get(f"{BASE_URL}/policies/{policy_id}")
    if response.status_code == 200:
        policy = response.json()
        print(f"  ✓ 航司: {policy['airline_name']}")
        print(f"  ✓ 票台: {policy['ticket_desk_type']}")
        print(f"  ✓ 材料数: {len(policy['materials'])}")
        return policy
    else:
        print(f"  ✗ 获取失败: {response.text}")
        return None


def test_list_policies():
    """列表查询"""
    print("\n🔎 查询政策列表...")
    response = requests.get(f"{BASE_URL}/policies?airline_code=AK")
    if response.status_code == 200:
        policies = response.json()
        print(f"  ✓ 查询到 {len(policies)} 个政策")
        for p in policies:
            print(f"    - {p['airline_code']}: {p['airline_name']}")
    else:
        print(f"  ✗ 查询失败: {response.text}")


def test_get_versions(policy_id: int):
    """获取版本历史"""
    print(f"\n📜 获取版本历史 (ID: {policy_id})...")
    response = requests.get(f"{BASE_URL}/policies/{policy_id}/versions")
    if response.status_code == 200:
        versions = response.json()
        print(f"  ✓ 共 {len(versions)} 个版本:")
        for v in versions:
            print(f"    - {v['version_tag']} ({v['operation_type']}) by {v['operator']}")
    else:
        print(f"  ✗ 查询失败: {response.text}")


def test_update_policy(policy_id: int):
    """更新政策"""
    print(f"\n✏️  更新政策 (ID: {policy_id})...")
    update_data = {
        "airline_name": "AirAsia (Updated)",
        "raw_policy": "Updated policy text...",
    }
    response = requests.put(f"{BASE_URL}/policies/{policy_id}?operator=test-user", json=update_data)
    if response.status_code == 200:
        print(f"  ✓ 政策更新成功")
        policy = response.json()
        print(f"  ✓ 当前版本: {policy['current_version_id']}")
    else:
        print(f"  ✗ 更新失败: {response.text}")


def test_get_audit_logs(policy_id: int):
    """获取审计日志"""
    print(f"\n📋 获取审计日志 (ID: {policy_id})...")
    response = requests.get(f"{BASE_URL}/policies/{policy_id}/audit-logs")
    if response.status_code == 200:
        logs = response.json()
        print(f"  ✓ 共 {len(logs)} 条日志:")
        for log in logs:
            print(f"    - {log['action']} by {log['operator']} at {log['created_at']}")
    else:
        print(f"  ✗ 查询失败: {response.text}")


def test_stats():
    """获取统计信息"""
    print("\n📊 获取系统统计...")
    response = requests.get(f"{BASE_URL}/stats")
    if response.status_code == 200:
        stats = response.json()
        print(f"  ✓ 总政策数: {stats['total_policies']}")
        print(f"  ✓ 总版本数: {stats['total_versions']}")
        print(f"  ✓ 航司数: {stats['total_airlines']}")
    else:
        print(f"  ✗ 查询失败: {response.text}")


def main():
    """运行所有测试"""
    print("=" * 60)
    print("病退政策管理系统 - API 测试")
    print("=" * 60 + "\n")

    try:
        # 1. 健康检查
        test_health()

        # 2. 创建政策
        policy_id = test_create_policy()
        if not policy_id:
            print("❌ 无法创建政策，停止测试")
            return

        # 3. 添加材料
        test_add_materials(policy_id)

        # 4. 获取政策详情
        test_get_policy(policy_id)

        # 5. 列表查询
        test_list_policies()

        # 6. 获取版本历史
        test_get_versions(policy_id)

        # 7. 更新政策
        test_update_policy(policy_id)

        # 8. 获取版本历史（验证新版本）
        test_get_versions(policy_id)

        # 9. 获取审计日志
        test_get_audit_logs(policy_id)

        # 10. 统计信息
        test_stats()

        print("\n" + "=" * 60)
        print("✅ 所有测试完成！")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 测试出错: {e}")


if __name__ == "__main__":
    main()
