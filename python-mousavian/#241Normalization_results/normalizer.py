from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
import json


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _safe_int(x: Any) -> int:
    try:
        return int(x)
    except Exception:
        return 0


def _deep_get(d: Any, path: List[Union[str, int]], default=None):
    cur = d
    for p in path:
        try:
            if isinstance(p, int):
                cur = cur[p]
            else:
                cur = cur.get(p)
        except Exception:
            return default
    return cur if cur is not None else default


def _extract_text_from_any(payload: Dict[str, Any]) -> str:
    """
    Best-effort text extraction across common provider shapes.
    """
    # OpenAI Responses API-ish: output_text
    t = payload.get("output_text")
    if isinstance(t, str) and t.strip():
        return t

    # OpenAI Chat Completions: choices[0].message.content
    t = _deep_get(payload, ["choices", 0, "message", "content"])
    if isinstance(t, str) and t.strip():
        return t

    # OpenAI Chat Completions alt: choices[0].delta.content
    t = _deep_get(payload, ["choices", 0, "delta", "content"])
    if isinstance(t, str) and t.strip():
        return t

    # Anthropic-like: content as list of blocks: [{"type":"text","text":"..."}]
    content = payload.get("content")
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text" and isinstance(block.get("text"), str):
                parts.append(block["text"])
        if parts:
            return "".join(parts)

    # Generic: "text"
    t = payload.get("text")
    if isinstance(t, str) and t.strip():
        return t

    return ""


def _extract_tool_calls(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Best-effort extraction for tool/function calls across shapes.
    """
    out: List[Dict[str, Any]] = []

    # OpenAI Chat Completions: choices[0].message.tool_calls
    tcs = _deep_get(payload, ["choices", 0, "message", "tool_calls"], default=[])
    if isinstance(tcs, list):
        for tc in tcs:
            if not isinstance(tc, dict):
                continue
            fn = tc.get("function") or {}
            name = fn.get("name") or tc.get("name")
            args = fn.get("arguments") or tc.get("arguments")
            if isinstance(args, str):
                # arguments sometimes is JSON string
                try:
                    args = json.loads(args)
                except Exception:
                    args = {"_raw": args}
            out.append({
                "id": tc.get("id") or "",
                "name": name or "",
                "arguments": args if isinstance(args, dict) else {"_raw": args},
            })

    # Anthropic-ish: tool_use blocks in content
    content = payload.get("content")
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                args = block.get("input")
                out.append({
                    "id": block.get("id") or "",
                    "name": block.get("name") or "",
                    "arguments": args if isinstance(args, dict) else {"_raw": args},
                })

    return out


def _extract_usage(payload: Dict[str, Any]) -> Dict[str, int]:
    # OpenAI Chat Completions: usage.prompt_tokens, completion_tokens, total_tokens
    u = payload.get("usage") or {}
    if isinstance(u, dict):
        prompt = u.get("prompt_tokens", u.get("input_tokens", 0))
        comp = u.get("completion_tokens", u.get("output_tokens", 0))
        total = u.get("total_tokens", _safe_int(prompt) + _safe_int(comp))
        return {
            "input_tokens": _safe_int(prompt),
            "output_tokens": _safe_int(comp),
            "total_tokens": _safe_int(total),
        }

    return {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}


def normalize_model_output(
    raw: Dict[str, Any],
    *,
    provider: str,
    model: str,
    request_id: Optional[str] = None,
    latency_ms: Optional[int] = None,
    created_at: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Convert raw provider/model output into a standardized JSON document for DB.
    """
    text = _extract_text_from_any(raw)
    tool_calls = _extract_tool_calls(raw)
    usage = _extract_usage(raw)

    doc = {
        "schema_version": "1.0",
        "provider": provider,
        "model": model,
        "request_id": request_id,
        "created_at": created_at or _utc_now_iso(),
        "latency_ms": _safe_int(latency_ms) if latency_ms is not None else None,
        "usage": usage,
        "output": {
            "text": text,
            "messages": ([{"role": "assistant", "content": text}] if text else []),
            "tool_calls": tool_calls,
        },
        "raw": raw,  # keep full payload for auditing/debug
    }
    return doc
