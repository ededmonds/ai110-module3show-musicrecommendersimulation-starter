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

Building this made it clear that "recommendation" is really just structured scoring plus sorting once you strip away the buzzwords — the hard part was never the code itself, it was deciding what should count and how much. What surprised me most was how much a single weight change could flip the entire ranking; moving genre from a small bonus to the dominant factor completely changed which songs felt "right" for the same listener. That made me think differently about apps like Spotify — their recommendations aren't neutral outputs of some objective algorithm, they're the result of someone's editorial choices about what should matter most, just expressed as numbers instead of opinions.