"""
ماژول مدیریت قواعد ارزیابی
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import json
import uuid
from datetime import datetime


class EvaluationRulesManager:
    """مدیریت قواعد ارزیابی پروپوزال"""
    
    def __init__(self, rules_file: Path):
        self.rules_file = rules_file
        self._ensure_rules_file()
    
    def _ensure_rules_file(self):
        """ایجاد فایل قواعد در صورت عدم وجود"""
        if not self.rules_file.exists():
            default_rules = {
                "rules": [],
                "last_updated": datetime.now().isoformat()
            }
            self.rules_file.write_text(
                json.dumps(default_rules, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
    
    def _load_rules(self) -> Dict[str, Any]:
        """بارگذاری قواعد"""
        try:
            content = self.rules_file.read_text(encoding="utf-8")
            return json.loads(content) if content else {"rules": []}
        except:
            return {"rules": []}
    
    def _save_rules(self, data: Dict[str, Any]):
        """ذخیره قواعد"""
        data["last_updated"] = datetime.now().isoformat()
        self.rules_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    
    def create_rule(self, name: str, description: str, rule_type: str,
                    weight: float, criteria: Dict[str, Any], enabled: bool = True) -> str:
        """
        ایجاد قاعده جدید
        
        Args:
            name: نام قاعده
            description: توضیحات
            rule_type: نوع قاعده (structural, grammatical, content)
            weight: وزن قاعده
            criteria: معیارهای ارزیابی
            enabled: فعال/غیرفعال
        
        Returns:
            rule_id
        """
        rule_id = str(uuid.uuid4())
        rule = {
            "id": rule_id,
            "name": name,
            "description": description,
            "rule_type": rule_type,
            "weight": weight,
            "enabled": enabled,
            "criteria": criteria,
            "created_at": datetime.now().isoformat()
        }
        
        data = self._load_rules()
        data["rules"].append(rule)
        self._save_rules(data)
        
        return rule_id
    
    def get_rule(self, rule_id: str) -> Optional[Dict[str, Any]]:
        """دریافت قاعده بر اساس ID"""
        data = self._load_rules()
        for rule in data["rules"]:
            if rule["id"] == rule_id:
                return rule
        return None
    
    def get_all_rules(self, enabled_only: bool = False) -> List[Dict[str, Any]]:
        """دریافت تمام قواعد"""
        data = self._load_rules()
        rules = data.get("rules", [])
        
        if enabled_only:
            rules = [r for r in rules if r.get("enabled", True)]
        
        return rules
    
    def update_rule(self, rule_id: str, **kwargs) -> bool:
        """به‌روزرسانی قاعده"""
        data = self._load_rules()
        
        for rule in data["rules"]:
            if rule["id"] == rule_id:
                rule.update(kwargs)
                rule["updated_at"] = datetime.now().isoformat()
                self._save_rules(data)
                return True
        
        return False
    
    def delete_rule(self, rule_id: str) -> bool:
        """حذف قاعده"""
        data = self._load_rules()
        original_count = len(data["rules"])
        data["rules"] = [r for r in data["rules"] if r["id"] != rule_id]
        
        if len(data["rules"]) < original_count:
            self._save_rules(data)
            return True
        
        return False
    
    def enable_rule(self, rule_id: str) -> bool:
        """فعال کردن قاعده"""
        return self.update_rule(rule_id, enabled=True)
    
    def disable_rule(self, rule_id: str) -> bool:
        """غیرفعال کردن قاعده"""
        return self.update_rule(rule_id, enabled=False)




