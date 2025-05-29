
import os
from dotenv import load_dotenv
load_dotenv()

DB_URL = os.getenv("BANK_DB_URL", "sqlite:///bank.db")
LOG_LEVEL = os.getenv("BANK_LOG_LEVEL", "INFO")
