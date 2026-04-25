import pandas as pd
import numpy as np
import joblib
import os
from sklearn.metrics.pairwise import cosine_similarity
from preprocessing import TextPreprocessor
from data_loader import load_data, generate_dummy_data

class Recommender:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, 'models', 'logistic_regression.pkl')
        
        if not os.path.exists(model_path):
            raise FileNotFoundError("Model not found. Please run train_model.py first.")
            
        self.pipeline = joblib.load(model_path)
        self.model = self.pipeline.named_steps['clf']
        self.tfidf = self.pipeline.named_steps['tfidf']
        self.tp = TextPreprocessor()
        
    def get_movie_features(self, df):
        """
        Computes feature vectors for each movie.
        Features: [Avg Sentiment, Pos/Neg Ratio, TF-IDF Centroid components...]
        """
        # 1. TF-IDF Centroids
        # Transform all reviews to TF-IDF vectors
        tfidf_matrix = self.tfidf.transform(df['cleaned_review'].tolist())
        
        # We need to aggregate these by movie.
        # Since tfidf_matrix is sparse, we can't just use groupby directly easily on the matrix.
        # We'll iterate or use a weighted average approach.
        
        movie_titles = df['movie_title'].unique()
        movie_features = {}
        
        print("Computing feature vectors for similarity...")
        
        for title in movie_titles:
            movie_mask = df['movie_title'] == title
            movie_reviews_tfidf = tfidf_matrix[movie_mask.values]
            
            # Centroid: Mean of TF-IDF vectors
            centroid = np.mean(movie_reviews_tfidf, axis=0) # Result is np.matrix
            centroid = np.asarray(centroid).flatten()
            
            # Scalar features
            subset = df[movie_mask]
            avg_sentiment = subset['sentiment_score'].mean()
            # Pos/Neg Ratio: (Count of Positive) / (Total Count)
            # Assuming 'sentiment' column is text 'positive'/'negative' or we use the score.
            # Let's use the score > 0.5 as positive approximation or use original labels if reliable.
            # Using sentiment_score > 0.5:
            pos_ratio = (subset['sentiment_score'] > 0.5).mean()
            
            # Combine features: [Avg Sentiment, Pos Ratio, ...Centroid...]
            # Weighting: Scalars might be drowned out by 5000 TF-IDF features.
            # Let's upweight scalars or normalize. For now, we append them.
            # To make scalars impactful, we might repeat them or scale them.
            # Simple approach: Concatenate.
            features = np.hstack(([avg_sentiment, pos_ratio], centroid))
            movie_features[title] = features
            
        return movie_features

    def get_similarity_recommendations(self, top_movies, all_movie_features, all_movies_list):
        """
        Finds similar movies for each of the top movies.
        """
        similar_movies = {}
        
        # Convert all features dictionary to a matrix for fast batch cosine similarity
        movie_titles_idx = list(all_movie_features.keys())
        feature_matrix = np.array([all_movie_features[t] for t in movie_titles_idx])
        
        for top_movie in top_movies['movie_title']:
            # Get vector for target movie
            target_vec = all_movie_features[top_movie].reshape(1, -1)
            
            # Compute Cosine Similarity
            sim_scores = cosine_similarity(target_vec, feature_matrix).flatten()
            
            # Get indices of top matches (excluding itself)
            # sort indices descending
            sorted_indices = sim_scores.argsort()[::-1]
            
            recommendations = []
            for idx in sorted_indices:
                candidate = movie_titles_idx[idx]
                if candidate != top_movie:
                    recommendations.append(candidate)
                if len(recommendations) >= 3: # Recommend top 3 similar
                    break
            
            similar_movies[top_movie] = recommendations
            
        return similar_movies

    def generate_recommendations(self, top_n=5):
        """
        Generates recommendations based on the whole dataset.
        Returns: feature-rich Top-N dataframe AND a dictionary of similarity suggestions.
        """
        print("Loading data for recommendation engine...")
        df = load_data()
        if df is None:
            return pd.DataFrame(), {}
            
        # Clean text
        print("Processing reviews for sentiment analysis...")
        clean_reviews = df['review'].apply(self.tp.clean_text)
        df['cleaned_review'] = clean_reviews # Store this for TF-IDF transform later
        
        # Predict Probabilities
        clean_reviews_list = clean_reviews.tolist()
        probs = self.model.predict_proba(self.tfidf.transform(clean_reviews_list))[:, 1]
        df['sentiment_score'] = probs
        
        # Aggregate by Movie
        movie_stats = df.groupby('movie_title').agg({
            'sentiment_score': 'mean',
            'rating': 'mean',
            'review': 'count'
        }).reset_index()
        
        # Hybrid Score Calculation
        movie_stats['norm_rating'] = movie_stats['rating'] / 10.0
        movie_stats['hybrid_score'] = (movie_stats['sentiment_score'] * 0.7) + (movie_stats['norm_rating'] * 0.3)
        
        # Rank Top 5
        top_movies_df = movie_stats.sort_values(by='hybrid_score', ascending=False).head(top_n)
        
        # --- Part 2: Similarity ---
        print("Calculating similarity-based suggestions...")
        movie_features = self.get_movie_features(df)
        similarity_suggestions = self.get_similarity_recommendations(top_movies_df, movie_features, movie_stats['movie_title'].tolist())
        
        return top_movies_df[['movie_title', 'hybrid_score', 'sentiment_score', 'rating']], similarity_suggestions

if __name__ == "__main__":
    rec = Recommender()
    top_movies, similar = rec.generate_recommendations(5)
    print("\nTop 5 Recommended Movies:")
    print(top_movies)
    print("\nSimilarity Suggestions:")
    for movie, suggestions in similar.items():
        print(f"Because you liked {movie}: {', '.join(suggestions)}")
