"""
ماژول توضیح‌پذیری (Explainability)
"""

from typing import List, Dict, Any, Optional
from app.services.evaluation_rules import EvaluationRulesManager
from app.utils.file_manager import FileManager


class ExplainabilityService:
    """سرویس توضیح‌پذیری برای تصمیم‌گیری سیستم"""
    
    def __init__(self, rules_manager: EvaluationRulesManager, file_manager: FileManager):
        self.rules_manager = rules_manager
        self.file_manager = file_manager
    
    def explain_decision(self, file_id: str, decision_id: Optional[str] = None) -> Dict[str, Any]:
        """
        توضیح تصمیم گرفته شده برای یک فایل
        
        Args:
            file_id: شناسه فایل
            decision_id: شناسه تصمیم (اختیاری)
        
        Returns:
            دیکشنری حاوی توضیحات
        """
        file_info = self.file_manager.get_file_info(file_id)
        if not file_info:
            raise ValueError(f"فایل با شناسه {file_id} یافت نشد")
        
        # دریافت قواعد فعال
        rules = self.rules_manager.get_all_rules(enabled_only=True)
        
        # شبیه‌سازی تحلیل (در نسخه واقعی، این از ماژول تحلیل می‌آید)
        explanations = []
        decision_factors = []
        total_score = 0.0
        max_score = 0.0
        
        for rule in rules:
            rule_score = self._evaluate_rule(rule, file_info)
            max_score += rule["weight"]
            total_score += rule_score * rule["weight"]
            
            explanations.append({
                "rule_id": rule["id"],
                "rule_name": rule["name"],
                "rule_type": rule["rule_type"],
                "score": rule_score,
                "weight": rule["weight"],
                "weighted_score": rule_score * rule["weight"],
                "explanation": f"قاعده '{rule['name']}' با امتیاز {rule_score:.2f} ارزیابی شد."
            })
            
            decision_factors.append({
                "factor": rule["name"],
                "impact": "positive" if rule_score > 0.7 else "negative" if rule_score < 0.4 else "neutral",
                "weight": rule["weight"]
            })
        
        confidence_score = total_score / max_score if max_score > 0 else 0.0
        
        return {
            "file_id": file_id,
            "explanations": explanations,
            "decision_factors": decision_factors,
            "confidence_score": round(confidence_score, 2),
            "total_score": round(total_score, 2),
            "max_score": round(max_score, 2)
        }
    
    def _evaluate_rule(self, rule: Dict[str, Any], file_info: Dict[str, Any]) -> float:
        """
        ارزیابی یک قاعده (شبیه‌سازی)
        در نسخه واقعی، این از ماژول تحلیل واقعی می‌آید
        """
        # شبیه‌سازی امتیازدهی
        import random
        return random.uniform(0.3, 0.9)




