"""Small experiment harness for tuning the recommender."""

from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

from src.recommender import load_songs, recommend_songs


PROFILES: Dict[str, Dict[str, float | str | bool]] = {
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


def print_recommendations(label: str, recommendations: Iterable[Tuple[dict, float, str]]) -> None:
    print(f"\n=== {label} ===")
    for idx, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{idx}. {song['title']} by {song['artist']} | score={score:.2f}")
        for reason in explanation.split("; "):
            print(f"   - {reason}")
        print()


def experiment_genre_weight(songs: List[dict], profile_name: str, profile: Dict[str, object]) -> None:
    print(f"\n--- Genre weight experiment for {profile_name} ---")
    for weight in (2.0, 1.0, 0.5, 0.25, 0.0):
        recs = recommend_songs(profile, songs, k=3, genre_weight=weight)
        print(f"genre_weight={weight}")
        for idx, (song, score, explanation) in enumerate(recs, start=1):
            print(f"  {idx}. {song['title']} ({score:.2f})")
            if idx == 1:
                print(f"     Why: {explanation}")


def experiment_feature_weights(songs: List[dict], profile_name: str, profile: Dict[str, object]) -> None:
    print(f"\n--- Adding tempo/valence impact for {profile_name} ---")
    baseline = recommend_songs(profile, songs, k=3)
    print("Baseline:")
    for idx, (song, score, explanation) in enumerate(baseline, start=1):
        print(f"  {idx}. {song['title']} ({score:.2f})")

    boosted = recommend_songs(
        profile,
        songs,
        k=3,
        numeric_feature_weights={
            "energy": 1.5,
            "valence": 2.0,
            "acousticness": 0.8,
            "danceability": 0.5,
            "tempo_bpm": 1.0,
        },
    )
    print("With valence + tempo emphasized:")
    for idx, (song, score, explanation) in enumerate(boosted, start=1):
        print(f"  {idx}. {song['title']} ({score:.2f})")
        print(f"     Why: {explanation}")


def experiment_weight_shift(songs: List[dict], profile_name: str, profile: Dict[str, object]) -> None:
    print(f"\n--- Weight shift experiment for {profile_name} ---")
    baseline = recommend_songs(profile, songs, k=5)
    print("Baseline:")
    for idx, (song, score, explanation) in enumerate(baseline, start=1):
        print(f"  {idx}. {song['title']} ({score:.2f})")

    shifted = recommend_songs(
        profile,
        songs,
        k=5,
        genre_weight=1.0,
        mood_weight=1.0,
        numeric_feature_weights={
            "energy": 3.0,
            "valence": 1.0,
            "acousticness": 0.8,
            "danceability": 0.5,
            "tempo_bpm": 0.3,
        },
    )
    print("After weight shift (genre halved, energy doubled):")
    for idx, (song, score, explanation) in enumerate(shifted, start=1):
        print(f"  {idx}. {song['title']} ({score:.2f})")
        print(f"     Why: {explanation}")


def run_all_experiments() -> None:
    songs = load_songs("data/songs.csv")

    print("Music recommender experiment harness")
    print("==================================")

    for profile_name, profile in PROFILES.items():
        recommendations = recommend_songs(profile, songs, k=5)
        print_recommendations(profile_name, recommendations)
        experiment_genre_weight(songs, profile_name, profile)
        experiment_feature_weights(songs, profile_name, profile)
        experiment_weight_shift(songs, profile_name, profile)


if __name__ == "__main__":
    run_all_experiments()
