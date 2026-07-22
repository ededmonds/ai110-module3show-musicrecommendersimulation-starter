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
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



