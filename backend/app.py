from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
import json

# 导入数据库和服务
from database import get_db, init_db
from models import Policy, Version, AuditLog
from schemas import (
    PolicyCreate,
    PolicyUpdate,
    PolicyResponse,
    MaterialCreate,
    MaterialResponse,
    VersionResponse,
    AuditLogResponse,
)
from services import PolicyService, VersionService, MaterialService, AuditService

# 创建FastAPI应用
app = FastAPI(
    title="病退政策管理系统 API",
    description="航司病退政策知识库与版本管理",
    version="1.0.0",
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== 初始化 ==============


@app.on_event("startup")
async def startup():
    """应用启动"""
    init_db()
    print("✓ API Server Started")


# ============== 政策接口 ==============


@app.post("/api/policies", response_model=PolicyResponse)
def create_policy(policy: PolicyCreate, db: Session = Depends(get_db)):
    """创建新政策"""
    # 检查重复
    existing = (
        db.query(Policy)
        .filter(Policy.airline_code == policy.airline_code, Policy.ticket_desk_type == policy.ticket_desk_type)
        .first()
    )
    if existing:
        raise HTTPException(status_code=409, detail=f"政策已存在: {policy.airline_code}-{policy.ticket_desk_type}")

    db_policy = PolicyService.create_policy(db, policy)
    return db_policy


@app.get("/api/policies", response_model=List[PolicyResponse])
def list_policies(
    airline_code: Optional[str] = Query(None),
    ticket_desk_type: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """查询政策列表"""
    policies = PolicyService.get_policies(db, airline_code=airline_code, ticket_desk_type=ticket_desk_type, limit=limit)
    return policies


@app.get("/api/policies/{policy_id}", response_model=PolicyResponse)
def get_policy(policy_id: int, db: Session = Depends(get_db)):
    """获取政策详情"""
    policy = PolicyService.get_policy(db, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="政策不存在")
    return policy


@app.put("/api/policies/{policy_id}", response_model=PolicyResponse)
def update_policy(policy_id: int, policy_update: PolicyUpdate, operator: Optional[str] = Query(default="manual"), db: Session = Depends(get_db)):
    """更新政策"""
    policy = PolicyService.update_policy(db, policy_id, policy_update, operator=operator)
    if not policy:
        raise HTTPException(status_code=404, detail="政策不存在")
    return policy


@app.delete("/api/policies/{policy_id}")
def delete_policy(policy_id: int, operator: Optional[str] = Query(default="manual"), db: Session = Depends(get_db)):
    """删除政策"""
    success = PolicyService.delete_policy(db, policy_id, operator=operator)
    if not success:
        raise HTTPException(status_code=404, detail="政策不存在")
    return {"status": "success", "message": "政策已删除"}


# ============== 材料接口 ==============


@app.post("/api/policies/{policy_id}/materials", response_model=MaterialResponse)
def add_material(policy_id: int, material: MaterialCreate, db: Session = Depends(get_db)):
    """为政策添加材料要求"""
    # 验证政策存在
    policy = PolicyService.get_policy(db, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="政策不存在")

    db_material = MaterialService.add_material(db, policy_id, material)
    return db_material


@app.get("/api/policies/{policy_id}/materials", response_model=List[MaterialResponse])
def get_materials(policy_id: int, db: Session = Depends(get_db)):
    """获取政策的所有材料要求"""
    policy = PolicyService.get_policy(db, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="政策不存在")

    materials = MaterialService.get_materials(db, policy_id)
    return materials


@app.put("/api/materials/{material_id}", response_model=MaterialResponse)
def update_material(material_id: int, material_update: MaterialCreate, db: Session = Depends(get_db)):
    """更新材料要求"""
    material = MaterialService.update_material(db, material_id, material_update)
    if not material:
        raise HTTPException(status_code=404, detail="材料不存在")
    return material


@app.delete("/api/materials/{material_id}")
def delete_material(material_id: int, db: Session = Depends(get_db)):
    """删除材料要求"""
    success = MaterialService.delete_material(db, material_id)
    if not success:
        raise HTTPException(status_code=404, detail="材料不存在")
    return {"status": "success", "message": "材料已删除"}


# ============== 版本接口 ==============


@app.get("/api/policies/{policy_id}/versions", response_model=List[VersionResponse])
def get_versions(policy_id: int, limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    """获取政策的版本历史"""
    policy = PolicyService.get_policy(db, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="政策不存在")

    versions = VersionService.get_versions(db, policy_id, limit=limit)
    return versions


@app.get("/api/versions/{version_id}", response_model=VersionResponse)
def get_version(version_id: int, db: Session = Depends(get_db)):
    """获取版本详情"""
    version = VersionService.get_version(db, version_id)
    if not version:
        raise HTTPException(status_code=404, detail="版本不存在")
    return version


@app.post("/api/policies/{policy_id}/versions/{version_id}/rollback", response_model=PolicyResponse)
def rollback_policy(
    policy_id: int,
    version_id: int,
    operator: Optional[str] = Query(default="manual"),
    db: Session = Depends(get_db),
):
    """回滚政策到指定版本"""
    rollback_version = VersionService.rollback_to_version(db, policy_id, version_id, operator=operator)
    if not rollback_version:
        raise HTTPException(status_code=404, detail="版本不存在或不匹配")

    policy = PolicyService.get_policy(db, policy_id)
    return policy


# ============== 审计日志接口 ==============


@app.get("/api/policies/{policy_id}/audit-logs", response_model=List[AuditLogResponse])
def get_audit_logs(policy_id: int, limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    """获取政策的审计日志"""
    policy = PolicyService.get_policy(db, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="政策不存在")

    logs = AuditService.get_audit_logs(db, policy_id, limit=limit)
    return logs


# ============== 统计接口 ==============


@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    """获取系统统计信息"""
    total_policies = db.query(Policy).count()
    total_versions = db.query(Version).count()
    airlines = db.query(Policy.airline_code).distinct().count()

    return {
        "total_policies": total_policies,
        "total_versions": total_versions,
        "total_airlines": airlines,
        "timestamp": datetime.utcnow().isoformat(),
    }


# ============== 健康检查 ==============


@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


# ============== 静态文件服务 ==============

# 挂载前端静态文件
static_path = Path(__file__).parent.parent / "static"
if static_path.exists():
    app.mount("/", StaticFiles(directory=str(static_path), html=True), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

# 启动时添加测试数据
@app.on_event("startup")
def startup_event():
    """应用启动时添加初始测试数据"""
    from database import SessionLocal
    from models import Policy
    db = SessionLocal()
    try:
        # 检查是否已经有数据
        existing = db.query(Policy).filter(Policy.airline_code == "FD/XJ/D7/AK/QZ/Z2/KT").first()
        if not existing:
            # 删除所有旧数据（可选）
            db.query(Policy).delete()
            
            # 添加亚航集团政策
            policy = Policy(
                airline_code="FD/XJ/D7/AK/QZ/Z2/KT",
                airline_name="亚航集团（Airasia Group）",
                ticket_desk_type="all",
                raw_policy="因病退票支持（有条件），因病改期否。旅客本人重大疾病或直系亲属重大疾病可申请。需在航班起飞前提交申请和完整材料。",
                breakdown_json={
                    "applicability": {
                        "refund": "支持（有条件）",
                        "rebooking": "否"
                    },
                    "conditions": {
                        "self_serious_illness": "可申请",
                        "relative_serious_illness": "可申请"
                    },
                    "time_limits": {
                        "cancel_seat": True,
                        "advance_hours": "起飞前",
                        "material_deadline": "客票有效期内"
                    },
                    "refund_rules": "不能全额退款，需收取相应取消费用"
                }
            )
            db.add(policy)
            db.commit()
            print("✅ 测试数据已添加")
    except Exception as e:
        print(f"❌ 添加测试数据失败: {e}")
    finally:
        db.close()
