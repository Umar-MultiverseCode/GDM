import pandas as pd
import numpy as np

# Load original dataset
try:
    df = pd.read_csv('diabetesGDM (1).csv')
    print(f"Original dataset size: {len(df)}")
except:
    print("Dataset not found!")
    exit()

def augment_data(df, target_size=2000):
    current_size = len(df)
    needed = target_size - current_size
    
    if needed <= 0:
        return df
    
    print(f"Augmenting with {needed} new synthetic records...")
    
    # Selecting existing rows randomly to duplicate with noise
    synthetic_records = []
    
    for _ in range(needed):
        # Randomly pick a sample from original
        sample = df.sample(1).iloc[0].copy()
        
        # Add slight intelligent noise to numerical columns
        # Glucose (+/- 5%)
        sample['Glucose'] *= np.random.uniform(0.95, 1.05)
        # BMI (+/- 3%)
        sample['BMI'] *= np.random.uniform(0.97, 1.03)
        # BloodPressure (+/- 5%)
        if sample['BloodPressure'] > 0:
            sample['BloodPressure'] *= np.random.uniform(0.95, 1.05)
        # Insulin (+/- 10%)
        if sample['Insulin'] > 0:
            sample['Insulin'] *= np.random.uniform(0.90, 1.10)
        # Age (+/- 2 years, capped at min 21)
        sample['Age'] = max(21, sample['Age'] + np.random.randint(-2, 3))
        # DPF (+/- 5%)
        sample['DiabetesPedigreeFunction'] *= np.random.uniform(0.95, 1.05)
        
        synthetic_records.append(sample)
        
    synthetic_df = pd.DataFrame(synthetic_records)
    new_df = pd.concat([df, synthetic_df], ignore_index=True)
    
    # Basic rounding/cleanup
    new_df['Pregnancies'] = new_df['Pregnancies'].apply(round)
    new_df['Glucose'] = new_df['Glucose'].apply(round)
    new_df['BloodPressure'] = new_df['BloodPressure'].apply(round)
    new_df['SkinThickness'] = new_df['SkinThickness'].apply(round)
    new_df['Insulin'] = new_df['Insulin'].apply(round)
    new_df['Age'] = new_df['Age'].apply(round)
    new_df['Outcome'] = new_df['Outcome'].apply(round)
    
    return new_df

# Generate extended dataset (1 Lakh records)
extended_df = augment_data(df, target_size=100000)

# Save to the SAME file name (or new if requested, but same is easier for the app)
extended_df.to_csv('diabetesGDM (1).csv', index=False)
print(f"Dataset successfully extended to {len(extended_df)} records.")

# Re-train the model automatically with new data
print("Re-training model with extended data...")
import train_model
print("Model re-trained and saved.")
