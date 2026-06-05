from sqlalchemy.orm import Session
from sqlalchemy import desc
from models import Policy, Material, Version, AuditLog
from schemas import PolicyCreate, PolicyUpdate, MaterialCreate, VersionCreate
from datetime import datetime
import json
from typing import Optional, List, Dict, Any


class PolicyService:
    """政策管理服务"""

    @staticmethod
    def create_policy(db: Session, policy: PolicyCreate) -> Policy:
        """创建新政策"""
        db_policy = Policy(
            airline_code=policy.airline_code,
            airline_name=policy.airline_name,
            ticket_desk_type=policy.ticket_desk_type,
            raw_policy=policy.raw_policy,
            breakdown_json=policy.breakdown_json,
        )
        db.add(db_policy)
        db.flush()

        # 创建初始版本
        version = VersionService.create_version(
            db=db,
            policy_id=db_policy.id,
            operator="system",
            changes_summary="Initial policy creation",
            operation_type="create",
            policy_snapshot=db_policy.to_dict(),
        )

        db_policy.current_version_id = version.id
        db.commit()
        db.refresh(db_policy)
        return db_policy

    @staticmethod
    def get_policy(db: Session, policy_id: int) -> Optional[Policy]:
        """获取政策"""
        return db.query(Policy).filter(Policy.id == policy_id).first()

    @staticmethod
    def get_policies(
        db: Session, airline_code: Optional[str] = None, ticket_desk_type: Optional[str] = None, limit: int = 100
    ) -> List[Policy]:
        """查询政策"""
        query = db.query(Policy)

        if airline_code:
            query = query.filter(Policy.airline_code == airline_code)
        if ticket_desk_type:
            query = query.filter(Policy.ticket_desk_type == ticket_desk_type)

        return query.limit(limit).all()

    @staticmethod
    def update_policy(db: Session, policy_id: int, policy_update: PolicyUpdate, operator: str = "system") -> Optional[Policy]:
        """更新政策"""
        db_policy = PolicyService.get_policy(db, policy_id)
        if not db_policy:
            return None

        # 保存旧值用于Diff
        old_values = {
            "airline_name": db_policy.airline_name,
            "raw_policy": db_policy.raw_policy,
            "breakdown_json": db_policy.breakdown_json,
        }

        # 更新字段
        if policy_update.airline_name:
            db_policy.airline_name = policy_update.airline_name
        if policy_update.ticket_desk_type:
            db_policy.ticket_desk_type = policy_update.ticket_desk_type
        if policy_update.raw_policy is not None:
            db_policy.raw_policy = policy_update.raw_policy
        if policy_update.breakdown_json is not None:
            db_policy.breakdown_json = policy_update.breakdown_json

        db_policy.updated_at = datetime.utcnow()
        db.flush()

        # 创建新版本
        new_values = {
            "airline_name": db_policy.airline_name,
            "raw_policy": db_policy.raw_policy,
            "breakdown_json": db_policy.breakdown_json,
        }

        version = VersionService.create_version(
            db=db,
            policy_id=policy_id,
            operator=operator,
            changes_summary="Policy updated",
            changes_detail={"old_values": old_values, "new_values": new_values},
            operation_type="update",
            policy_snapshot=db_policy.to_dict(),
        )

        db_policy.current_version_id = version.id

        # 记录审计日志
        AuditService.log_action(db, policy_id, "update", operator, {"changes": new_values})

        db.commit()
        db.refresh(db_policy)
        return db_policy

    @staticmethod
    def delete_policy(db: Session, policy_id: int, operator: str = "system") -> bool:
        """删除政策"""
        db_policy = PolicyService.get_policy(db, policy_id)
        if not db_policy:
            return False

        AuditService.log_action(db, policy_id, "delete", operator, {"airline_code": db_policy.airline_code})

        db.delete(db_policy)
        db.commit()
        return True


