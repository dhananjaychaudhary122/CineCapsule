import datetime
from collections import defaultdict, Counter

class Achievement:
    def __init__(self, name, description, category, condition_func):
        self.name = name
        self.description = description
        self.category = category
        self.condition_func = condition_func  # Function showing (user_profile, current_movie) -> bool

class UserProfile:
    def __init__(self, user_id):
        self.user_id = user_id
        self.watched_movies = []  # List of dicts with movie metadata and watch timestamp
        self.genre_counts = Counter()
        self.achievements_unlocked = []  # List of Achievement objects
        self.watch_streaks = 0
        self.last_watch_date = None

    def add_watch_event(self, movie):
        """
        Log a watch event.
        movie: dict containing 'title', 'genre' (list), 'rating', 'sentiment', 'type' (Movie/Series), etc.
        """
        timestamp = datetime.datetime.now()
        movie['watched_at'] = timestamp
        self.watched_movies.append(movie)
        
        # Update genre counts
        for genre in movie.get('genres', []):
            self.genre_counts[genre] += 1
            
        # Basic streak logic (simplified for demo)
        today = timestamp.date()
        if self.last_watch_date:
            delta = (today - self.last_watch_date).days
            if delta == 1:
                self.watch_streaks += 1
            elif delta > 1:
                self.watch_streaks = 1 # Reset if gap > 1 day, start new if watched today
        else:
            self.watch_streaks = 1
            
        self.last_watch_date = today

