from fastapi import FastAPI, UploadFile, File, HTTPException, Path as PathParam
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
import json

# Import services and utilities
from app.services.data_cleaning import DataCleaning
from app.services.tokenizer import PersianTokenizer
from app.services.odf_extractor import ODFExtractor
from app.services.evaluation_rules import EvaluationRulesManager
from app.services.explainability import ExplainabilityService
from app.services.bias_detection import BiasDetectionService
from app.core.security import SecuritySettings, SecurityMiddleware
from app.utils.file_manager import FileManager
from app.models.schemas import (
    PreprocessResponse, EvaluationRule, EvaluationRuleResponse,
    ExplainabilityRequest, ExplainabilityResponse, BiasDetectionResponse
)

# مسیر ذخیره‌سازی فایل‌ها و بازخوردها
UPLOAD_DIR = Path("uploads")
FEEDBACK_FILE = Path("feedback.json")
METADATA_FILE = Path("file_metadata.json")
RULES_FILE = Path("evaluation_rules.json")
SECURITY_CONFIG_FILE = Path("security_config.json")
UPLOAD_DIR.mkdir(exist_ok=True)
if not FEEDBACK_FILE.exists():
    FEEDBACK_FILE.write_text("[]", encoding="utf-8")  # ایجاد فایل خالی JSON برای بازخوردها

# Initialize services
file_manager = FileManager(UPLOAD_DIR, METADATA_FILE)
data_cleaning = DataCleaning()
tokenizer = PersianTokenizer()
odf_extractor = ODFExtractor()
rules_manager = EvaluationRulesManager(RULES_FILE)
explainability_service = ExplainabilityService(rules_manager, file_manager)
bias_detection_service = BiasDetectionService(file_manager)
security_settings = SecuritySettings(SECURITY_CONFIG_FILE)
security_middleware_service = SecurityMiddleware(security_settings)

# تنظیمات FastAPI و CORS
app = FastAPI(title="SmartProposal Backend")

origins = [
    "http://localhost:3000"
]

# CORS Middleware
security_config = security_settings.get_config()
cors_config = security_config.get("cors", {})
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_config.get("allowed_origins", origins),
    allow_credentials=cors_config.get("allow_credentials", True),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security Headers Middleware
from app.middleware.security_middleware import SecurityHeadersMiddleware

# Create a wrapper function for the middleware
def create_security_middleware(app_instance):
    return SecurityHeadersMiddleware(app_instance, security_middleware_service)

# Add middleware after app creation
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    security_headers = security_middleware_service.get_security_headers()
    for header, value in security_headers.items():
        response.headers[header] = value
    return response

