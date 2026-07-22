# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

---

## 2. Intended Use

VibeMatch is a content-based song recommender built as a classroom simulation for an intro AI course, not a production system. It takes a single, explicitly stated taste profile (favorite genre, favorite mood, a target energy level, and whether the listener likes acoustic songs) and returns a ranked, explained list of the best-matching songs from a small local catalog.

It assumes the user can articulate their preferences up front — there's no listening history, no implicit behavior tracking, and no notion of a user changing their mind over time. It's meant for exploring how a recommender's logic can be designed and reasoned about, not for serving real listeners at scale.

---

## 3. How the Model Works

Think of it like a judge scoring contestants against a checklist. Every song in the catalog gets compared to what the listener said they want, and each thing that matches earns points: matching their favorite genre earns the most points, matching their favorite mood earns fewer, and how close the song's energy level is to what they asked for earns a sliding amount — a near-perfect energy match earns almost as much as a genre match, while a wildly different energy level earns nothing. A smaller bonus is added if the song's acoustic-ness lines up with whether the listener said they like acoustic music. Every song gets added up this way, and the songs with the highest totals rise to the top.

The starter file I began with was empty — just placeholder functions that returned nothing. I built the actual scoring pipeline from scratch: loading the CSV, deciding what should count and by how much, judging every song, and sorting the results. The point values themselves went through a few rounds of revision before landing on genre worth the most, energy a close second, mood a supporting signal, and acoustic preference as a light tie-breaker. I also went back and reworked the ranking step to be more efficient — instead of sorting the entire catalog every time, it now only keeps track of the top results as it goes.

---

## 4. Data

The catalog has 18 songs. It started as a 10-song starter file covering 7 genres (pop, lofi, rock, ambient, jazz, synthwave, indie pop) and 6 moods (happy, chill, intense, relaxed, moody, focused). I added 8 more songs specifically to fill gaps — genres like metal, classical, hip-hop, house, country, folk, R&B, and reggae, and moods like nostalgic, angry, melancholic, euphoric, confident, playful, and sensual — so the catalog now spans 15 genres and 13 moods in total.

Even expanded, it's a tiny, hand-built dataset. It has no lyrics or vocal content, no cultural or language dimension, no artist popularity or recency signal, and only one or two songs per genre — so any genre is one song away from being either overrepresented or missing entirely from a given recommendation.

---

## 5. Strengths

The system works best for a listener with a clear, narrow preference — someone who wants "pop, happy, high energy" reliably gets pop/happy songs with close-matching energy at the top, and someone who wants "rock, intense, high energy, not acoustic" reliably surfaces the one song built for exactly that. The energy-similarity scoring is the part I'm most confident in: it rewards "close" rather than treating energy as a pass/fail check, so songs get ranked instead of just filtered. The explanations attached to every score also worked out well — being able to see exactly why a song ranked where it did made it easy to sanity-check the system by hand, and in every test I ran the top result matched my own intuition about what "should" come out on top.

---

## 6. Limitations and Bias

The scoring only looks at four features — genre, mood, energy, and acousticness — and ignores valence, danceability, and tempo entirely, so two songs that differ a lot on those axes can score identically. Genre and mood matching are exact string comparisons, which is brittle: "rock" gets zero credit for a "synthwave" song even if they'd feel similar to a listener, and there's no concept of genres being "close" to each other. The point weights (2.0 for genre, 1.0 for mood, up to 2.0 for energy, 0.5 for acoustic) were something I chose by hand and adjusted through trial and error, not something learned from real user feedback or data — so there's a real chance they overweight genre and underweight mood relative to what would actually feel right to a listener. The system also has no idea of diversity, so nothing stops the top results from clustering around one artist. And because the catalog is so small, some genres are represented by a single song, meaning that song either wins by default or loses by default for any listener interested in that genre — there's no room for it to be "one good option among several."

---

## 7. Evaluation

