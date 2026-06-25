"""Application configuration."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SAMPLE_DIR = DATA_DIR / "sample"
TEMPLATE_DIR = DATA_DIR / "templates"
EXPORT_DIR = DATA_DIR / "exports"
ASSETS_DIR = BASE_DIR / "assets"
DB_PATH = DATA_DIR / "election_portal.db"

DATABASE_URL = f"sqlite:///{DB_PATH}"
# PostgreSQL: postgresql://user:pass@localhost:5432/election_portal

REFRESH_INTERVAL = 15  # seconds
MARGIN_ALERT_THRESHOLD = 500
DEFAULT_ELECTION_YEAR = 2024

ELECTION_TYPES = [
    "Parliamentary",
    "Assembly",
    "Municipal",
    "Panchayat",
    "Local Body",
]

USER_ROLES = {
    "super_admin": "Super Admin",
    "election_officer": "Election Officer",
    "analyst": "Analyst",
    "public": "Public User",
}

PARTY_COLORS = {
    "National Democratic Alliance": "#1e3a8a",
    "United Progressive Alliance": "#059669",
    "Aam Aadmi Party": "#0ea5e9",
    "Dravida Munnetra Kazhagam": "#dc2626",
    "All India Anna Dravida Munnetra Kazhagam": "#16a34a",
    "Bharatiya Janata Party": "#f59e0b",
    "Indian National Congress": "#2563eb",
    "Independent": "#6b7280",
}
