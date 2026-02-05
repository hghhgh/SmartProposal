import os
import time
from pathlib import Path

def cleanup_temp_files(temp_dir: str, hours: int):
    """
    Delete temp files older than `hours` hours from temp_dir
    """
    now = time.time()
    max_age_seconds = hours * 3600

    temp_path = Path(temp_dir)

    if not temp_path.exists():
        print(f"Directory not found: {temp_dir}")
        return

    for file in temp_path.iterdir():
        if file.is_file():
            file_age = now - file.stat().st_mtime

            if file_age > max_age_seconds:
                try:
                    file.unlink()
                    print(f"Deleted: {file.name}")
                except Exception as e:
                    print(f"Failed to delete {file.name}: {e}")


if __name__ == "__main__":
    TEMP_DIR = "temp"   
    HOURS = 2           

    cleanup_temp_files(TEMP_DIR, HOURS)
