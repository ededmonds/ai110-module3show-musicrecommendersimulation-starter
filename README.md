# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works
Thought processHow The System Works
The recommender takes a user's taste profile and scores every song in songs.csv against it, then returns the highest-scoring matches. Data flows in three stages: user_prefs (a dict or UserProfile) and the loaded song list both feed into a loop that calls score_song() once per song; each call returns a point total plus a list of reasons; the results are sorted by score and sliced to the top k.
Algorithm Recipe (finalized):
Each song earns points against the user's profile, out of a maximum of 5.5:

Genre match: +2.0 pts if song.genre == favorite_genre
Mood match: +1.0 pt if song.mood == favorite_mood
Energy similarity: up to +2.0 pts, scaled by closeness — 2.0 * max(0, 1 - |song.energy - target_energy|)
Acoustic preference: +0.5 pts if song.acousticness falls on the correct side of 0.5 for likes_acoustic

Any profile field left unset (e.g. a partial profile) is simply skipped rather than penalized, and songs are ranked by total points, descending.
Potential biases:
This system likely over-prioritizes genre — at 2.0 of 5.5 possible points (36%), a song that's a near-perfect mood and energy match but the "wrong" genre can still lose to a same-genre song that fits the user's mood and energy poorly. It also can't recognize adjacent categories: genre and mood matching is exact-string-only, so a user who likes "rock" gets zero credit for a "synthwave" song even if it's sonically close, and "intense" gets no credit for "energetic." The acoustic bonus is a hard cutoff at 0.5 acousticness, so a song at 0.49 and a song at 0.02 are scored identically as "not acoustic," losing real nuance near the boundary. Finally, the recipe ignores valence, danceability, and tempo entirely, so two songs that are identical on genre/mood/energy/acousticness score the same even if one is fast and danceable and the other isn't — the system can't distinguish within that cluster.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
Loading songs from data/songs.csv...
18

============================================================
 TOP 5 RECOMMENDATIONS
============================================================

1. Sunrise City                        Score: 4.96
   - genre match (+2.0 pts): pop
   - mood match (+1.0 pt): happy
   - energy similarity (+1.96 pts): song energy 0.82 vs target 0.80

2. Gym Hero                            Score: 3.74
   - genre match (+2.0 pts): pop
   - energy similarity (+1.74 pts): song energy 0.93 vs target 0.80

3. Rooftop Lights                      Score: 2.92
   - mood match (+1.0 pt): happy
   - energy similarity (+1.92 pts): song energy 0.76 vs target 0.80

4. Basement Bounce                     Score: 2.00
   - energy similarity (+2.00 pts): song energy 0.80 vs target 0.80

5. Night Drive Loop                    Score: 1.90
   - energy similarity (+1.90 pts): song energy 0.75 vs target 0.80

