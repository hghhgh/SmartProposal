"""
Code Name: knowledge_multi_source_merge
File: issues/issue_758_knowledge_merge.py

This script tests loading multiple knowledge sources and merging them
without conflicts.
"""

from typing import List, Dict
from pydantic import BaseModel
from fastapi import HTTPException

# Simulated in-memory knowledge storage
knowledge_db: Dict[str, Dict] = {}

class KnowledgeItem(BaseModel):
    id: str
    title: str
    content: str

def merge_knowledge_sources(sources: List[List[KnowledgeItem]]):
    """
    Merge multiple sources of knowledge items into the knowledge_db.
    Avoid conflicts based on unique item IDs.
    """
    merged_ids = []
    for source in sources:
        for item in source:
            if item.id in knowledge_db:
                # Conflict detected, skip item
                print(f"Conflict detected for item id {item.id}, skipping.")
                continue
            knowledge_db[item.id] = item.dict()
            merged_ids.append(item.id)
    return merged_ids

# Example usage
if __name__ == "__main__":
    # Source 1
    source1 = [
        KnowledgeItem(id="001", title="Python Basics", content="Introduction to Python."),
        KnowledgeItem(id="002", title="Data Structures", content="Lists, Dicts, Sets.")
    ]

    # Source 2
    source2 = [
        KnowledgeItem(id="002", title="Data Structures Updated", content="Advanced DS."),
        KnowledgeItem(id="003", title="Algorithms", content="Sorting and Searching.")
    ]

    merged = merge_knowledge_sources([source1, source2])
    print(f"Merged items: {merged}")
    print(f"Current knowledge DB: {knowledge_db}")