class AchievementSystem:
    def __init__(self):
        self.achievements = self._define_achievements()

    def _define_achievements(self):
        """Defines the library of all possible achievements."""
        achievements = []
        
        # --- Helpers ---
        def has_genre(movie, genre):
            return genre.lower() in [g.lower() for g in movie.get('genres', [])]
        
        def count_genre(user, genre):
            return user.genre_counts[genre]

        def count_type(user, ctype):
            return sum(1 for m in user.watched_movies if m.get('type') == ctype)

        # --- ACTION GENRE ---
        achievements.append(Achievement("Action Rookie", "Watched 3 action movies", "Action", 
            lambda u, m: count_genre(u, 'Action') == 3))
        achievements.append(Achievement("Explosive Start", "Watched first action movie", "Action", 
            lambda u, m: count_genre(u, 'Action') == 1))
        achievements.append(Achievement("Adrenaline Junkie", "Watched 10 action movies", "Action", 
            lambda u, m: count_genre(u, 'Action') == 10))
        achievements.append(Achievement("One-Man Army", "Watched 5 action series", "Action", 
            lambda u, m: sum(1 for x in u.watched_movies if has_genre(x, 'Action') and x.get('type') == 'Series') == 5))
        achievements.append(Achievement("Bullet Time", "Watched action movies back-to-back", "Action", 
           lambda u, m: len(u.watched_movies) >= 2 and has_genre(u.watched_movies[-1], 'Action') and has_genre(u.watched_movies[-2], 'Action')))

        # --- DRAMA GENRE ---
        achievements.append(Achievement("Drama Debut", "First drama watched", "Drama", 
            lambda u, m: count_genre(u, 'Drama') == 1))
        achievements.append(Achievement("Emotional Rollercoaster", "Watched 5 drama movies", "Drama", 
            lambda u, m: count_genre(u, 'Drama') == 5))
        achievements.append(Achievement("Tearjerker", "Watched 10 drama titles", "Drama", 
            lambda u, m: count_genre(u, 'Drama') == 10))
        achievements.append(Achievement("Story Lover", "Drama movies over multiple years", "Drama", 
            lambda u, m: len(set(x.get('year') for x in u.watched_movies if has_genre(x, 'Drama'))) >= 3))
        achievements.append(Achievement("Deep Feels", "Long-form drama series completed", "Drama", 
             lambda u, m: has_genre(m, 'Drama') and m.get('type') == 'Series')) # Simplified trigger on any Drama Series

        # --- COMEDY GENRE ---
        achievements.append(Achievement("Laugh Track", "First comedy watched", "Comedy", 
            lambda u, m: count_genre(u, 'Comedy') == 1))
        achievements.append(Achievement("Giggle Fest", "Watched 5 comedies", "Comedy", 
            lambda u, m: count_genre(u, 'Comedy') == 5))
        achievements.append(Achievement("Comic Relief", "Watched 10 comedies", "Comedy", 
            lambda u, m: count_genre(u, 'Comedy') == 10))
        achievements.append(Achievement("Sitcom Star", "Completed a comedy series", "Comedy", 
             lambda u, m: has_genre(m, 'Comedy') and m.get('type') == 'Series'))
        achievements.append(Achievement("Mood Lifter", "Comedy watched after negative sentiment content", "Comedy", 
            lambda u, m: len(u.watched_movies) >= 2 and has_genre(m, 'Comedy') and u.watched_movies[-2].get('sentiment_score', 0) < 0))

        # --- THRILLER / HORROR ---
        achievements.append(Achievement("Edge of Seat", "First thriller watched", "Thriller", 
            lambda u, m: count_genre(u, 'Thriller') == 1))
        achievements.append(Achievement("Night Watcher", "Watched horror at night (after 8 PM)", "Horror", 
            lambda u, m: has_genre(m, 'Horror') and m['watched_at'].hour >= 20))
        achievements.append(Achievement("Fearless", "Watched 5 horror movies", "Horror", 
            lambda u, m: count_genre(u, 'Horror') == 5))
        achievements.append(Achievement("Mind Bender", "Psychological thrillers watched", "Thriller", 
             lambda u, m: has_genre(m, 'Thriller') and 'Psychological' in m.get('themes', [])))
        achievements.append(Achievement("No Jump Scares", "Horror marathon (3 in a row)", "Horror", 
             lambda u, m: len(u.watched_movies) >= 3 and all(has_genre(x, 'Horror') for x in u.watched_movies[-3:])))

        # --- SCI-FI / FANTASY ---
        achievements.append(Achievement("Sci-Fi Explorer", "First sci-fi movie watched", "Sci-Fi", 
             lambda u, m: count_genre(u, 'Sci-Fi') == 1))
        achievements.append(Achievement("Time Traveler", "Time-travel content watched", "Sci-Fi", 
             lambda u, m: 'Time Travel' in m.get('themes', [])))
        achievements.append(Achievement("Galaxy Hopper", "Watched 5 sci-fi movies", "Sci-Fi", 
             lambda u, m: count_genre(u, 'Sci-Fi') == 5))
        achievements.append(Achievement("Fantasy Realm", "Watched fantasy series", "Fantasy", 
             lambda u, m: has_genre(m, 'Fantasy') and m.get('type') == 'Series'))
        achievements.append(Achievement("World Builder", "Sci-fi series completed", "Sci-Fi", 
             lambda u, m: has_genre(m, 'Sci-Fi') and m.get('type') == 'Series'))

        # --- ROMANCE ---
        achievements.append(Achievement("Hopeless Romantic", "First romance movie", "Romance", 
             lambda u, m: count_genre(u, 'Romance') == 1))
        achievements.append(Achievement("Love Story", "Watched 5 romance titles", "Romance", 
             lambda u, m: count_genre(u, 'Romance') == 5))
        achievements.append(Achievement("Heartstrings", "Romance marathon (3 in a row)", "Romance", 
             lambda u, m: len(u.watched_movies) >= 3 and all(has_genre(x, 'Romance') for x in u.watched_movies[-3:])))
        achievements.append(Achievement("Date Night", "Romance watched on weekend", "Romance", 
             lambda u, m: has_genre(m, 'Romance') and m['watched_at'].weekday() >= 5))
        achievements.append(Achievement("Love Across Time", "Historical romance watched", "Romance", 
             lambda u, m: has_genre(m, 'Romance') and 'Historical' in m.get('themes', [])))

        # --- ANIMATION ---
        achievements.append(Achievement("Animated Beginnings", "First animated movie", "Animation", 
             lambda u, m: count_genre(u, 'Animation') == 1))
        achievements.append(Achievement("Toon Fan", "Watched 5 animated titles", "Animation", 
             lambda u, m: count_genre(u, 'Animation') == 5))
        achievements.append(Achievement("Pixar Mode", "Animated emotional content watched", "Animation", 
             lambda u, m: has_genre(m, 'Animation') and m.get('sentiment_score', 0) > 0.8)) # High sentiment animation
        achievements.append(Achievement("Family Time", "Animation watched", "Animation", 
             lambda u, m: has_genre(m, 'Animation'))) # Simplified
        achievements.append(Achievement("Forever Young", "Animation across age categories (implied by count > 2)", "Animation", 
             lambda u, m: count_genre(u, 'Animation') > 2))

        # --- DIVERSITY & EXPLORATION ---
        achievements.append(Achievement("Genre Explorer", "Watched 5 different genres", "Diversity", 
             lambda u, m: len(u.genre_counts) >= 5))
        achievements.append(Achievement("Polyglot Viewer", "Watched content in multiple languages", "Diversity", 
             lambda u, m: len(set(x.get('language', 'English') for x in u.watched_movies)) > 1))
        achievements.append(Achievement("Weekend Warrior", "Movies watched on weekend", "Diversity", 
             lambda u, m: m['watched_at'].weekday() >= 5))
        achievements.append(Achievement("Night Owl", "Late-night viewing (after 11 PM)", "Diversity", 
             lambda u, m: m['watched_at'].hour >= 23))
        achievements.append(Achievement("Cinephile", "Watched 50 total titles", "Diversity", 
             lambda u, m: len(u.watched_movies) == 50))

        # --- BONUS / PRESTIGE ---
        achievements.append(Achievement("Sentiment Seeker", "Prefers high-sentiment movies (Avg > 0.7)", "Prestige", 
             lambda u, m: len(u.watched_movies) > 5 and sum(x.get('sentiment_score', 0) for x in u.watched_movies)/len(u.watched_movies) > 0.7))
        achievements.append(Achievement("Critic Mode", "Watches low-rated but high-sentiment movies", "Prestige", 
             lambda u, m: m.get('rating', 0) < 5 and m.get('sentiment_score', 0) > 0.5))
        achievements.append(Achievement("Binge Master", "Completed multiple series", "Prestige", 
             lambda u, m: count_type(u, 'Series') >= 2))
        achievements.append(Achievement("Balanced Taste", "Watched at least 1 of top 5 genres", "Prestige", 
             lambda u, m: all(u.genre_counts[g] >= 1 for g in ['Action', 'Drama', 'Comedy', 'Sci-Fi', 'Romance'])))
        achievements.append(Achievement("CineCapsule Legend", "Unlocks 30 achievements", "Prestige", 
             lambda u, m: len(u.achievements_unlocked) >= 30))

        return achievements

    def evaluate(self, user, movie):
        """
        Evaluate achievements after a user watches a movie.
        Returns a list of newly unlocked achievements.
        """
        unlocked_now = []
        for ach in self.achievements:
            # Check if condition met AND not already unlocked
            if ach not in user.achievements_unlocked:
                try:
                    if ach.condition_func(user, movie):
                        user.achievements_unlocked.append(ach)
                        unlocked_now.append(ach)
                except Exception as e:
                    # Fail silently for safety
                    pass
        return unlocked_now
