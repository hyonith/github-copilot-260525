from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# 刻意埋入的錯誤：CONFIG 中未定義 SQLITE_PATH。
CONFIG = {
    "DB_TIMEOUT": 30,
    "DB_ECHO": False,
}


def build_dsn() -> str:
    # 錯誤根源：CONFIG 中不含 "SQLITE_PATH"，執行時會立刻拋出 KeyError。
    db_path = CONFIG["SQLITE_PATH"]
    return f"sqlite:///{db_path}"
