from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000"
]

app = FastAPI(title="SmartProposal Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Receives an ODT file and saves it to server
    """
    if not file.filename.endswith(".odt"):
        return JSONResponse(content={"error": "Only .odt files allowed"}, status_code=400)

    save_path = UPLOAD_DIR / file.filename
    with save_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Placeholder response
    return {"filename": file.filename, "message": "File uploaded successfully, analysis pending."}


@app.get("/")
def root():
    return {"message": "SmartProposal Backend is running"}
