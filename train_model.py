# Optimized training parameters for large datasets
import logging
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle

# Configure logging for production diagnostics
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def train_gdm_model(data_path: str, model_save_path: str):
    """
    Executes the end-to-end model training pipeline: data loading, 
    preprocessing, training, evaluation, and serialization.
    """
    logging.info(f"Loading dataset from {data_path}...")
    df = pd.read_csv(data_path)

    # Preprocessing: Handle missing values (0s are missing in this clinical context)
    logging.info("Executing clinical data preprocessing and imputation...")
    cols_with_zeros = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    for col in cols_with_zeros:
        df[col] = df[col].replace(0, np.nan)
        df[col] = df[col].fillna(df[col].mean())

    # Feature engineering and separation
    X = df.drop('Outcome', axis=1)
    y = df['Outcome']

    # Dataset partition (80/20 split)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model training: Random Forest Classifier
    logging.info("Training Random Forest Classifier (n_estimators=100)...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Performance Evaluation
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    logging.info(f"Model Training Complete. Diagnostic Accuracy: {accuracy:.4f}")
    
    # Detailed telemetry
    print("\n--- Clinical Classification Report ---")
    print(classification_report(y_test, y_pred))

    # Binary Serialization
    with open(model_save_path, 'wb') as f:
        pickle.dump(model, f)
    logging.info(f"Binary model successfully persisted to {model_save_path}")

if __name__ == "__main__":
    train_gdm_model('diabetesGDM (1).csv', 'gdm_model.pkl')