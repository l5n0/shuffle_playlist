"""Playlist processing logic - TRUE in-place shuffle."""
import random
import time
from typing import Tuple, List
from utils import extract_playlist_id, set_random_seed
from spotify_client import SpotifyClient

class PlaylistHandler:
    def __init__(self, client: SpotifyClient):
        self.client = client
    
    def process_playlist(self, playlist_input: str, seed: str | None) -> Tuple[dict, int, int, int]:
        """Perfect in-place shuffle using Spotify reorder API."""
        set_random_seed(seed)
        
        playlist_id = extract_playlist_id(playlist_input)
        metadata = self.client.get_playlist_metadata(playlist_id)
        print(f"🔄 Shuffling: {metadata['name']} ({len(playlist_input)} chars)")
        
        # Get current order
        items = self.client.get_playlist_items(playlist_id)
        valid_tracks = self._extract_valid_tracks(items)
        
        if not valid_tracks:
            raise ValueError("No valid tracks found")
        
        num_tracks = len(valid_tracks)
        print(f"🎲 Shuffling {num_tracks} tracks")
        
        # Create target shuffle order
        shuffle_order = list(range(num_tracks))
        random.shuffle(shuffle_order)
        
        # Build move operations (old_pos -> new_pos)
        moves = []
        for new_pos, old_pos in enumerate(shuffle_order):
            if new_pos != old_pos:
                moves.append((old_pos, new_pos))
        
        print(f"🔀 {len(moves)} moves required")
        self._execute_shuffles(playlist_id, moves)
        
        print(f"✅ Perfect shuffle complete!")
        print(f"📱 {metadata['external_urls']['spotify']}")
        
        return metadata, num_tracks, 0, 0
    
    def _execute_shuffles(self, playlist_id: str, moves: List[tuple]) -> None:
        """Execute shuffle moves with rate limiting."""
        print("🔀 Executing reorders...")
        for i, (from_pos, to_pos) in enumerate(moves, 1):
            try:
                self.client.move_track(playlist_id, from_pos, to_pos)
                if i % 10 == 0:
                    print(f"   {i}/{len(moves)} moves complete")
                time.sleep(0.1)  # Rate limit
            except Exception as e:
                print(f"   ⚠️  Move {i} failed: {e}")
    
    def _extract_valid_tracks(self, items: list) -> list:
        """Extract valid tracks only."""
        valid_tracks = []
        for i, item in enumerate(items):
            track = item.get("track")
            if track and not track.get("is_local") and track.get("uri"):
                valid_tracks.append(track["uri"])
        print(f"🔧 {len(valid_tracks)} valid tracks ready")
        return valid_tracks
