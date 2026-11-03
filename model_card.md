# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

VibeFinder 1.0

---

## 2. Intended Use

This recommender is meant for a small classroom-style music demo. It helps a user get a first list of songs based on a taste profile. The system assumes a user has a favorite genre, a favorite mood, and a rough idea of how energetic or acoustic they want the music to feel. It is not built for a real commercial music app. It is meant to show how simple content-based recommendations work.

---

## 3. How the Model Works

This recommender compares each song to the user's taste profile. It looks at genre, mood, energy, tempo, valence, danceability, and acousticness. It gives a bigger score when a song matches the user's favorite genre and mood. Then it checks how close the song's numbers are to the user's target values. This makes the system easy to understand and easy to adjust.

---

## 4. Data

The catalog has 20 songs. It includes many genres such as pop, lofi, rock, synthwave, indie pop, hip hop, punk, jazz, folk, r&b, electronic, country, classical, and more. The moods include happy, chill, intense, relaxed, moody, focused, romantic, melancholic, nostalgic, and angry. I did not add or remove songs. The dataset is small, so it misses some real-world music tastes like very niche genres, strong cultural trends, and many kinds of emotional states.

---

## 5. Strengths

The system works best when a user's profile is clear and simple. A user who likes pop and happy songs gets good results. A user who likes chill lofi songs also gets very believable recommendations. The scoring is easy to explain. It is also easy to see why a song was picked, because the system gives a reason string like “genre match” or “energy close to target.”

---

## 6. Limitations and Bias

The biggest problem is that genre and mood are too powerful. A song that matches the user's favorite genre often jumps ahead even when it does not fit the rest of the profile. This can create a filter bubble. A user may keep getting songs from the same style instead of a wider mix. The catalog is also small, so the system does not see many types of music.

---

## 7. Evaluation

I tested a few user profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, and Indie Pop Romantic. I compared the top songs for each one and looked at whether the results made sense. The biggest surprise was that “Gym Hero” kept showing up for happy pop users. This happened because the system loves exact genre and mood matches first. A pop song that is also happy gets a big bonus. After that, the model only adds a little more for energy and tempo. So “Gym Hero” can stay near the top even when a different happy pop song might feel more fitting.

I also compared High-Energy Pop with Chill Lofi. The first profile moved toward bright and punchy songs. The second profile moved toward slow, quiet, acoustic tracks. That made sense because the energy target changed a lot. The system responded to energy, but it still favored the same genre and mood buckets.

The biggest mismatch happened with Indie Pop Romantic. The model liked “Stupid Song” because it matched the indie pop genre, even though it felt more melancholic than romantic. When I lowered the genre weight, “Heaven” jumped up. That made more sense to me because it matched the mood better. This showed that the system was relying too much on the genre label.

---

## 8. Future Work

I would make the model less dependent on exact genre matches. I would add more balanced scoring so mood and energy matter more. I would also add diversity controls so the top results do not all come from one style. A better system could explain recommendations in plain words, like “This song fits your mood but is a bit different from your usual genre.” I would also want it to handle more complex tastes, such as “happy but low energy” or “romantic but still energetic.”

---

## 9. Personal Reflection

I learned that recommenders are simple rules under the hood, even when they look smart. I was surprised by how much one exact genre match could control the whole ranking. This changed how I think about music apps. They can seem personal, but they often stay inside a small comfort zone unless the scoring is designed to explore beyond it.

