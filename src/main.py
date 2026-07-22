"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs

EVAL_PROFILES below covers the "System Evaluation" step: three baseline
taste profiles plus five adversarial / edge-case profiles designed to try
to trick or break the scoring logic (contradictory preferences, a genre
that doesn't exist in the catalog, an out-of-range energy value, a
completely empty profile, and a profile whose genre/mood conflict with its
own acoustic preference).
"""

from .recommender import load_songs, recommend_songs

EVAL_PROFILES = {
    "Baseline: High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
    "Baseline: Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.3,
        "likes_acoustic": True,
    },
    "Baseline: Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
    "Adversarial: Energetic Sadness (classical/melancholic/energy 0.9/acoustic)": {
        "favorite_genre": "classical",
        "favorite_mood": "melancholic",
        "target_energy": 0.9,
        "likes_acoustic": True,
    },
    "Adversarial: Nonexistent genre (opera)": {
        "favorite_genre": "opera",
        "favorite_mood": "happy",
        "target_energy": 0.5,
        "likes_acoustic": True,
    },
    "Adversarial: Out-of-range energy (1.5)": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 1.5,
        "likes_acoustic": False,
    },
    "Adversarial: Empty profile": {},
    "Adversarial: Metal but likes_acoustic=True": {
        "favorite_genre": "metal",
        "favorite_mood": "angry",
        "target_energy": 0.95,
        "likes_acoustic": True,
    },
}


def print_recommendations(profile_name: str, user_prefs: dict, songs: list, k: int = 3) -> None:
    """Print a formatted top-k recommendation block for one user profile."""
    print("\n" + "=" * 70)
    print(f" {profile_name}")
    print(f" prefs: {user_prefs}")
    print("=" * 70)

    recommendations = recommend_songs(user_prefs, songs, k=k)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']:<35} Score: {score:.2f}")
        for reason in explanation.split("; "):
            print(f"   - {reason}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs.\n")

    for profile_name, user_prefs in EVAL_PROFILES.items():
        print_recommendations(profile_name, user_prefs, songs, k=3)

    print()


if __name__ == "__main__":
    main()
