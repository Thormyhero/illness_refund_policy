#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
病退政策管理系统 - 政策添加工具

用法:
    python add_policy_cli.py --code "MU" --name "中国东方航空" --refund "支持" --rebooking "否"

或交互式:
    python add_policy_cli.py
"""

import requests
import json
import sys
from typing import Optional

API_BASE = "https://illnessrefundpolicy-production.up.railway.app/api"

def add_policy(
    airline_code: str,
    airline_name: str,
    ticket_desk_type: str = "all",
    refund_support: str = "支持",
    rebooking_support: str = "否",
    raw_policy: str = "",
    advance_hours: str = "起飞前"
) -> bool:
    """添加政策到系统"""
    
    url = f"{API_BASE}/policies"
    
    payload = {
        "airline_code": airline_code,
        "airline_name": airline_name,
        "ticket_desk_type": ticket_desk_type,
        "raw_policy": raw_policy,
        "breakdown_json": {
            "applicability": {
                "refund": refund_support,
                "rebooking": rebooking_support
            },
            "time_limits": {
                "cancel_seat": True,
                "advance_hours": advance_hours,
                "material_deadline": "客票有效期内"
            }
        }
    }
    
    try:
        print(f"📌 正在添加政策: {airline_name} ({airline_code})...")
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            policy_id = data.get('id')
            print(f"✅ 成功！Policy ID: {policy_id}")
            return True
        elif response.status_code == 409 or "已存在" in response.text:
            print(f"⚠️  政策已存在: {airline_code}-{ticket_desk_type}")
            return True
        else:
            print(f"❌ 失败！状态码: {response.status_code}")
            print(f"   响应: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def interactive_mode():
    """交互式添加政策"""
    print("\n🚀 病退政策添加工具 (交互模式)")
    print("━" * 50)
    
    while True:
        print("\n请输入政策信息（留空表示使用默认值）:")
        
        airline_code = input("航司代码 (如: MU): ").strip()
        if not airline_code:
            print("❌ 航司代码不能为空")
            continue
        
        airline_name = input("航司名称 (如: 中国东方航空): ").strip()
        if not airline_name:
            print("❌ 航司名称不能为空")
            continue
        
        refund = input("是否支持因病退票 (支持/否) [默认:支持]: ").strip() or "支持"
        rebooking = input("是否支持因病改期 (支持/否) [默认:否]: ").strip() or "否"
        advance_hours = input("提前提交时间 (如: 4) [默认:起飞前]: ").strip() or "起飞前"
        
        if add_policy(airline_code, airline_name, refund_support=refund, rebooking_support=rebooking, advance_hours=advance_hours):
            again = input("\n继续添加? (y/n) [默认:y]: ").strip().lower() or "y"
            if again != "y":
                print("✅ 已完成")
                break
        else:
            retry = input("\n重试? (y/n) [默认:y]: ").strip().lower() or "y"
            if retry != "y":
                break

def batch_mode():
    """批量添加政策"""
    policies = [
        ("MU", "中国东方航空", "支持", "否", "4"),
        ("CA", "中国国际航空", "支持", "否", "3"),
        ("CZ", "中国南方航空", "支持", "支持", "2"),
        ("3U", "四川航空", "支持", "否", "起飞前"),
    ]
    
    print("\n🚀 批量添加示例政策")
    print("━" * 50)
    
    success = 0
    failed = 0
    
    for code, name, refund, rebooking, hours in policies:
        if add_policy(code, name, refund_support=refund, rebooking_support=rebooking, advance_hours=hours):
            success += 1
        else:
            failed += 1
    
    print("\n" + "━" * 50)
    print(f"✅ 成功: {success} | ❌ 失败: {failed}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 命令行模式
        import argparse
        parser = argparse.ArgumentParser(description="病退政策添加工具")
        parser.add_argument("--code", required=True, help="航司代码")
        parser.add_argument("--name", required=True, help="航司名称")
        parser.add_argument("--refund", default="支持", help="是否支持因病退票")
        parser.add_argument("--rebooking", default="否", help="是否支持因病改期")
        parser.add_argument("--hours", default="起飞前", help="提前提交时间")
        parser.add_argument("--policy", default="", help="政策原文")
        
        args = parser.parse_args()
        add_policy(
            args.code,
            args.name,
            refund_support=args.refund,
            rebooking_support=args.rebooking,
            advance_hours=args.hours,
            raw_policy=args.policy
        )
    else:
        # 交互模式
        choice = input("选择模式: (1)交互模式 (2)批量添加 [默认:1]: ").strip() or "1"
        
        if choice == "2":
            batch_mode()
        else:
            interactive_mode()
