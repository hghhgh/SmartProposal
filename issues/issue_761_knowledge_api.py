"""
Code Name: knowledge_api_manager
File: issues/issue_761_knowledge_api.py

This module provides endpoints for uploading, listing, and removing knowledge items.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict

router = APIRouter()

# Simulated in-memory database
knowledge_db: Dict[str, Dict] = {}

class KnowledgeItem(BaseModel):
    id: str
    title: str
    content: str

class KnowledgeBatch(BaseModel):
    items: List[KnowledgeItem]

# -------------------------------
# Upload a single knowledge item
# -------------------------------
@router.post("/admin/knowledge/upload")
async def upload_knowledge(item: KnowledgeItem):
    if item.id in knowledge_db:
        raise HTTPException(status_code=400, detail=f"Item with id {item.id} already exists")
    knowledge_db[item.id] = item.dict()
    return {"status": "success", "item_id": item.id}

# -------------------------------
# Batch upload knowledge items
# -------------------------------
@router.post("/admin/knowledge/upload/batch")
async def upload_knowledge_batch(batch: KnowledgeBatch):
    added_items = []
    for item in batch.items:
        if item.id not in knowledge_db:
            knowledge_db[item.id] = item.dict()
            added_items.append(item.id)
    return {"status": "success", "added_items": added_items}

# -------------------------------
# List all knowledge items
# -------------------------------
@router.get("/admin/knowledge/list")
async def list_knowledge():
    return {"knowledge_items": list(knowledge_db.values())}

# -------------------------------
# Remove a knowledge item
# -------------------------------
@router.delete("/admin/knowledge/remove/{item_id}")
async def remove_knowledge(item_id: str):
    if item_id not in knowledge_db:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")
    removed_item = knowledge_db.pop(item_id)
    return {"status": "success", "removed_item": removed_item}
