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

Real-world recommenders like Spotify or Netflix typically blend two approaches: content-based filtering, which compares an item's own attributes (genre, tempo, audio features) against what a user has liked before, and collaborative filtering, which looks at patterns across many users ("people who liked X also liked Y"). They also weigh implicit signals heavily — skip rate, replay count, time of day — not just what a user says they like. My version is a simplified content-based system: it has no listening history or other users to learn from, so it relies entirely on a user's stated preferences (favorite genre, favorite mood, target energy, acoustic preference) compared directly against each song's own attributes. It prioritizes energy match and genre match most heavily, since those proved the strongest signals for distinguishing one song's vibe from another in my data, treats mood as a secondary confirming signal, and uses acoustic preference as a lighter-weight factor.

Features used by Song and UserProfile:
Song — id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness (of these, the scoring algorithm actively uses genre, mood, energy, and acousticness).
UserProfile — favorite_genre, favorite_mood, target_energy, likes_acoustic.

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



