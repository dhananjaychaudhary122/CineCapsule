import datetime
from achievements import AchievementSystem, UserProfile

def simulate_watch_history():
    print("="*60)
    print("      CineCapsule – Achievement System Demo")
    print("="*60)

    # 1. Initialize System
    system = AchievementSystem()
    user = UserProfile(user_id="user_123")
    print(f"\n[INFO] Initialized new user profile: {user.user_id}")
    print(f"[INFO] Total available achievements: {len(system.achievements)}")

    # 2. Simulated Watch History Data
    # A mix of movies to trigger various achievements (Action, Drama, Comedy, Horror, Sci-Fi)
    watch_history = [
        # Action Streak
        {'title': 'Mad Max: Fury Road', 'genres': ['Action', 'Sci-Fi'], 'type': 'Movie', 'rating': 8.1, 'sentiment_score': 0.8},
        {'title': 'John Wick', 'genres': ['Action', 'Thriller'], 'type': 'Movie', 'rating': 7.4, 'sentiment_score': 0.85},
        {'title': 'Die Hard', 'genres': ['Action'], 'type': 'Movie', 'rating': 8.2, 'sentiment_score': 0.9}, # Should trigger "Action Rookie", "Adrenaline Junkie" (if 10), "Bullet Time"
        
        # Drama
        {'title': 'The Shawshank Redemption', 'genres': ['Drama'], 'type': 'Movie', 'rating': 9.3, 'sentiment_score': 0.95}, # Drama Debut
        
        # Horror at Night (Simulation relies on current time in the class, so we might not trigger time-based ones accurately in a static loop without mocking time, but let's assume evening run or just show logic)
        {'title': 'The Conjuring', 'genres': ['Horror', 'Thriller'], 'type': 'Movie', 'rating': 7.5, 'sentiment_score': 0.6}, # Edge of Seat (Thriller), maybe Night Watcher if run at night

        # Comedy
        {'title': 'Superbad', 'genres': ['Comedy'], 'type': 'Movie', 'rating': 7.6, 'sentiment_score': 0.8}, # Laugh Track
        
        # Sci-Fi / Fantasy
        {'title': 'Interstellar', 'genres': ['Sci-Fi', 'Drama'], 'type': 'Movie', 'rating': 8.6, 'sentiment_score': 0.9, 'themes': ['Time Travel']}, # Sci-Fi Explorer, Time Traveler
        
        # Series Binge
        {'title': 'Breaking Bad', 'genres': ['Crime', 'Drama'], 'type': 'Series', 'rating': 9.5, 'sentiment_score': 0.9}, # Deep Feels (Drama Series)
        
        # Animation
        {'title': 'Spirited Away', 'genres': ['Animation', 'Fantasy'], 'type': 'Movie', 'rating': 8.6, 'sentiment_score': 0.9}, # Animated Beginnings, Pixar Mode (High Sentiment)
        
        # More Action to hit 5 counts? 
        {'title': 'The Dark Knight', 'genres': ['Action', 'Crime'], 'type': 'Movie', 'rating': 9.0, 'sentiment_score': 0.9},
        {'title': 'Gladiator', 'genres': ['Action', 'Drama'], 'type': 'Movie', 'rating': 8.5, 'sentiment_score': 0.85}, 
    ]

    print("\n[INFO] Starting Watch Simulation...\n")

    # 3. Process Watch Events
    for i, movie in enumerate(watch_history, 1):
        print(f"User is watching: {movie['title']} ({', '.join(movie['genres'])})")
        
        # Log event
        user.add_watch_event(movie)
        
        # Check for new achievements
        unlocked = system.evaluate(user, movie)
        
        if unlocked:
            for ach in unlocked:
                print(f"  >>> ACHIEVEMENT UNLOCKED: {ach.name} <<<")
                print(f"      Desc: {ach.description}")
                print(f"      Category: {ach.category}")
        else:
            print("  (No new achievements unlocked)")
        print("-" * 40)

    # 4. Final Summary
    print("\n" + "="*60)
    print("      FINAL USER STATS")
    print("="*60)
    print(f"Total Titles Watched: {len(user.watched_movies)}")
    print("Genre Breakdown:")
    for genre, count in user.genre_counts.items():
        print(f"  - {genre}: {count}")
    
    print("\nUnlocked Achievements:")
    if user.achievements_unlocked:
        for ach in user.achievements_unlocked:
            print(f"  [x] {ach.name} ({ach.category})")
    else:
        print("  None")
    print("="*60)

if __name__ == "__main__":
    simulate_watch_history()