class VersionService:
    """版本管理服务"""

    @staticmethod
    def create_version(
        db: Session,
        policy_id: int,
        operator: str,
        changes_summary: str = "",
        changes_detail: Optional[Dict[str, Any]] = None,
        operation_type: str = "update",
        policy_snapshot: Optional[Dict[str, Any]] = None,
    ) -> Version:
        """创建新版本"""
        # 获取最新版本号
        latest_version = (
            db.query(Version).filter(Version.policy_id == policy_id).order_by(desc(Version.version_number)).first()
        )
        next_version_number = (latest_version.version_number + 1) if latest_version else 1

        # 生成版本标签
        version_tag = f"v{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"

        version = Version(
            policy_id=policy_id,
            version_number=next_version_number,
            version_tag=version_tag,
            changes_summary=changes_summary,
            changes_detail=changes_detail,
            operator=operator,
            operation_type=operation_type,
            policy_snapshot=policy_snapshot,
        )

        db.add(version)
        db.commit()
        db.refresh(version)
        return version

    @staticmethod
    def get_version(db: Session, version_id: int) -> Optional[Version]:
        """获取版本"""
        return db.query(Version).filter(Version.id == version_id).first()

    @staticmethod
    def get_versions(db: Session, policy_id: int, limit: int = 100) -> List[Version]:
        """获取某政策的所有版本"""
        return (
            db.query(Version).filter(Version.policy_id == policy_id).order_by(desc(Version.created_at)).limit(limit).all()
        )

    @staticmethod
    def rollback_to_version(db: Session, policy_id: int, version_id: int, operator: str = "system") -> Optional[Version]:
        """回滚到指定版本"""
        target_version = VersionService.get_version(db, version_id)
        if not target_version or target_version.policy_id != policy_id:
            return None

        db_policy = db.query(Policy).filter(Policy.id == policy_id).first()
        if not db_policy:
            return None

        # 恢复快照
        if target_version.policy_snapshot:
            snapshot = target_version.policy_snapshot
            db_policy.airline_name = snapshot.get("airline_name")
            db_policy.raw_policy = snapshot.get("raw_policy")
            db_policy.breakdown_json = snapshot.get("breakdown")
            db_policy.updated_at = datetime.utcnow()
            db.flush()

        # 创建新版本记录回滚操作
        rollback_version = VersionService.create_version(
            db=db,
            policy_id=policy_id,
            operator=operator,
            changes_summary=f"Rollback to version {target_version.version_tag}",
            changes_detail={"rollback_from": target_version.version_tag},
            operation_type="rollback",
            policy_snapshot=db_policy.to_dict(),
        )

        db_policy.current_version_id = rollback_version.id

        # 记录审计日志
        AuditService.log_action(
            db, policy_id, "rollback", operator, {"from_version": target_version.version_tag, "to_version": rollback_version.version_tag}
        )

        db.commit()
        db.refresh(db_policy)
        return rollback_version


class MaterialService:
    """材料管理服务"""

    @staticmethod
    def add_material(db: Session, policy_id: int, material: MaterialCreate) -> Material:
        """添加材料要求"""
        db_material = Material(
            policy_id=policy_id,
            material_type=material.material_type,
            definition=material.definition,
            simple_rules=material.simple_rules,
            detailed_config=material.detailed_config,
        )
        db.add(db_material)
        db.commit()
        db.refresh(db_material)
        return db_material

    @staticmethod
    def get_materials(db: Session, policy_id: int) -> List[Material]:
        """获取某政策的所有材料要求"""
        return db.query(Material).filter(Material.policy_id == policy_id).all()

    @staticmethod
    def update_material(db: Session, material_id: int, material_update: MaterialCreate) -> Optional[Material]:
        """更新材料要求"""
        db_material = db.query(Material).filter(Material.id == material_id).first()
        if not db_material:
            return None

        if material_update.definition:
            db_material.definition = material_update.definition
        if material_update.simple_rules:
            db_material.simple_rules = material_update.simple_rules
        if material_update.detailed_config:
            db_material.detailed_config = material_update.detailed_config

        db.commit()
        db.refresh(db_material)
        return db_material

    @staticmethod
    def delete_material(db: Session, material_id: int) -> bool:
        """删除材料要求"""
        db_material = db.query(Material).filter(Material.id == material_id).first()
        if not db_material:
            return False

        db.delete(db_material)
        db.commit()
        return True


class AuditService:
    """审计日志服务"""

    @staticmethod
    def log_action(
        db: Session,
        policy_id: int,
        action: str,
        operator: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> AuditLog:
        """记录操作"""
        audit_log = AuditLog(
            policy_id=policy_id,
            action=action,
            operator=operator,
            details=details or {},
        )
        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)
        return audit_log

    @staticmethod
    def get_audit_logs(db: Session, policy_id: int, limit: int = 100) -> List[AuditLog]:
        """获取审计日志"""
        return db.query(AuditLog).filter(AuditLog.policy_id == policy_id).order_by(desc(AuditLog.created_at)).limit(limit).all()
