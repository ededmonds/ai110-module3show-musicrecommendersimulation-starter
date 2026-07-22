import csv
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple


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


# ---------------------------------------------------------------------------
# Algorithm Recipe
# ---------------------------------------------------------------------------
# A song's score is a weighted sum of four components, each on a 0-1 scale,
# so the weights below sum to 1.0 and the final score lands on 0-1:
#
#   energy match   (weight 0.30): 1 - |song.energy - target_energy|
#   genre match    (weight 0.25): 1 if song.genre == favorite_genre else 0
#   mood match     (weight 0.20): 1 if song.mood == favorite_mood else 0
#   acoustic match (weight 0.25): song.acousticness if likes_acoustic
#                                  else (1 - song.acousticness)
#
# Each component also contributes a human-readable reason string, so we can
# explain *why* a song scored the way it did.
# ---------------------------------------------------------------------------

WEIGHTS = {
    "energy": 0.30,
    "genre": 0.25,
    "mood": 0.20,
    "acoustic": 0.25,
}


def _compute_score(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Shared scoring logic used by both the functional and OOP APIs.

    Any preference key that's missing from user_prefs (e.g. a starter
    profile that only sets favorite_genre/favorite_mood/target_energy) is
    simply skipped rather than raising a KeyError - its weight is left out
    of the total and the remaining components are re-normalized so the
    score still lands on a 0-1 scale.
    """
    reasons: List[str] = []
    weighted_total = 0.0
    weight_used = 0.0

    # Energy match: closer to the user's target energy scores higher.
    if user_prefs.get("target_energy") is not None:
        energy_diff = abs(song["energy"] - user_prefs["target_energy"])
        energy_component = 1 - energy_diff
        weighted_total += WEIGHTS["energy"] * energy_component
        weight_used += WEIGHTS["energy"]
        if energy_diff <= 0.1:
            reasons.append(
                f"energy ({song['energy']:.2f}) is close to your target "
                f"({user_prefs['target_energy']:.2f})"
            )

    # Genre match: exact bonus if it matches the favorite genre.
    if user_prefs.get("favorite_genre"):
        genre_match = song["genre"] == user_prefs["favorite_genre"]
        weighted_total += WEIGHTS["genre"] * (1.0 if genre_match else 0.0)
        weight_used += WEIGHTS["genre"]
        if genre_match:
            reasons.append(f"matches your favorite genre ({user_prefs['favorite_genre']})")

    # Mood match: exact bonus if it matches the favorite mood.
    if user_prefs.get("favorite_mood"):
        mood_match = song["mood"] == user_prefs["favorite_mood"]
        weighted_total += WEIGHTS["mood"] * (1.0 if mood_match else 0.0)
        weight_used += WEIGHTS["mood"]
        if mood_match:
            reasons.append(f"matches your favorite mood ({user_prefs['favorite_mood']})")

    # Acoustic preference: reward high acousticness if the user likes it,
    # otherwise reward low acousticness. Only applied if the preference
    # was actually provided.
    if user_prefs.get("likes_acoustic") is not None:
        if user_prefs["likes_acoustic"]:
            acoustic_component = song["acousticness"]
            if song["acousticness"] >= 0.6:
                reasons.append("high acousticness matches your acoustic preference")
        else:
            acoustic_component = 1 - song["acousticness"]
            if song["acousticness"] <= 0.3:
                reasons.append("low acousticness matches your preference for non-acoustic songs")
        weighted_total += WEIGHTS["acoustic"] * acoustic_component
        weight_used += WEIGHTS["acoustic"]

    score = weighted_total / weight_used if weight_used else 0.0

    if not reasons:
        reasons.append("no strong matches, but closest overall fit available")

    return round(score, 4), reasons


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        user_dict = asdict(user)
        scored = [
            (song, _compute_score(user_dict, asdict(song))[0])
            for song in self.songs
        ]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = _compute_score(asdict(user), asdict(song))
        return f"Score {score}: " + "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    numeric_fields = ["energy", "tempo_bpm", "valence", "danceability", "acousticness"]

    with open(csv_path, newline="") as f:
        rows = list(csv.DictReader(f))

    songs = []
    for row in rows:
        for field in numeric_fields:
            row[field] = float(row[field])
        row["id"] = int(row["id"])
        songs.append(row)

    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    return _compute_score(user_prefs, song)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    results = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        results.append((song, score, explanation))

    results.sort(key=lambda item: item[1], reverse=True)
    return results[:k]
