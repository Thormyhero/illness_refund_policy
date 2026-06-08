from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import json

Base = declarative_base()


class Policy(Base):
    """航司病退政策主表"""
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    airline_code = Column(String(100), index=True, nullable=False)  # 航司代码 (AK/MU/CZ等)
    airline_name = Column(String(100), nullable=False)  # 航司名称
    ticket_desk_type = Column(String(50), default="all", nullable=False)  # 票台类型

    # 政策原文
    raw_policy = Column(Text, nullable=True)  # 原始政策文本

    # 拆解后的结构化数据
    breakdown_json = Column(JSON, nullable=True)  # {
    #   "applicability": {...},
    #   "time_limits": {...},
    #   "materials": {...}
    # }

    # 元数据
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    current_version_id = Column(Integer, nullable=True)  # 去掉外键，避免循环引用

    # 关系 - 明确指定 foreign_keys 避免歧义
    versions = relationship("Version", back_populates="policy", cascade="all, delete-orphan", foreign_keys="Version.policy_id")
    materials = relationship("Material", back_populates="policy", cascade="all, delete-orphan", foreign_keys="Material.policy_id")
    audit_logs = relationship("AuditLog", back_populates="policy", cascade="all, delete-orphan", foreign_keys="AuditLog.policy_id")

    def to_dict(self):
        return {
            "id": self.id,
            "airline_code": self.airline_code,
            "airline_name": self.airline_name,
            "ticket_desk_type": self.ticket_desk_type,
            "raw_policy": self.raw_policy,
            "breakdown": self.breakdown_json,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "current_version": self.current_version_id,
        }


class Material(Base):
    """材料要求详情表"""
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False, index=True)
    material_type = Column(String(100), nullable=False)  # medical_certificate/diagnosis/invoice等

    # 完整定义
    definition = Column(Text, nullable=True)

    # 简要规则 (JSON数组)
    simple_rules = Column(JSON, default=list)  # ["rule1", "rule2", ...]

    # 详细配置 (JSON)
    detailed_config = Column(JSON, nullable=True)  # {
    #   "required": true,
    #   "fields": [...],
    #   "validation_rules": [...]
    # }

    policy = relationship("Policy", back_populates="materials")

    def to_dict(self):
        return {
            "id": self.id,
            "material_type": self.material_type,
            "definition": self.definition,
            "simple_rules": self.simple_rules,
            "detailed_config": self.detailed_config,
        }


class Version(Base):
    """政策版本历史表"""
    __tablename__ = "versions"

    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False, index=True)

    # 版本标识
    version_number = Column(Integer, nullable=False)  # v1, v2, v3...
    version_tag = Column(String(50), nullable=False)  # 格式: v{YYYY-MM-DD-HHmmss}

    # 变更信息
    changes_summary = Column(String(500), nullable=True)  # 简短描述
    changes_detail = Column(JSON, nullable=True)  # {
    #   "fields_changed": [...],
    #   "old_values": {...},
    #   "new_values": {...}
    # }

    # 元数据
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    operator = Column(String(100), nullable=False)  # 操作者 (user/ai-bot-name)
    operation_type = Column(String(20), default="update")  # create/update/rollback

    # 快照 (完整的政策数据)
    policy_snapshot = Column(JSON, nullable=True)

    policy = relationship("Policy", back_populates="versions")

    def to_dict(self):
        return {
            "id": self.id,
            "version_number": self.version_number,
            "version_tag": self.version_tag,
            "changes_summary": self.changes_summary,
            "changes_detail": self.changes_detail,
            "created_at": self.created_at.isoformat(),
            "operator": self.operator,
            "operation_type": self.operation_type,
        }


class AuditLog(Base):
    """操作审计日志表"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False, index=True)

    # 操作信息
    action = Column(String(50), nullable=False)  # create/update/delete/rollback
    operator = Column(String(100), nullable=False)

    # 操作详情
    details = Column(JSON, nullable=True)

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    policy = relationship("Policy", back_populates="audit_logs")

    def to_dict(self):
        return {
            "id": self.id,
            "action": self.action,
            "operator": self.operator,
            "details": self.details,
            "created_at": self.created_at.isoformat(),
        }
