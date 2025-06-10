from flask import Flask, jsonify, request
import requests
from datetime import datetime, timedelta
app = Flask(__name__)
CORS(app)  
from flask_cors import CORS
CORS(app, origins=["https://music-dashboard-three-woad.vercel.app/"])

ARTISTS = [
    {"label": "Ed Sheeran", "id": 3648},
    {"label": "The Weeknd", "id": 3852},
    {"label": "Tones And I", "id": 1410939},
    {"label": "Imagine Dragons", "id": 4132},
    {"label": "Harry Styles", "id": 558681},
    {"label": "Mark Ronson", "id": 1759},
    {"label": "Bruno Mars", "id": 3501},
    {"label": "Luis Fonsi", "id": 1434},
    {"label": "Daddy Yankee", "id": 1802},
    {"label": "Justin Bieber", "id": 3479},
    {"label": "The Kid LAROI", "id": 1333786},
    {"label": "Glass Animals", "id": 3656},
    {"label": "The Chainsmokers", "id": 4796},
    {"label": "Halsey", "id": 5109},
    {"label": "Miley Cyrus", "id": 2619},
    {"label": "Lewis Capaldi", "id": 550208},
    {"label": "Daft Punk", "id": 170},
    {"label": "Taylor Swift", "id": 2762},
    {"label": "Dua Lipa", "id": 5381},
    {"label": "Drake", "id": 3380},
    {"label": "Christina Perri", "id": 3684},
    {"label": "OneRepublic", "id": 2796},
    {"label": "Juice WRLD", "id": 921966},
    {"label": "Justin Beiber", "id": 3476},  
    {"label": "Coldplay", "id": 439},
    {"label": "Lady Gaga", "id": 3188},
    {"label": "Shawn Mendes", "id": 4934},
    {"label": "Camila Cabello", "id": 454302},  
    {"label": "Pritam", "id": 127583},
    {"label": "Arijit Singh", "id": 303406},
    {"label": "Shreya Ghoshal", "id": 23385},
    {"label": "Rajat Nagpal", "id": 1349325},
    {"label": "Jubin Nautiyal", "id": 785271},
    {"label": "Tanishk Bagchi", "id": 388884},
    {"label": "Dhvani Bhanushali", "id": 874442},
    {"label": "Alka Yagnik", "id": 267405},
    {"label": "Sonu Nigam", "id": 108808}
]

MOODS = [
    {"label": "celebratory", "id": 504927},
    {"label": "fun", "id": 504978},
    {"label": "affectionate", "id": 504909},
]

ACTIVITIES = [
    {"label": "partying", "id": 504876},
    {"label": "dancy", "id": 504872},
    {"label": "drinking", "id": 504886},
    {"label": "urban", "id": 504878},
]







REFRESH_TOKEN = "CdbzEeHvYZKK372srNTsHTuHK1kdexWeChihqXtFwQDHMyH8X4zkL9BDUUNtMs7n"

def refresh_access_token(refresh_token=REFRESH_TOKEN):
    url = "https://api.chartmetric.com/api/token"
    headers = {"Content-Type": "application/json"}
    data = {"refreshtoken": refresh_token}
    response = requests.post(url, json=data, headers=headers)

    print("=== TOKEN DEBUG ===")
    print("Status Code:", response.status_code)
    print("Token Response:", response.text)

    if response.status_code == 200:
        return response.json().get('token')
    return None
def extract_artist_name(t):
    artist = ""
    if "artist" in t and t["artist"]:
        artist = t["artist"][0].get("name", "")
    elif "artist_names" in t and t["artist_names"]:
        artist = t["artist_names"][0]
    elif "artists" in t and t["artists"]:
        artist = t["artists"][0].get("name", "")
    return artist


