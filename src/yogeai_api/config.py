import os
from dotenv import load_dotenv

load_dotenv()

MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "15"))
TOP_K_DEFAULT = int(os.getenv("TOP_K_DEFAULT", "4"))
