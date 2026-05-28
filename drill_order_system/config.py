from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 刻意埋入的錯誤：CONFIG 中未定義 SQLITE_PATH。
CONFIG = {
    "DB_TIMEOUT": 30,
    "DB_ECHO": False,
}


def build_dsn() -> str:
    print("正在獲取資料庫路徑...")  
    # str(BASE_DIR / "app/users.db") --- IGNORE ---
    return str(CONFIG["SQLITE_PATH"])