def fetch_top_tracks(api_token, params):
    url = "https://api.chartmetric.com/api/charts/spotify"
    headers = {"Authorization": f"Bearer {api_token}"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get('obj', {}).get('data', [])
    return []
def get_genres(api_token):
    url = "https://api.chartmetric.com/api/genre"
    headers = {"Authorization": f"Bearer {api_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('obj', [])
    else:
        print("Error fetching genres:", response.status_code, response.text)
        return []
@app.route("/api/artists", methods=["GET"])
def get_artists_api():
    search = request.args.get("search", "").lower()
    if search:
        filtered = [a for a in ARTISTS if search in a["label"].lower()]
    else:
        filtered = ARTISTS
    return jsonify(filtered)


def fetch_tracks_by_genre(api_token, genre_id, sort_column="score", sort_order_desc=True, limit=50):
    url = "https://api.chartmetric.com/api/track/list/filter"
    headers = {"Authorization": f"Bearer {api_token}"}
    params = [
        ("genres[]", genre_id),
        ("sortColumn", sort_column),
        ("sortOrderDesc", str(sort_order_desc).lower()),  # "true" or "false"
        ("limit", str(limit))
    ]
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching tracks:", response.status_code, response.text)
        return []

def get_moods(api_token):
    url = "https://api.chartmetric.com/api/mood"
    headers = {"Authorization": f"Bearer {api_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('obj', [])
    else:
        print("Error fetching moods:", response.status_code, response.text)
        return []

def get_activities(api_token):
    url = "https://api.chartmetric.com/api/activity"
    headers = {"Authorization": f"Bearer {api_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('obj', [])
    else:
        print("Error fetching activities:", response.status_code, response.text)
        return []
@app.route("/api/moods", methods=["GET"])
def get_moods_api():
    search = request.args.get("search", "").lower()
    if search:
        filtered = [m for m in MOODS if search in m["label"].lower()]
    else:
        filtered = MOODS
    return jsonify(filtered)

@app.route("/api/activities", methods=["GET"])
def get_activities_api():
    search = request.args.get("search", "").lower()
    if search:
        filtered = [a for a in ACTIVITIES if search in a["label"].lower()]
    else:
        filtered = ACTIVITIES
    return jsonify(filtered)


@app.route("/api/tracks-by-mood", methods=["GET"])
def get_tracks_by_mood_api():
    mood_id = request.args.get("mood_id", "")
    sort_column = request.args.get("sortColumn", "score")
    sort_order_desc = request.args.get("sortOrderDesc", "true").lower() == "true"
    if not mood_id:
        return jsonify([])
    api_token = refresh_access_token()
    if not api_token:
        return jsonify([])
    url = "https://api.chartmetric.com/api/track/list/filter"
    headers = {"Authorization": f"Bearer {api_token}"}
    params = [
        ("moods[]", mood_id),
        ("sortColumn", sort_column),
        ("limit", "50"),
        ("sortOrderDesc", str(sort_order_desc).lower()),
    ]
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        tracks = []
        for t in data.get("obj", []):
            artist = extract_artist_name(t)
            release_date = ""
            if "release_dates" in t and t["release_dates"]:
                release_date = t["release_dates"][0][:10]
            elif "album" in t and t["album"]:
                release_date = t["album"][0].get("release_date", "")[:10]
            latest = t.get("latest", {})
            tracks.append({
                "track": t.get("name", ""),
                "artist": artist,
                "release_date": release_date,
                "streams": latest.get("spotify_plays", t.get("plays", t.get("score", 0))),
                "playlist_count": latest.get("spotify_playlist_count"),
                "popularity": latest.get("spotify_popularity"),
                "playlist_reach": latest.get("spotify_playlist_total_reach"),
                "score": t.get("score", 0),
            })
        return jsonify(tracks)
    else:
        print("Error fetching tracks:", response.status_code, response.text)
        return jsonify([])

@app.route("/api/tracks-by-activity", methods=["GET"])
def get_tracks_by_activity_api():
    activity_id = request.args.get("activity_id", "")
    sort_column = request.args.get("sortColumn", "score")
    sort_order_desc = request.args.get("sortOrderDesc", "true").lower() == "true"
    if not activity_id:
        return jsonify([])
    api_token = refresh_access_token()
    if not api_token:
        return jsonify([])
    url = "https://api.chartmetric.com/api/track/list/filter"
    headers = {"Authorization": f"Bearer {api_token}"}
    params = [
        ("activities[]", activity_id),
        ("sortColumn", sort_column),
        ("limit", "50"),
        ("sortOrderDesc", str(sort_order_desc).lower()),
    ]
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        tracks = []
        for t in data.get("obj", []):
            artist = extract_artist_name(t)
            release_date = ""
            if "release_dates" in t and t["release_dates"]:
                release_date = t["release_dates"][0][:10]
            elif "album" in t and t["album"]:
                release_date = t["album"][0].get("release_date", "")[:10]
            latest = t.get("latest", {})
            tracks.append({
                "track": t.get("name", ""),
                "artist": artist,
                "release_date": release_date,
                "streams": latest.get("spotify_plays", t.get("plays", t.get("score", 0))),
                "playlist_count": latest.get("spotify_playlist_count"),
                "popularity": latest.get("spotify_popularity"),
                "playlist_reach": latest.get("spotify_playlist_total_reach"),
                "score": t.get("score", 0),
            })
        return jsonify(tracks)
    else:
        print("Error fetching tracks:", response.status_code, response.text)
        return jsonify([])



@app.route("/api/top-tracks", methods=["GET"])
def get_top_tracks():
    sort_order = request.args.get("order", "desc")
    api_token = refresh_access_token()
    if not api_token:
        return jsonify({"error": "Could not refresh token"}), 500

    yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    params = {
        "date": yesterday,
        "country_code": "WW",
        "interval": "daily",
        "type": "plays"
        
    }
    raw_tracks = fetch_top_tracks(api_token, params)
  
    tracks = []
    for t in raw_tracks[:50]:
        tracks.append({
            "track": t.get("name", ""),  
            "artist": t.get("artist_names", [""])[0], 
            "release_date": (t.get("release_dates", [""])[0][:10] if t.get("release_dates") else ""),
            "streams": t.get("plays", 0),
            "playlist_count": t.get("playlist_count", 0),
            "popularity": t.get("popularity", 0),
            "playlist_reach": t.get("playlist_reach", 0),
           

        })
    tracks = sorted(tracks, key=lambda t: t.get("streams", 0), reverse=(sort_order=="desc"))
    return jsonify(tracks)
@app.route("/api/genres", methods=["GET"])
def get_genres_api():
    search = request.args.get("search", "").lower()
    api_token = refresh_access_token()
    if not api_token:
        return jsonify([])
    genres = get_genres(api_token)
    if search:
        genres = [g for g in genres if search in g['name'].lower()]
    return jsonify([{"label": g["name"], "id": g["id"]} for g in genres])

@app.route("/api/tracks-by-genres", methods=["GET"])
def get_tracks_by_genres_api():
    genre_ids = request.args.get("genre_ids", "")
    sort_column = request.args.get("sortColumn", "score")
    sort_order_desc = request.args.get("sortOrderDesc", "true").lower() == "true"
    if not genre_ids:
        return jsonify([])
    genre_id_list = [gid for gid in genre_ids.split(",") if gid]
    api_token = refresh_access_token()
    if not api_token:
        return jsonify([])
    all_tracks = []
    for gid in genre_id_list:
        track_data = fetch_tracks_by_genre(api_token, gid, sort_column, sort_order_desc)
        if track_data and track_data.get("obj"):
            for t in track_data["obj"]:
                artist = extract_artist_name(t)
                release_date = ""
                if "release_dates" in t and t["release_dates"]:
                    release_date = t["release_dates"][0][:10]
                elif "album" in t and t["album"]:
                    release_date = t["album"][0].get("release_date", "")[:10]
                streams = t.get("plays", t.get("score", 0))
                track = {
                    "track": t.get("name", ""),
                    "artist": artist,
                    "release_date": release_date,
                    "streams": streams
                }
                all_tracks.append(track)
    track_map = {}
    for t in all_tracks:
        name = t["track"]
        if name not in track_map or t["streams"] > track_map[name]["streams"]:
            track_map[name] = t
    sorted_tracks = sorted(track_map.values(), key=lambda t: t["streams"], reverse=True)
    return jsonify(sorted_tracks[:50])
@app.route("/api/tracks-by-artist", methods=["GET"])
def get_tracks_by_artist_api():
    artist_id = request.args.get("artist_id", "")
    sort_column = request.args.get("sortColumn", "score")
    sort_order_desc = request.args.get("sortOrderDesc", "true").lower() == "true"
    if not artist_id:
        return jsonify([])
    api_token = refresh_access_token()
    if not api_token:
        return jsonify([])
    url = "https://api.chartmetric.com/api/track/list/filter"
    headers = {"Authorization": f"Bearer {api_token}"}
    params = [
        ("artists[]", artist_id),
        ("sortColumn", sort_column),
        ("limit", "50"),
        ("sortOrderDesc", str(sort_order_desc).lower()),
    ]
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        tracks = []
        for t in data.get("obj", []):
            artist = extract_artist_name(t)
            release_date = ""
            if "release_dates" in t and t["release_dates"]:
                release_date = t["release_dates"][0][:10]
            elif "album" in t and t["album"]:
                release_date = t["album"][0].get("release_date", "")[:10]
            latest = t.get("latest", {})
            tracks.append({
                "track": t.get("name", ""),
                "artist": artist,
                "release_date": release_date,
                "streams": latest.get("spotify_plays", t.get("plays", t.get("score", 0))),
                "playlist_count": latest.get("spotify_playlist_count"),
                "popularity": latest.get("spotify_popularity"),
                "playlist_reach": latest.get("spotify_playlist_total_reach"),
                "score": t.get("score", 0),
            })
        return jsonify(tracks)
    else:
        print("Error fetching tracks:", response.status_code, response.text)
        return jsonify([])

@app.route("/api/tracks-by-filters", methods=["GET"])
def get_tracks_by_filters():
    genre_ids = request.args.get("genre_ids", "")
    artist_id = request.args.get("artist_id", "")
    mood_ids = request.args.get("mood_ids", "")
    activity_ids = request.args.get("activity_ids", "")
    sort_column = request.args.get("sortColumn", "score")
    sort_order_desc = request.args.get("sortOrderDesc", "true").lower() == "true"
    api_token = refresh_access_token()
    if not api_token:
        return jsonify([])

    url = "https://api.chartmetric.com/api/track/list/filter"
    headers = {"Authorization": f"Bearer {api_token}"}
    params = []

    if genre_ids:
        for gid in genre_ids.split(","):
            params.append(("genres[]", gid))
    if mood_ids:
        for mid in mood_ids.split(","):
            params.append(("moods[]", mid))
    if activity_ids:
        for aid in activity_ids.split(","):
            params.append(("activities[]", aid))
    if artist_id:
        params.append(("artists[]", artist_id))
    params.extend([
        ("sortColumn", sort_column),
        ("limit", "50"),
        ("sortOrderDesc", str(sort_order_desc).lower()),
    ])
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        tracks = []
        for t in data.get("obj", []):
            artist = extract_artist_name(t)
            release_date = ""
            if "release_dates" in t and t["release_dates"]:
                release_date = t["release_dates"][0][:10]
            elif "album" in t and t["album"]:
                release_date = t["album"][0].get("release_date", "")[:10]
            latest = t.get("latest", {})
            tracks.append({
                "track": t.get("name", ""),
                "artist": artist,
                "release_date": release_date,
                "streams": latest.get("spotify_plays", t.get("plays", t.get("score", 0))),
                "playlist_count": latest.get("spotify_playlist_count"),
                "popularity": latest.get("spotify_popularity"),
                "playlist_reach": latest.get("spotify_playlist_total_reach"),
                "score": t.get("score", 0),
            })
        return jsonify(tracks)
    else:
        print("Error fetching tracks:", response.status_code, response.text)
        return jsonify([])


@app.route("/api/tracks-by-release-date", methods=["GET"])
def get_tracks_by_release_date():
    filter_option = request.args.get("filter_option", "")
    sort_column = request.args.get("sortColumn", "score")
    sort_order_desc = request.args.get("sortOrderDesc", "true").lower() == "true"
    api_token = refresh_access_token()
    if not api_token:
        return jsonify([])
    end_date = datetime.today()
    if filter_option == "Last 1 Week":
        start_date = end_date - timedelta(days=7)
    elif filter_option == "Last 1 Month":
        start_date = end_date - timedelta(days=30)
    elif filter_option == "Last 1 Year":
        start_date = end_date - timedelta(days=365)
    else:
        start_date = end_date - timedelta(days=7)
    url = "https://api.chartmetric.com/api/track/list/filter"
    headers = {"Authorization": f"Bearer {api_token}"}
    params = [
        ("min_release_date", start_date.strftime('%Y-%m-%d')),
        ("max_release_date", end_date.strftime('%Y-%m-%d')),
        ("sortColumn", sort_column),
        ("limit", "50"),
        ("sortOrderDesc", str(sort_order_desc).lower()),
    ]
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        tracks = []
        for t in data.get("obj", []):
            artist = extract_artist_name(t)
            release_date = ""
            if "release_dates" in t and t["release_dates"]:
                release_date = t["release_dates"][0][:10]
            elif "album" in t and t["album"]:
                release_date = t["album"][0].get("release_date", "")[:10]
            latest = t.get("latest", {})
            tracks.append({
                "track": t.get("name", ""),
                "artist": artist,
                "release_date": release_date,
                "streams": latest.get("spotify_plays", t.get("plays", t.get("score", 0))),
                "playlist_count": latest.get("spotify_playlist_count"),
                "popularity": latest.get("spotify_popularity"),
                "playlist_reach": latest.get("spotify_playlist_total_reach"),
                "score": t.get("score", 0),
            })
        return jsonify(tracks)
    else:
        print("Error fetching tracks:", response.status_code, response.text)
        return jsonify([])



@app.route("/")
def home():
    return "Backend is running!"

if __name__ == "__main__":
    app.run(port=5000, debug=True)