I didn't have labeled "correct" recommendations to measure against, so evaluation was mostly manual sanity-checking rather than numeric. I ran the recommender against a handful of profiles — a full profile (rock, intense, energy 0.85, dislikes acoustic), the plain starter profile (pop, happy, energy 0.8, no acoustic preference set), and a deliberately incomplete profile missing a field — to confirm the top result matched what I'd expect a person with that taste to want, and that missing profile fields didn't crash the system or silently skew results. I also cross-checked that the functional API and the object-oriented `Recommender` class always produced identical rankings, since they share the same scoring logic underneath.

What surprised me was how little the acoustic bonus (0.5 points) actually moved the final ranking compared to genre and energy — it almost never changed which song came out on top, which made it obvious just how much the genre and energy weights are doing the real work of the ranking.

---

## 8. Future Work

The most useful next step would be folding valence, danceability, and tempo into the score instead of ignoring them. I'd also want to replace exact-match genre/mood scoring with something that allows partial credit for related categories, rather than an all-or-nothing match. Adding a diversity rule — capping how many songs from one artist can appear in the top results — would make the output feel less repetitive. Letting a user specify more than one favorite genre or mood, instead of exactly one of each, would also make the profile better reflect how people actually describe their taste. Longer term, I'd want an actual evaluation set — labeled "good" and "bad" matches — so I could measure the system numerically instead of relying on my own judgment of whether a result "feels right."

---

## 9. Personal Reflection

**Biggest learning moment.** It wasn't the scoring math — it was debugging the plumbing around it. My first real run failed with `ModuleNotFoundError: No module named 'recommender'`, which turned out to be an absolute import in a file meant to be run as a package (`python -m src.main`); fixing it meant switching to a relative import and understanding *why* Python treats `cd src && python main.py` and `python -m src.main` differently. Right after that, I hit a chain of `KeyError`s — `target_energy`, then `favorite_mood`, then `likes_acoustic` — because the `user_prefs` dict my scoring function expected didn't match what the starter's example profile actually contained. That was the real lesson: the bug wasn't in my algorithm, it was in the contract between two pieces of code that I'd assumed matched without checking. Now I default to making functions tolerate missing keys gracefully instead of assuming every caller will hand me a complete dictionary.

**How AI tools helped, and where I had to double-check them.** Having an AI assistant to talk through the design with let me move fast — I could describe an idea in plain language ("genre matches should count for more than mood") and see it turned into working, testable code in the same breath, which made it much easier to iterate on the point weights instead of getting stuck on syntax. But I couldn't just trust the first version blindly. Early on, the assistant built a whole scoring approach based on comparing one song to another (song-to-song similarity) before I'd shown it the actual starter file, which turned out to be structured around comparing songs to a *user profile* instead — a completely different design. I only caught that by actually reading the code it produced against what my assignment scaffold required, not by assuming it had guessed right. I also made a point of re-running the recommender myself after every change and checking the printed scores against my own intuition, rather than trusting that "it runs without errors" meant "it works correctly."

**What surprised me about simple algorithms feeling like recommendations.** The whole scoring system is just addition — a few `if` checks and one absolute-value formula for energy — and yet watching it consistently rank the "obviously right" song first for a given taste profile felt uncannily like it understood something. That illusion cracked in a useful way during the sensitivity experiment: when I doubled energy's weight and halved genre's, one adversarial profile flipped its top recommendation entirely. That made it obvious that the "personality" of the recommender isn't emergent intelligence, it's just the weights I chose, expressed back at me as a ranked list. Simple arithmetic can feel like judgment purely because sorting numbers hides how arbitrary the numbers were in the first place.

**What I'd try next.** I'd want to fold in the features I ignored — valence, danceability, tempo — so two songs that are identical on genre/mood/energy stop scoring as identical twins. I'd also replace the exact-string genre and mood matching with something that allows partial credit for related categories, since right now "rock" and "synthwave" are treated as completely unrelated even when they'd feel close to a listener. Longer term, I'd want to move away from hand-picked weights entirely and toward weights learned from actual feedback (skips, replays, ratings), plus a small labeled evaluation set so I could measure whether a change actually improved recommendations instead of just changing them, which is exactly the ambiguity I ran into during the weight-shift experiment.
