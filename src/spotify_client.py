"""Spotify API client wrapper - COMPLETE VERSION."""
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import Config
from utils import chunked
import datetime as dt

class SpotifyClient:
    def __init__(self):
        print("Authenticating with Spotify...")
        self.sp = self._authenticate()
        print("Spotify authenticated!")
    
    def _authenticate(self) -> spotipy.Spotify:
        """Create authenticated Spotify client."""
        auth_manager = SpotifyOAuth(
            scope=Config.SCOPES,
            client_id=Config.CLIENT_ID,
            client_secret=Config.CLIENT_SECRET,
            redirect_uri=Config.REDIRECT_URI,
            open_browser=True,
            cache_path=Config.CACHE_PATH
        )
        return spotipy.Spotify(auth_manager=auth_manager)
    
    def get_playlist_items(self, playlist_id: str) -> list:
        """Fetch all items from playlist with pagination."""
        print(f"Fetching playlist items...")
        items = []
        offset = 0
        
        while True:
            page = self.sp.playlist_items(
                playlist_id,
                offset=offset,
                additional_types=("track", "episode"),
                fields="items(track(uri,is_local)),next,total"
            )
            items.extend(page.get("items", []))
            if not page.get("next"):
                break
            offset += len(page["items"])
        
        print(f"Found {len(items)} total items")
        return items
    
    def get_playlist_metadata(self, playlist_id: str) -> dict:
        """Get playlist metadata."""
        return self.sp.playlist(
            playlist_id, 
            fields="name,public,owner(id),external_urls"
        )
    
    def move_track(self, playlist_id: str, from_pos: int, to_pos: int) -> str:
        """Move single track from from_pos to to_pos (FIXED)."""
        print(f"{from_pos} → {to_pos}", end=" ")
        
        # Spotify API: range_start + insert_before/insert_after
        if to_pos < from_pos:
            result = self.sp.playlist_reorder_items(
                playlist_id, 
                range_start=from_pos,
                insert_before=to_pos
            )
        else:
            result = self.sp.playlist_reorder_items(
                playlist_id, 
                range_start=from_pos,
                insert_after=to_pos
            )
        print("Good")
        return result['snapshot_id']
    
    def get_current_user(self) -> dict:
        """Get current user info."""
        return self.sp.current_user()
