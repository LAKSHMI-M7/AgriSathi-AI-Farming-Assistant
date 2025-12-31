import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

def train_crop_model():
    # Load dataset
    data_path = os.path.join(os.path.dirname(__file__), "..", "dataset", "crop_recommendation_dataset_1000.csv")
    df = pd.read_csv(data_path)

    # Features and Target
    X = df[['N', 'P', 'K', 'pH', 'temp', 'rainfall', 'humidity']]
    y = df['crop']

    # Train Random Forest
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Save model
    model_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        
    model_path = os.path.join(model_dir, "crop_model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    
    print(f"Model trained and saved to {model_path}")

if __name__ == "__main__":
    train_crop_model()