```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

(.venv) ericedmonds@Erics-MacBook-Pro-2 ai110-module3show-musicrecommendersimulation-starter % python -m src.main 
Loading songs from data/songs.csv...
Loaded 18 songs.


======================================================================
 Baseline: High-Energy Pop
 prefs: {'favorite_genre': 'pop', 'favorite_mood': 'happy', 'target_energy': 0.9, 'likes_acoustic': False}
======================================================================

1. Sunrise City                        Score: 5.34
   - genre match (+2.0 pts): pop
   - mood match (+1.0 pt): happy
   - energy similarity (+1.84 pts): song energy 0.82 vs target 0.90
   - acoustic preference match (+0.5 pts)

2. Gym Hero                            Score: 4.44
   - genre match (+2.0 pts): pop
   - energy similarity (+1.94 pts): song energy 0.93 vs target 0.90
   - acoustic preference match (+0.5 pts)

3. Rooftop Lights                      Score: 3.22
   - mood match (+1.0 pt): happy
   - energy similarity (+1.72 pts): song energy 0.76 vs target 0.90
   - acoustic preference match (+0.5 pts)

======================================================================
 Baseline: Chill Lofi
 prefs: {'favorite_genre': 'lofi', 'favorite_mood': 'chill', 'target_energy': 0.3, 'likes_acoustic': True}
======================================================================

1. Library Rain                        Score: 5.40
   - genre match (+2.0 pts): lofi
   - mood match (+1.0 pt): chill
   - energy similarity (+1.90 pts): song energy 0.35 vs target 0.30
   - acoustic preference match (+0.5 pts)

2. Midnight Coding                     Score: 5.26
   - genre match (+2.0 pts): lofi
   - mood match (+1.0 pt): chill
   - energy similarity (+1.76 pts): song energy 0.42 vs target 0.30
   - acoustic preference match (+0.5 pts)

3. Focus Flow                          Score: 4.30
   - genre match (+2.0 pts): lofi
   - energy similarity (+1.80 pts): song energy 0.40 vs target 0.30
   - acoustic preference match (+0.5 pts)

======================================================================
 Baseline: Deep Intense Rock
 prefs: {'favorite_genre': 'rock', 'favorite_mood': 'intense', 'target_energy': 0.9, 'likes_acoustic': False}
======================================================================

1. Storm Runner                        Score: 5.48
   - genre match (+2.0 pts): rock
   - mood match (+1.0 pt): intense
   - energy similarity (+1.98 pts): song energy 0.91 vs target 0.90
   - acoustic preference match (+0.5 pts)

2. Gym Hero                            Score: 3.44
   - mood match (+1.0 pt): intense
   - energy similarity (+1.94 pts): song energy 0.93 vs target 0.90
   - acoustic preference match (+0.5 pts)

3. Warehouse Pulse                     Score: 2.46
   - energy similarity (+1.96 pts): song energy 0.88 vs target 0.90
   - acoustic preference match (+0.5 pts)

======================================================================
 Adversarial: Energetic Sadness (classical/melancholic/energy 0.9/acoustic)
 prefs: {'favorite_genre': 'classical', 'favorite_mood': 'melancholic', 'target_energy': 0.9, 'likes_acoustic': True}
======================================================================

1. Paper Boats                         Score: 4.10
   - genre match (+2.0 pts): classical
   - mood match (+1.0 pt): melancholic
   - energy similarity (+0.60 pts): song energy 0.20 vs target 0.90
   - acoustic preference match (+0.5 pts)

2. Storm Runner                        Score: 1.98
   - energy similarity (+1.98 pts): song energy 0.91 vs target 0.90

3. Warehouse Pulse                     Score: 1.96
   - energy similarity (+1.96 pts): song energy 0.88 vs target 0.90

======================================================================
 Adversarial: Nonexistent genre (opera)
 prefs: {'favorite_genre': 'opera', 'favorite_mood': 'happy', 'target_energy': 0.5, 'likes_acoustic': True}
======================================================================

1. Rooftop Lights                      Score: 2.48
   - mood match (+1.0 pt): happy
   - energy similarity (+1.48 pts): song energy 0.76 vs target 0.50

2. Sundown Highway                     Score: 2.46
   - energy similarity (+1.96 pts): song energy 0.48 vs target 0.50
   - acoustic preference match (+0.5 pts)

3. Sunrise City                        Score: 2.36
   - mood match (+1.0 pt): happy
   - energy similarity (+1.36 pts): song energy 0.82 vs target 0.50

======================================================================
 Adversarial: Out-of-range energy (1.5)
 prefs: {'favorite_genre': 'rock', 'favorite_mood': 'intense', 'target_energy': 1.5, 'likes_acoustic': False}
======================================================================

1. Storm Runner                        Score: 4.32
   - genre match (+2.0 pts): rock
   - mood match (+1.0 pt): intense
   - energy similarity (+0.82 pts): song energy 0.91 vs target 1.50
   - acoustic preference match (+0.5 pts)

2. Gym Hero                            Score: 2.36
   - mood match (+1.0 pt): intense
   - energy similarity (+0.86 pts): song energy 0.93 vs target 1.50
   - acoustic preference match (+0.5 pts)

3. Riot Fuel                           Score: 1.44
   - energy similarity (+0.94 pts): song energy 0.97 vs target 1.50
   - acoustic preference match (+0.5 pts)

======================================================================
 Adversarial: Empty profile
 prefs: {}
======================================================================

1. Sunrise City                        Score: 0.00
   - no matching criteria, included as closest available option

2. Midnight Coding                     Score: 0.00
   - no matching criteria, included as closest available option

3. Storm Runner                        Score: 0.00
   - no matching criteria, included as closest available option

======================================================================
 Adversarial: Metal but likes_acoustic=True
 prefs: {'favorite_genre': 'metal', 'favorite_mood': 'angry', 'target_energy': 0.95, 'likes_acoustic': True}
======================================================================

1. Riot Fuel                           Score: 4.96
   - genre match (+2.0 pts): metal
   - mood match (+1.0 pt): angry
   - energy similarity (+1.96 pts): song energy 0.97 vs target 0.95

2. Gym Hero                            Score: 1.96
   - energy similarity (+1.96 pts): song energy 0.93 vs target 0.95

3. Storm Runner                        Score: 1.92
   - energy similarity (+1.92 pts): song energy 0.91 vs target 0.95

(.venv) ericedmonds@Erics-MacBook-Pro-2 ai110-module3show-musicrecommendersimulation-starter % 


---

## Limitations and Risks

Summarize some limitations of your recommender.

The recommender is limited by a small, static catalog — it can only recommend songs already in songs.csv, so it has no ability to discover new music, and a user whose taste doesn't overlap with the existing genres/moods will get weak matches no matter how well the algorithm runs. It's purely content-based with no collaborative filtering, so it can never produce the "people who liked X also liked Y" recommendations that come from learning across many users — every score depends entirely on hand-coded rules applied to one song at a time. The taste profile is also static: there's no feedback loop, so the system never learns from skips, replays, or thumbs-up/down, and a user's profile has to be manually updated to reflect a change in taste. Genre and mood matching rely on exact string equality, which is brittle — "rock" and "hard rock," or "intense" and "energetic," are treated as completely unrelated even if they'd feel similar to a listener. The point weights themselves (2.0/1.0/2.0/0.5) were chosen by hand rather than derived from user testing or data, so there's a real risk they don't actually reflect what makes a recommendation feel right, and as noted earlier they likely overweight genre relative to mood and energy. Finally, the algorithm has no concept of diversity — nothing stops the top-k results from clustering around a single artist or a narrow slice of the catalog, and features like valence, danceability, and tempo are ignored entirely, so songs that differ meaningfully on those axes can still score identically.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



