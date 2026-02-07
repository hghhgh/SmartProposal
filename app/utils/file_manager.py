"""
مدیریت فایل‌های آپلود شده
"""

from pathlib import Path
from typing import Dict, Any, Optional
import json
import uuid
from datetime import datetime


class FileManager:
    """مدیریت فایل‌های آپلود شده و متادیتا"""
    
    def __init__(self, upload_dir: Path, metadata_file: Path):
        self.upload_dir = upload_dir
        self.metadata_file = metadata_file
        self.upload_dir.mkdir(exist_ok=True)
        self._ensure_metadata_file()
    
    def _ensure_metadata_file(self):
        """ایجاد فایل متادیتا در صورت عدم وجود"""
        if not self.metadata_file.exists():
            self.metadata_file.write_text("{}", encoding="utf-8")
    
    def _load_metadata(self) -> Dict[str, Any]:
        """بارگذاری متادیتا"""
        try:
            content = self.metadata_file.read_text(encoding="utf-8")
            return json.loads(content) if content else {}
        except:
            return {}
    
    def _save_metadata(self, metadata: Dict[str, Any]):
        """ذخیره متادیتا"""
        self.metadata_file.write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    
    def register_file(self, filename: str) -> str:
        """
        ثبت فایل جدید و برگرداندن file_id
        
        Args:
            filename: نام فایل
        
        Returns:
            file_id منحصر به فرد
        """
        file_id = str(uuid.uuid4())
        metadata = self._load_metadata()
        
        metadata[file_id] = {
            "file_id": file_id,
            "filename": filename,
            "uploaded_at": datetime.now().isoformat(),
            "status": "uploaded",
            "file_path": str(self.upload_dir / filename)
        }
        
        self._save_metadata(metadata)
        return file_id
    
    def get_file_info(self, file_id: str) -> Optional[Dict[str, Any]]:
        """دریافت اطلاعات فایل"""
        metadata = self._load_metadata()
        return metadata.get(file_id)
    
    def update_file_status(self, file_id: str, status: str, **kwargs):
        """به‌روزرسانی وضعیت فایل"""
        metadata = self._load_metadata()
        if file_id in metadata:
            metadata[file_id]["status"] = status
            metadata[file_id].update(kwargs)
            self._save_metadata(metadata)
    
    def get_file_path(self, file_id: str) -> Optional[Path]:
        """دریافت مسیر فایل"""
        file_info = self.get_file_info(file_id)
        if file_info:
            return Path(file_info["file_path"])
        return None




