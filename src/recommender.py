import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Recommend the top-k songs for a user using the same scoring logic as score_song()."""
        user_prefs = {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
            "preferred_acousticness": 0.8 if user.likes_acoustic else 0.2,
        }

        scored = []
        for song in self.songs:
            song_prefs = {
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "tempo_bpm": song.tempo_bpm,
                "valence": song.valence,
                "danceability": song.danceability,
                "acousticness": song.acousticness,
            }
            score, _ = score_song(user_prefs, song_prefs)
            scored.append((song, score))

        scored.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a short explanation of why this song was recommended."""
        user_prefs = {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
            "preferred_acousticness": 0.8 if user.likes_acoustic else 0.2,
        }

        song_prefs = {
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "tempo_bpm": song.tempo_bpm,
            "valence": song.valence,
            "danceability": song.danceability,
            "acousticness": song.acousticness,
        }

        _, reasons = score_song(user_prefs, song_prefs)
        return "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Load all songs from a CSV file into a list of dictionaries."""
    songs: List[Dict] = []
    with open(csv_path, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            song = {
                'id': int(row['id']),
                'title': row['title'].strip(),
                'artist': row['artist'].strip(),
                'genre': row['genre'].strip(),
                'mood': row['mood'].strip(),
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness']),
            }
            songs.append(song)
    return songs

def score_song(
    user_prefs: Dict,
    song: Dict,
    genre_weight: float = 2.0,
    mood_weight: float = 1.0,
    numeric_feature_weights: Optional[Dict[str, float]] = None,
) -> Tuple[float, List[str]]:
    """Score one song by matching genre, mood, and closeness to the user's preferred features.

    The optional weight parameters make it easy to run experiments on how different musical
    signals affect the final ranking.
    """
    score = 0.0
    reasons: List[str] = []

    if song.get("genre") == user_prefs.get("favorite_genre"):
        score += genre_weight
        reasons.append(f"genre match (+{genre_weight})")

    if song.get("mood") == user_prefs.get("favorite_mood"):
        score += mood_weight
        reasons.append(f"mood match (+{mood_weight})")

    default_numeric_weights = {
        "energy": 1.5,
        "valence": 1.0,
        "acousticness": 0.8,
        "danceability": 0.5,
        "tempo_bpm": 0.3,
    }
    if numeric_feature_weights is None:
        numeric_feature_weights = default_numeric_weights

    # (song field, profile key, label)
    numeric_features = [
        ("energy", "target_energy", "energy"),
        ("valence", "target_valence", "valence"),
        ("acousticness", "preferred_acousticness", "acousticness"),
        ("danceability", "preferred_danceability", "danceability"),
        ("tempo_bpm", "preferred_tempo", "tempo"),
    ]

    for song_field, pref_key, label in numeric_features:
        target = user_prefs.get(pref_key)
        value = song.get(song_field)
        if target is None or value is None:
            continue

        weight = numeric_feature_weights.get(song_field, 0.0)
        if weight == 0:
            continue

        if song_field == "tempo_bpm":
            difference = abs(float(value) - float(target)) / (164 - 60)
        else:
            difference = abs(float(value) - float(target))

        similarity = max(0.0, 1.0 - difference)
        contribution = similarity * weight
        score += contribution
        reasons.append(f"{label} close to target (+{contribution:.2f})")

    return score, reasons

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    genre_weight: float = 2.0,
    mood_weight: float = 1.0,
    numeric_feature_weights: Optional[Dict[str, float]] = None,
) -> List[Tuple[Dict, float, str]]:
    """Rank songs by score and return the top k recommendations with explanations."""
    ranked = [
        (song, score, "; ".join(reasons))
        for song in songs
        for score, reasons in [
            score_song(
                user_prefs,
                song,
                genre_weight=genre_weight,
                mood_weight=mood_weight,
                numeric_feature_weights=numeric_feature_weights,
            )
        ]
    ]
    ranked.sort(key=lambda item: item[1], reverse=True)
    return ranked[:k]
