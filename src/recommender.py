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
# Algorithm Recipe (point-based)
# ---------------------------------------------------------------------------
# Each song earns points against a user's taste profile. Max possible score
# is 5.5 when every preference is supplied and fully matched:
#
#   genre match    : +2.0 pts  if song.genre == favorite_genre
#   mood match      : +1.0 pt   if song.mood == favorite_mood
#   energy similarity: up to +2.0 pts, scaled by closeness -
#                      2.0 * max(0, 1 - |song.energy - target_energy|)
#   acoustic match  : +0.5 pts  if song.acousticness is on the correct side
#                      of 0.5 for the user's likes_acoustic preference
#
# Any preference key missing from user_prefs (e.g. a starter profile that
# only sets favorite_genre/favorite_mood/target_energy) is simply skipped -
# no points are awarded or lost for it, and no KeyError is raised.
# ---------------------------------------------------------------------------

POINTS = {
    "genre": 2.0,
    "mood": 1.0,
    "energy_max": 2.0,
    "acoustic": 0.5,
}


def _compute_score(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Shared point-based scoring logic used by both the functional and OOP APIs."""
    reasons: List[str] = []
    score = 0.0

    # Genre match: flat bonus for an exact match.
    if user_prefs.get("favorite_genre"):
        if song["genre"] == user_prefs["favorite_genre"]:
            score += POINTS["genre"]
            reasons.append(f"genre match (+{POINTS['genre']:.1f} pts): {song['genre']}")

    # Mood match: flat bonus for an exact match.
    if user_prefs.get("favorite_mood"):
        if song["mood"] == user_prefs["favorite_mood"]:
            score += POINTS["mood"]
            reasons.append(f"mood match (+{POINTS['mood']:.1f} pt): {song['mood']}")

    # Energy similarity: linearly scaled points based on closeness to target.
    if user_prefs.get("target_energy") is not None:
        energy_diff = abs(song["energy"] - user_prefs["target_energy"])
        energy_points = POINTS["energy_max"] * max(0.0, 1 - energy_diff)
        score += energy_points
        if energy_points > 0:
            reasons.append(
                f"energy similarity (+{energy_points:.2f} pts): "
                f"song energy {song['energy']:.2f} vs target {user_prefs['target_energy']:.2f}"
            )

    # Acoustic preference: flat bonus if the song is on the right side of 0.5.
    if user_prefs.get("likes_acoustic") is not None:
        is_acoustic = song["acousticness"] >= 0.5
        if is_acoustic == user_prefs["likes_acoustic"]:
            score += POINTS["acoustic"]
            reasons.append(f"acoustic preference match (+{POINTS['acoustic']:.1f} pts)")

    if not reasons:
        reasons.append("no matching criteria, included as closest available option")

    return round(score, 2), reasons


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
