#!/usr/bin/env python3
"""
Spotify Playlist Shuffler (10K+ Tracks) - INDUSTRIAL STRENGTH
Multi-pass shuffling for massive playlists up to 10,000+ tracks.
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import time
import re
import os
from urllib.parse import urlparse

def extract_playlist_id(url_or_id):
    """Extract Spotify playlist ID from URL or return as-is."""
    if 'spotify.com/playlist/' in url_or_id:
        return re.search(r'playlist/([a-zA-Z0-9]+)', url_or_id).group(1)
    return url_or_id

def setup_spotify():
    """Authenticate and return Spotify client with fallback."""
    scope = 'playlist-modify-public playlist-modify-private playlist-read-private'
    
    client_id = os.getenv('SPOTIPY_CLIENT_ID')
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI', 'http://127.0.0.1:8888/callback')
    
    if not client_id or not client_secret:
        print("ERROR: Missing Spotify API credentials!")
        print("Set SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI")
        exit(1)
    
    try:
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope=scope
            )
        )
        sp.current_user()
        return sp
    except Exception as e:
        print(f"Auth failed: {e}")
        exit(1)

def get_playlist_tracks(sp, playlist_id):
    """Fetch all valid track URIs from playlist."""
    tracks = []
    results = sp.playlist_items(playlist_id, fields='items(track(uri))')
    
    for item in results['items']:
        if item['track'] and item['track']['uri']:
            tracks.append(item['track']['uri'])
    
    return tracks

def mega_shuffle(sp, playlist_id, n_tracks, passes=5):
    """Industrial-strength shuffle: Multiple full passes for 10K+ tracks."""
    print(f"INDUSTRIAL SHUFFLE: {n_tracks} tracks, {passes} passes")
    total_moves = 0
    
    for pass_num in range(1, passes + 1):
        print(f"\nPASS {pass_num}/{passes} ({n_tracks} tracks)...")
        moves = 0
        
        # Forward pass: Move random track to front
        for i in range(n_tracks):
            try:
                target = random.randint(0, n_tracks - 1)
                sp.playlist_reorder_items(
                    playlist_id, 
                    range_start=target, 
                    insert_before=0
                )
                moves += 1
                total_moves += 1
                
                if moves % 50 == 0:
                    print(f"   {moves}/{n_tracks} moves ✓")
                
                time.sleep(0.15)  # Rate limit
                
            except Exception as e:
                print(f"Move {i+1} failed: {str(e)[:40]}")
                continue
        
        print(f"Pass {pass_num}: {moves} moves complete")
        time.sleep(1)  # Pass cooldown
    
    print(f"\nMEGA SHUFFLE COMPLETE: {total_moves} TOTAL MOVES!")
    return total_moves

def main():
    print("=== Spotify Mega Shuffler (10K+ Tracks) ===")
    
    playlist_input = input("Playlist URL or ID: ").strip()
    playlist_id = extract_playlist_id(playlist_input)
    
    seed_input = input("Optional seed (Enter = random): ").strip()
    if seed_input:
        random.seed(int(seed_input))
    
    print("Authenticating...")
    sp = setup_spotify()
    print("Spotify authenticated!")
    
    print("Fetching playlist...")
    playlist_info = sp.playlist(playlist_id)
    print(f"Target: {playlist_info['name']} ({len(playlist_info['tracks']['items'])} tracks)")
    
    tracks = get_playlist_tracks(sp, playlist_id)
    print(f"{len(tracks)} valid tracks ready")
    
    if len(tracks) == 0:
        print("No tracks!")
        return
    
    # Auto-select passes based on size
    passes = max(3, min(10, len(tracks) // 100 + 3))
    confirm = input(f"Shuffle with {passes} passes? (y/n): ").lower()
    if confirm != 'y':
        return
    
    print("Starting MEGA SHUFFLE...")
    total_moves = mega_shuffle(sp, playlist_id, len(tracks), passes)
    
    print("\nMEGA SHUFFLE FINISHED!")
    print(f"- Playlist: {playlist_info['name']}")
    print(f"- Tracks: {len(tracks):,}")
    print(f"- Total Moves: {total_moves:,}")
    print(f"📱 {playlist_info['external_urls']['spotify']}")

if __name__ == "__main__":
    main()
