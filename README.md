# Spotify Playlist Shuffler 🎶

**Shuffle any Spotify playlist with one click!** Creates a perfectly randomized copy while preserving duplicates.

## ✨ Features
- ✅ Handles playlists of **any size** (pagination)
- ✅ Skips local files automatically
- ✅ Preserves **exact duplicate order**
- ✅ Configurable via `.env`
- ✅ Token caching (no repeated logins)

## 🛠️ Quick Setup (2 minutes)

### 1. Get Spotify App Credentials
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create app → Copy **Client ID** & **Client Secret**
3. Add **Redirect URI**: `http://localhost:8888/callback`

### 2. Install & Run
```
# Clone/Download this repo
git clone <repo> && cd shuffle_playlist

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Copy & edit config
cp .env.example .env
# Open .env and paste your Spotify credentials
```

### 3. First Run (Spotify Login)
```
python main.py
```

- Browser opens → **Login to Spotify**
- Authorize the app
- **Token saved** → No more logins needed!

## 🚀 Usage
```
=== Spotify Playlist Shuffler ===
Playlist URL or ID: https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M
Optional seed (Enter = random):

Loading playlist...
✅ Done!
New Playlist: Today's Top Hits (Shuffled 2025-12-04 18:30)
Items Added: 124
Skipped (local): 0
Skipped (other): 0
URL: https://open.spotify.com/playlist/...
```

**Works with:**
- Full URLs: `https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M`
- Short IDs: `37i9dQZF1DXcBWIGoYBM5M`

## 🔧 Configuration (.env)
```
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
CACHE_PATH=.spotify_token_cache
BATCH_SIZE=100
```


## 📁 Project Structure
```
shuffle_playlist/
├── main.py # 🚪 Entry point
├── requirements.txt # 📦 Dependencies
├── .env.example # 📋 Config template
├── .env # 🔑 Your secrets
└── src/ # 🏗️ Source code
├── init.py
├── config.py
├── utils.py
├── spotify_client.py
└── playlist_handler.py
```


## 🐛 Troubleshooting
```
| Problem | Solution |
|---------|----------|
| `Missing required env vars` | Edit `.env` with your Spotify credentials |
| `No valid tracks found` | Playlist has only local files |
| Browser not opening | Login manually at the shown URL |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
```
## 🙌 Advanced Usage

**Same shuffle every time:**
```
python main.py

Enter seed: 42
```

**Custom batch size:**
```
BATCH_SIZE=50 # For huge playlists
```


## 📄 License
MIT - Use it anywhere!

## ❤️ Made With
- [Spotipy](https://spotipy.readthedocs.io/) - Spotify API
- [Python-dotenv](https://pypi.org/project/python-dotenv/) - Config management

**Questions?** Open an issue or ping me! 🎉