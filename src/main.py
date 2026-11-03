"""
Command line runner for the Music Recommender Simulation.
"""

from src.recommender import load_songs, recommend_songs

PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.90,
        "target_valence": 0.80,
        "likes_acoustic": False,
        "preferred_acousticness": 0.10,
        "preferred_danceability": 0.85,
        "preferred_tempo": 125,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "target_valence": 0.60,
        "likes_acoustic": True,
        "preferred_acousticness": 0.80,
        "preferred_danceability": 0.60,
        "preferred_tempo": 75,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.92,
        "target_valence": 0.45,
        "likes_acoustic": False,
        "preferred_acousticness": 0.10,
        "preferred_danceability": 0.65,
        "preferred_tempo": 150,
    },
    "Indie Pop Romantic": {
        "favorite_genre": "indie pop",
        "favorite_mood": "romantic",
        "target_energy": 0.60,
        "target_valence": 0.70,
        "likes_acoustic": True,
        "preferred_acousticness": 0.60,
        "preferred_danceability": 0.60,
        "preferred_tempo": 100,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in PROFILES.items():
        print(f"\n=== {name} ===")
        recommendations = recommend_songs(user_prefs, songs, k=5)

        for idx, rec in enumerate(recommendations, start=1):
            song, score, explanation = rec
            print(f"{idx}. {song['title']} by {song['artist']}")
            print(f"   Score: {score:.2f}")
            print("   Why:")
            for reason in explanation.split("; "):
                print(f"      - {reason}")
            print()


if __name__ == "__main__":
    main()
