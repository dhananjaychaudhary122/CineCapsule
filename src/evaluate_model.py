import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from utils import save_plot, set_plot_style

def evaluate_models():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'test_data.csv')
    model_dir = os.path.join(base_dir, 'models')
    
    if not os.path.exists(data_path):
        print("Test data not found. Please run train_model.py first.")
        return

    print("Loading test data and models...")
    df_test = pd.read_csv(data_path).dropna() # dropna to handle potential glitches
    X_test = df_test['review'].tolist()
    y_test = df_test['sentiment'].values
    
    model_lr = joblib.load(os.path.join(model_dir, 'logistic_regression.pkl'))
    model_nb = joblib.load(os.path.join(model_dir, 'naive_bayes.pkl'))
    
    models = {'Logistic Regression': model_lr, 'Naive Bayes': model_nb}
    set_plot_style()
    
    for name, model in models.items():
        print(f"\n--- Evaluating {name} ---")
        y_pred = model.predict(X_test)
        
        # Metrics
        acc = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {acc:.4f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
        
        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred, labels=['negative', 'positive'])
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Neg', 'Pos'], yticklabels=['Neg', 'Pos'])
        plt.title(f'Confusion Matrix - {name}')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        save_plot(fig, f'confusion_matrix_{name.replace(" ", "_").lower()}.png')
        plt.close()

if __name__ == "__main__":
    evaluate_models()
