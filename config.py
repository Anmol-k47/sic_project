"""
WorkMatch Pro v4 — Configuration & Constants (Live Data Edition)
"""
import os


def load_env():
    """Load .env file if present."""
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())


load_env()

# Database
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workmatch_v4.db")
CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "live_data_cache.json")

# API Credentials (from env or .env file)
ADZUNA_APP_ID = os.environ.get("ADZUNA_APP_ID", "")
ADZUNA_APP_KEY = os.environ.get("ADZUNA_APP_KEY", "")
DATA_GOV_KEY = os.environ.get("DATA_GOV_API_KEY", "")

# SBERT model name
SBERT_MODEL = "all-MiniLM-L6-v2"

# CNN hyperparameters
CNN_MAX_WORDS = 4000
CNN_MAX_LEN = 32
CNN_EPOCHS = 60
CNN_BATCH_SIZE = 32
CNN_EMBED_DIM = 128

# Matching thresholds
SBERT_WEIGHT = 0.84
CAT_BONUS_WEIGHT = 0.12
LIVE_BONUS_WEIGHT = 0.04
CNN_CONFIDENCE_THRESHOLD = 0.55
MIN_MATCH_SCORE = 0.32
FUZZY_THRESHOLD = 78

# Cache TTL (seconds) — 6 hours
CACHE_TTL = 21600
CACHE_MAX_SIZE = 500
