import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI", "http://127.0.0.1:8888/callback")
    CACHE_PATH = os.getenv("CACHE_PATH", ".spotify_token_cache")
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", "100"))
    SCOPES = (
        "playlist-read-private "
        "playlist-read-collaborative "
        "playlist-modify-private "
        "playlist-modify-public"
    )

    @classmethod
    def validate(cls):
        required = ["CLIENT_ID", "CLIENT_SECRET", "REDIRECT_URI"]
        missing = [attr for attr in required if not getattr(cls, attr)]
        if missing:
            raise ValueError(f"Missing required env vars: {', '.join(missing)}")
