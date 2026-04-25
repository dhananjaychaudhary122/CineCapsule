import sys
import os
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__)))

from train_model import train_models
from evaluate_model import evaluate_models
from recommendation import Recommender
import joblib

def main():
    print("="*60)
    print("      CineCapsule – Sentiment-Driven Recommendation System")
    print("="*60)
    
    # 1. Training Phase
    # Check if models exist, else train
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, 'models', 'logistic_regression.pkl')
    
    if not os.path.exists(model_path):
        print("\n[INFO] Models not found. Starting training pipeline...")
        train_models()
    else:
        print("\n[INFO] Models found. Using existing trained models.")
        # Optional: Ask user if they want to retrain
        # train_models() 
        
    # 2. Evaluation Phase
    print("\n[INFO] Evaluating Models...")
    evaluate_models()
    
    # 3. Recommendation Phase
    print("\n[INFO] Generating Recommendations...")
    try:
        rec = Recommender()
        top_movies, similar_movies = rec.generate_recommendations(top_n=5)
        
        # Prepare Output String
        output_lines = []
        output_lines.append("\n" + "*"*60)
        output_lines.append("          TOP 5 HIGHEST RANKED MOVIES")
        output_lines.append("*"*60)
        output_lines.append(top_movies[['movie_title', 'hybrid_score', 'sentiment_score', 'rating']].to_string(index=False))
        
        output_lines.append("\n" + "*"*60)
        output_lines.append("      DEBUG: SIMILARITY-BASED SUGGESTIONS")
        output_lines.append("*"*60)
        
        top_titles_set = set(top_movies['movie_title'].values)
        
        for movie_title in top_movies['movie_title']:
            output_lines.append(f"\nSince you liked '{movie_title}':")
            suggestions = similar_movies.get(movie_title, [])
            filtered_suggestions = [m for m in suggestions if m not in top_titles_set]
            
            if filtered_suggestions:
                for sm in filtered_suggestions[:3]:
                    output_lines.append(f"  -> {sm}")
            else:
                output_lines.append("  -> No other distinct similar movies found.")
        
        # Print to Console
        full_output = "\n".join(output_lines)
        print(full_output)
        
        # Save to File
        os.makedirs(os.path.join(base_dir, 'outputs'), exist_ok=True)
        with open(os.path.join(base_dir, 'outputs', 'results.txt'), 'w', encoding='utf-8') as f:
            f.write(full_output)
            
        print(f"\n[SUCCESS] Pipeline executed successfully. Results saved to {os.path.join(base_dir, 'outputs', 'results.txt')}")
        
    except Exception as e:
        print(f"\n[ERROR] Recommendation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
