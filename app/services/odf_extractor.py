"""
ماژول استخراج محتوا از فایل‌های ODF
"""

from pathlib import Path
from typing import Dict, Any, List
from odf.opendocument import load
from odf.text import P, H
from odf.table import Table, TableRow, TableCell


class ODFExtractor:
    """کلاس استخراج محتوا از فایل‌های ODT"""
    
    def __init__(self):
        pass
    
    def extract_text(self, file_path: Path) -> Dict[str, Any]:
        """
        استخراج متن از فایل ODT
        
        Args:
            file_path: مسیر فایل ODT
        
        Returns:
            دیکشنری حاوی متن و متادیتا
        """
        try:
            doc = load(str(file_path))
            
            # استخراج متن از پاراگراف‌ها
            paragraphs = []
            for paragraph in doc.getElementsByType(P):
                text = self._extract_text_from_element(paragraph)
                if text.strip():
                    paragraphs.append(text)
            
            # استخراج متن از عنوان‌ها
            headings = []
            for heading in doc.getElementsByType(H):
                text = self._extract_text_from_element(heading)
                if text.strip():
                    headings.append(text)
            
            # استخراج متن از جداول
            tables = []
            for table in doc.getElementsByType(Table):
                table_data = self._extract_table_data(table)
                if table_data:
                    tables.append(table_data)
            
            # ترکیب تمام متن
            full_text = "\n\n".join(paragraphs)
            
            return {
                "full_text": full_text,
                "paragraphs": paragraphs,
                "headings": headings,
                "tables": tables,
                "metadata": {
                    "total_paragraphs": len(paragraphs),
                    "total_headings": len(headings),
                    "total_tables": len(tables),
                    "total_length": len(full_text)
                }
            }
        except Exception as e:
            raise Exception(f"خطا در استخراج محتوا از فایل ODT: {str(e)}")
    
    def _extract_text_from_element(self, element) -> str:
        """استخراج متن از یک المان"""
        text_parts = []
        for node in element.childNodes:
            if node.nodeType == 3:  # Text node
                text_parts.append(node.data)
            elif hasattr(node, 'childNodes'):
                text_parts.append(self._extract_text_from_element(node))
        return "".join(text_parts)
    
    def _extract_table_data(self, table) -> List[List[str]]:
        """استخراج داده از جدول"""
        rows_data = []
        for row in table.getElementsByType(TableRow):
            row_data = []
            for cell in row.getElementsByType(TableCell):
                cell_text = self._extract_text_from_element(cell)
                row_data.append(cell_text.strip())
            if row_data:
                rows_data.append(row_data)
        return rows_data




