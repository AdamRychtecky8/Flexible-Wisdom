# notebooks/_utils.py (you’ll create this soon)
from pathlib import Path
import os
from dotenv import load_dotenv

def get_data_dir() -> Path:
    load_dotenv()  # loads .env from repo root
    data_dir = os.getenv("DATA_DIR")
    if not data_dir or not Path(data_dir).exists():
        raise FileNotFoundError(
            "DATA_DIR is not set or path does not exist. "
            "Create a .env file (see .env.example) and set DATA_DIR to your OneDrive data path."
        )
    return Path(data_dir)
