from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "user.db"


def get_db_path() -> Path:
	# Intentional bug: missing SQLITE_PATH causes runtime KeyError.
	cfg = {"DB_TIMEOUT": 30}
	return Path(cfg["SQLITE_PATH"])
