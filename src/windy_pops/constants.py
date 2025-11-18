from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent / "data"
SECRETS_PATH = Path(__file__).parent.parent.parent / "secrets.ini"

LOCATIONS = {"shoreham_beach": {"lat": 50.827274, "lon": -0.271525}}

LIGHTNING_LIMIT = 50
MAX_WIND_SPEED = 30
MIN_WIND_SPEED = 10

MINIMUM_WINDOW_DURATION = 90
INTERVAL_LENGTH_MINUTES = 180
