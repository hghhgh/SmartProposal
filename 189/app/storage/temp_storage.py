from pathlib import Path
import time

BASE_DIR = Path("tmp/encrypted")
BASE_DIR.mkdir(parents=True, exist_ok=True)

MAX_AGE = 24 * 3600  # 24 ساعت

def save_temp_file(file_id: str, data: bytes):
    path = BASE_DIR / file_id
    with open(path, "wb") as f:
        f.write(data)

def cleanup():
    now = time.time()
    for f in BASE_DIR.iterdir():
        if now - f.stat().st_mtime > MAX_AGE:
            f.unlink()
