"""
Content-based music recommender.

How The System Works
---------------------
Data flows through three stages:

  1. INPUT   - a user's taste profile (a dict, or a UserProfile instance)
               describing favorite_genre, favorite_mood, target_energy,
               and likes_acoustic.
  2. PROCESS - The Loop: every song loaded from songs.csv is judged
               individually against that profile via score_song() /
               _compute_score(), which returns a point total plus a list
               of human-readable reasons for the score.
  3. OUTPUT  - The Ranking: all scored songs are sorted descending and
               sliced to the top K, returned as (song, score, explanation)
               tuples (functional API) or a list of Song objects
               (Recommender.recommend, OOP API). Both APIs share the same
               scoring logic, so they always agree.

Algorithm Recipe (finalized, point-based)
------------------------------------------
Each song earns points against the user's profile, out of a maximum of 5.5:

  genre match       : +2.0 pts  if song.genre == favorite_genre
  mood match        : +1.0 pt   if song.mood == favorite_mood
  energy similarity : up to +2.0 pts, scaled by closeness -
                       2.0 * max(0, 1 - |song.energy - target_energy|)
  acoustic match    : +0.5 pts  if song.acousticness is on the correct
                       side of 0.5 for the user's likes_acoustic preference

Any preference key missing from user_prefs (e.g. a starter profile that
only sets favorite_genre/favorite_mood/target_energy) is simply skipped -
no points are awarded or lost for it, and no KeyError is raised. Songs are
ranked by total points, descending.

Potential Biases
-----------------
- Over-prioritizes genre: at 2.0 of 5.5 possible points (36%), a song that
  is a near-perfect mood/energy match but the "wrong" genre can still lose
  to a same-genre song that fits the user's mood and energy poorly.
- Exact-match only: genre and mood matching is a literal string comparison,
  so "rock" gets zero credit for a sonically similar "synthwave" song, and
  "intense" gets no credit for "energetic."
- Hard acoustic cutoff: the +0.5 bonus is a step function at 0.5
  acousticness, so a song at 0.49 and a song at 0.02 are scored identically
  as "not acoustic," losing nuance near the boundary.
- Ignores valence, danceability, and tempo entirely, so two songs that
  match on genre/mood/energy/acousticness score identically even if one is
  fast and danceable and the other isn't.
"""

import csv
import heapq
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


# See the module docstring above ("Algorithm Recipe") for the full
# point-weighting rationale.
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

    Every song is judged by score_song() via a generator expression (lazy,
    no intermediate list), then heapq.nlargest() picks the top k by score
    in O(n log k) instead of sorting the full catalog in O(n log n).
    """
    scored = (
        (song, *score_song(user_prefs, song))
        for song in songs
    )
    top = heapq.nlargest(k, scored, key=lambda item: item[1])
    return [(song, score, "; ".join(reasons)) for song, score, reasons in top]
