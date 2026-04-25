import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from data_loader import load_data, generate_dummy_data
from preprocessing import TextPreprocessor

def train_models():
    # 1. Load Data
    df = load_data()
    if df is None:
        generate_dummy_data()
        df = load_data()
    
    print(f"Data Loaded: {df.shape[0]} reviews.")
    
    # 2. Preprocess (We can do this inside the pipeline or beforehand)
    # Using the preprocessor beforehand to save time during training
    print("Preprocessing text... (This might take a moment)")
    tp = TextPreprocessor()
    df['cleaned_review'] = df['review'].apply(tp.clean_text)
    
    X = df['cleaned_review']
    y = df['sentiment']
    
    # 3. Train Test Split
    print("Splitting data...")
    # Convert to values/list to avoid Series issues with some sklearn versions
    X = X.astype(str).tolist()
    y = y.values
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 4. Pipeline Construction
    # Model 1: Logistic Regression
    print("Training Logistic Regression...")
    pipeline_lr = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000)),
        ('clf', LogisticRegression(max_iter=1000))
    ])
    pipeline_lr.fit(X_train, y_train)
    
    # Model 2: Naive Bayes
    print("Training Naive Bayes...")
    pipeline_nb = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000)),
        ('clf', MultinomialNB())
    ])
    pipeline_nb.fit(X_train, y_train)
    
    # 5. Save Models
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_dir = os.path.join(base_dir, 'models')
    os.makedirs(model_dir, exist_ok=True)
    
    print(f"Saving models to {model_dir}...")
    joblib.dump(pipeline_lr, os.path.join(model_dir, 'logistic_regression.pkl'))
    joblib.dump(pipeline_nb, os.path.join(model_dir, 'naive_bayes.pkl'))
    
    # Save test data for evaluation
    test_data = pd.DataFrame({'review': X_test, 'sentiment': y_test})
    test_data.to_csv(os.path.join(base_dir, 'data', 'test_data.csv'), index=False)
    
    print("Training Complete.")

if __name__ == "__main__":
    train_models()
