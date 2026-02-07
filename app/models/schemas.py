"""
مدل‌های Pydantic برای API
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class PreprocessRequest(BaseModel):
    """درخواست پیش‌پردازش"""
    file_id: str
    options: Optional[Dict[str, Any]] = None


class PreprocessResponse(BaseModel):
    """پاسخ پیش‌پردازش"""
    file_id: str
    status: str
    cleaned_text: Optional[str] = None
    token_stats: Optional[Dict[str, Any]] = None
    cleaning_stats: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class EvaluationRule(BaseModel):
    """قاعده ارزیابی"""
    id: Optional[str] = None
    name: str
    description: str
    rule_type: str  # structural, grammatical, content
    weight: float
    enabled: bool = True
    criteria: Dict[str, Any]


class EvaluationRuleResponse(BaseModel):
    """پاسخ مدیریت قواعد"""
    success: bool
    message: str
    rule: Optional[EvaluationRule] = None
    rules: Optional[List[EvaluationRule]] = None


class ExplainabilityRequest(BaseModel):
    """درخواست توضیح‌پذیری"""
    file_id: str
    decision_id: Optional[str] = None


class ExplainabilityResponse(BaseModel):
    """پاسخ توضیح‌پذیری"""
    file_id: str
    explanations: List[Dict[str, Any]]
    decision_factors: List[Dict[str, Any]]
    confidence_score: float


class BiasDetectionResponse(BaseModel):
    """پاسخ تشخیص bias"""
    file_id: str
    has_bias: bool
    bias_types: List[str]
    bias_details: List[Dict[str, Any]]
    recommendations: List[str]