@app.get("/")
def root():
    return {"message": "SmartProposal Backend is running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    دریافت فایل ODT و ذخیره آن در سرور
    """
    if not file:
        raise HTTPException(status_code=400, detail="هیچ فایلی ارسال نشده است")

    if not file.filename.lower().endswith(".odt"):
        raise HTTPException(status_code=400, detail="فقط فایل با فرمت ODT مجاز است")

    try:
        save_path = UPLOAD_DIR / file.filename
        with save_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # ثبت فایل در سیستم
        file_id = file_manager.register_file(file.filename)

        return JSONResponse(
            status_code=200,
            content={
                "file_id": file_id,
                "filename": file.filename,
                "message": "فایل با موفقیت آپلود شد"
            }
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="خطای داخلی سرور. لطفاً بعداً دوباره تلاش کنید"
        )

@app.post("/feedback")
async def submit_feedback(feedback: str):
    """
    ثبت بازخورد کاربر (good, average, bad) و ذخیره آن در فایل JSON
    """
    if feedback not in ["good", "average", "bad"]:
        raise HTTPException(status_code=400, detail="مقدار بازخورد معتبر نیست")

    try:
        # خواندن بازخوردهای قبلی
        existing_feedback = json.loads(FEEDBACK_FILE.read_text(encoding="utf-8"))
        # اضافه کردن بازخورد جدید
        existing_feedback.append({"feedback": feedback})
        # ذخیره مجدد در فایل
        FEEDBACK_FILE.write_text(json.dumps(existing_feedback, ensure_ascii=False, indent=2), encoding="utf-8")

        return {
            "message": "بازخورد شما با موفقیت ثبت شد",
            "feedback": feedback
        }

    except Exception:
        raise HTTPException(status_code=500, detail="خطای ذخیره بازخورد")

@app.get("/feedbacks")
def get_all_feedbacks():
    """
    مشاهده تمام بازخوردهای ثبت شده (برای تست و بررسی)
    """
    try:
        feedbacks = json.loads(FEEDBACK_FILE.read_text(encoding="utf-8"))
        return {"feedbacks": feedbacks}
    except Exception:
        raise HTTPException(status_code=500, detail="خطای خواندن بازخوردها")

@app.post("/preprocess/{file_id}", response_model=PreprocessResponse)
async def preprocess_file(file_id: str):
    """
    پیش‌پردازش فایل آپلود شده
    این API فایل ODT را می‌خواند، متن را استخراج می‌کند،
    پاکسازی می‌کند و توکن‌سازی می‌کند.
    """
    # بررسی وجود فایل
    file_info = file_manager.get_file_info(file_id)
    if not file_info:
        raise HTTPException(status_code=404, detail="فایل یافت نشد")
    
    file_path = file_manager.get_file_path(file_id)
    if not file_path or not file_path.exists():
        raise HTTPException(status_code=404, detail="فایل در سیستم فایل یافت نشد")
    
    try:
        # به‌روزرسانی وضعیت
        file_manager.update_file_status(file_id, "processing")
        
        # استخراج متن از فایل ODT
        extracted_data = odf_extractor.extract_text(file_path)
        original_text = extracted_data["full_text"]
        
        # پاکسازی متن
        cleaned_text = data_cleaning.clean_text(original_text)
        
        # توکن‌سازی
        token_stats = tokenizer.get_token_stats(cleaned_text)
        
        # آمار پاکسازی
        cleaning_stats = data_cleaning.get_cleaning_stats(original_text, cleaned_text)
        
        # به‌روزرسانی وضعیت
        file_manager.update_file_status(
            file_id,
            "processed",
            cleaned_text=cleaned_text,
            token_stats=token_stats,
            cleaning_stats=cleaning_stats
        )
        
        return PreprocessResponse(
            file_id=file_id,
            status="success",
            cleaned_text=cleaned_text,
            token_stats=token_stats,
            cleaning_stats=cleaning_stats,
            metadata=extracted_data["metadata"]
        )
    
    except Exception as e:
        file_manager.update_file_status(file_id, "error", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"خطا در پیش‌پردازش فایل: {str(e)}"
        )

# ========== API مدیریت قواعد ارزیابی ==========

@app.post("/evaluation-rules", response_model=EvaluationRuleResponse)
async def create_evaluation_rule(rule: EvaluationRule):
    """
    ایجاد قاعده ارزیابی جدید
    """
    try:
        rule_id = rules_manager.create_rule(
            name=rule.name,
            description=rule.description,
            rule_type=rule.rule_type,
            weight=rule.weight,
            criteria=rule.criteria,
            enabled=rule.enabled
        )
        
        created_rule = rules_manager.get_rule(rule_id)
        return EvaluationRuleResponse(
            success=True,
            message="قاعده با موفقیت ایجاد شد",
            rule=created_rule
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطا در ایجاد قاعده: {str(e)}")

@app.get("/evaluation-rules", response_model=EvaluationRuleResponse)
async def get_all_evaluation_rules(enabled_only: bool = False):
    """
    دریافت تمام قواعد ارزیابی
    """
    try:
        rules = rules_manager.get_all_rules(enabled_only=enabled_only)
        return EvaluationRuleResponse(
            success=True,
            message="قواعد با موفقیت دریافت شدند",
            rules=rules
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطا در دریافت قواعد: {str(e)}")

@app.get("/evaluation-rules/{rule_id}", response_model=EvaluationRuleResponse)
async def get_evaluation_rule(rule_id: str):
    """
    دریافت قاعده ارزیابی بر اساس ID
    """
    rule = rules_manager.get_rule(rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="قاعده یافت نشد")
    
    return EvaluationRuleResponse(
        success=True,
        message="قاعده با موفقیت دریافت شد",
        rule=rule
    )

@app.put("/evaluation-rules/{rule_id}", response_model=EvaluationRuleResponse)
async def update_evaluation_rule(rule_id: str, rule: EvaluationRule):
    """
    به‌روزرسانی قاعده ارزیابی
    """
    if not rules_manager.get_rule(rule_id):
        raise HTTPException(status_code=404, detail="قاعده یافت نشد")
    
    try:
        success = rules_manager.update_rule(
            rule_id,
            name=rule.name,
            description=rule.description,
            rule_type=rule.rule_type,
            weight=rule.weight,
            criteria=rule.criteria,
            enabled=rule.enabled
        )
        
        if success:
            updated_rule = rules_manager.get_rule(rule_id)
            return EvaluationRuleResponse(
                success=True,
                message="قاعده با موفقیت به‌روزرسانی شد",
                rule=updated_rule
            )
        else:
            raise HTTPException(status_code=500, detail="خطا در به‌روزرسانی قاعده")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطا در به‌روزرسانی قاعده: {str(e)}")

@app.delete("/evaluation-rules/{rule_id}", response_model=EvaluationRuleResponse)
async def delete_evaluation_rule(rule_id: str):
    """
    حذف قاعده ارزیابی
    """
    success = rules_manager.delete_rule(rule_id)
    if not success:
        raise HTTPException(status_code=404, detail="قاعده یافت نشد")
    
    return EvaluationRuleResponse(
        success=True,
        message="قاعده با موفقیت حذف شد"
    )

@app.post("/evaluation-rules/{rule_id}/enable", response_model=EvaluationRuleResponse)
async def enable_evaluation_rule(rule_id: str):
    """فعال کردن قاعده"""
    success = rules_manager.enable_rule(rule_id)
    if not success:
        raise HTTPException(status_code=404, detail="قاعده یافت نشد")
    
    return EvaluationRuleResponse(
        success=True,
        message="قاعده فعال شد"
    )

@app.post("/evaluation-rules/{rule_id}/disable", response_model=EvaluationRuleResponse)
async def disable_evaluation_rule(rule_id: str):
    """غیرفعال کردن قاعده"""
    success = rules_manager.disable_rule(rule_id)
    if not success:
        raise HTTPException(status_code=404, detail="قاعده یافت نشد")
    
    return EvaluationRuleResponse(
        success=True,
        message="قاعده غیرفعال شد"
    )

# ========== API توضیح‌پذیری ==========

@app.post("/explainability", response_model=ExplainabilityResponse)
async def explain_decision(request: ExplainabilityRequest):
    """
    دریافت توضیحات برای تصمیم گرفته شده
    """
    try:
        result = explainability_service.explain_decision(
            file_id=request.file_id,
            decision_id=request.decision_id
        )
        
        return ExplainabilityResponse(
            file_id=result["file_id"],
            explanations=result["explanations"],
            decision_factors=result["decision_factors"],
            confidence_score=result["confidence_score"]
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطا در تولید توضیحات: {str(e)}")

# ========== API تشخیص bias ==========

@app.get("/bias-detection/{file_id}", response_model=BiasDetectionResponse)
async def detect_bias(file_id: str):
    """
    تشخیص bias در فایل
    """
    try:
        result = bias_detection_service.detect_bias(file_id)
        
        return BiasDetectionResponse(
            file_id=result["file_id"],
            has_bias=result["has_bias"],
            bias_types=result["bias_types"],
            bias_details=result["bias_details"],
            recommendations=result["recommendations"]
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطا در تشخیص bias: {str(e)}")

# ========== API تنظیمات امنیتی ==========

@app.get("/security/settings")
async def get_security_settings():
    """
    دریافت تنظیمات امنیتی سیستم
    """
    try:
        config = security_settings.get_config()
        # حذف اطلاعات حساس قبل از ارسال
        safe_config = {k: v for k, v in config.items() if k != "secret_keys"}
        return safe_config
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطا در دریافت تنظیمات: {str(e)}")

@app.put("/security/settings")
async def update_security_settings(settings: dict):
    """
    به‌روزرسانی تنظیمات امنیتی سیستم
    """
    try:
        security_settings.update_config(**settings)
        return {"message": "تنظیمات امنیتی با موفقیت به‌روزرسانی شد"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطا در به‌روزرسانی تنظیمات: {str(e)}")
