import os
import time
from pathlib import Path

# -------- cleanup function 
def cleanup_temp_files(temp_dir: str, hours: int):
    now = time.time()
    max_age_seconds = hours * 3600
    temp_path = Path(temp_dir)

    for file in temp_path.iterdir():
        if file.is_file():
            file_age = now - file.stat().st_mtime
            if file_age > max_age_seconds:
                file.unlink()


# -------- test --------
def setup_test_environment():
    Path("temp").mkdir(exist_ok=True)
    Path("data").mkdir(exist_ok=True)

   
    main_file = Path("data/main_file.txt")
    main_file.write_text("IMPORTANT DATA")

    
    old_temp = Path("temp/old_temp.txt")
    old_temp.write_text("OLD TEMP FILE")
    old_time = time.time() - 3 * 3600  # 3 ساعت قبل
    os.utime(old_temp, (old_time, old_time))

    
    new_temp = Path("temp/new_temp.txt")
    new_temp.write_text("NEW TEMP FILE")

    print("Test environment created.\n")


def run_test():
    cleanup_temp_files("temp", hours=2)

    print("After cleanup:\n")

    print("temp folder:")
    for f in Path("temp").iterdir():
        print(" -", f.name)

    print("\ndata folder:")
    for f in Path("data").iterdir():
        print(" -", f.name)

    # assertions 
    assert not Path("temp/old_temp.txt").exists(), " old_temp.txt should be deleted"
    assert Path("temp/new_temp.txt").exists(), " new_temp.txt should NOT be deleted"
    assert Path("data/main_file.txt").exists(), " main_file.txt should NOT be deleted"

    print("\n TEST PASSED SUCCESSFULLY")


if __name__ == "__main__":
    setup_test_environment()
    run_test()
