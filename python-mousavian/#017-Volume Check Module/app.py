from __future__ import annotations

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

MAX_BYTES = 20 * 1024 * 1024  # 20MB

app = FastAPI()


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # Read stream in chunks to avoid loading very large files at once
    total = 0
    chunk_size = 1024 * 1024  # 1MB

    while True:
        chunk = await file.read(chunk_size)
        if not chunk:
            break
        total += len(chunk)
        if total > MAX_BYTES:
            raise HTTPException(status_code=413, detail=f"File too large. Max is {MAX_BYTES} bytes.")

    return {"ok": True, "filename": file.filename, "size": total}


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"ok": False, "detail": exc.detail})
