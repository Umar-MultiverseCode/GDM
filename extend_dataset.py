import logging
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def augment_data(df: pd.DataFrame, target_size: int = 2000) -> pd.DataFrame:
    """
    Performs data augmentation using stochastic noise injection to 
    simulate clinical variability in synthetic records.
    
    Args:
        df (pd.DataFrame): The source clinical dataset.
        target_size (int): The desired total count of records.
        
    Returns:
        pd.DataFrame: The expanded dataset including synthetic samples.
    """
    current_size = len(df)
    needed = target_size - current_size
    
    if needed <= 0:
        logging.info("Dataset already meets or exceeds target size. No augmentation required.")
        return df
    
    logging.info(f"Initiating augmentation sequence for {needed} synthetic clinical records...")
    
    synthetic_records = []
    
    # Process augmentation with Gaussian-like noise for feature realism
    for _ in range(needed):
        sample = df.sample(1).iloc[0].copy()
        
        # Clinical parameter variability simulation
        sample['Glucose'] *= np.random.uniform(0.95, 1.05)
        sample['BMI'] *= np.random.uniform(0.97, 1.03)
        
        if sample['BloodPressure'] > 0:
            sample['BloodPressure'] *= np.random.uniform(0.95, 1.05)
            
        if sample['Insulin'] > 0:
            sample['Insulin'] *= np.random.uniform(0.90, 1.10)
            
        sample['Age'] = max(21, int(sample['Age'] + np.random.randint(-2, 3)))
        sample['DiabetesPedigreeFunction'] *= np.random.uniform(0.95, 1.05)
        
        synthetic_records.append(sample)
        
    synthetic_df = pd.DataFrame(synthetic_records)
    new_df = pd.concat([df, synthetic_df], ignore_index=True)
    
    # Post-processing: Quantize clinical metrics to integer representations
    quantize_cols = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'Age', 'Outcome']
    for col in quantize_cols:
        new_df[col] = new_df[col].round().astype(int)
    
    return new_df

def main():
    source_file = 'diabetesGDM (1).csv'
    target_records = 100000
    
    try:
        logging.info(f"Loading primary source: {source_file}")
        df = pd.read_csv(source_file)
    except FileNotFoundError:
        logging.error(f"Critical Error: Data source '{source_file}' not found. Aborting.")
        return

    # Execute Augmentation
    extended_df = augment_data(df, target_size=target_records)
    
    # Persist Expanded Dataset
    extended_df.to_csv(source_file, index=False)
    logging.info(f"Dataset successfully persisted with {len(extended_df)} records.")

    # Re-train the model to capture expanded data distribution
    logging.info("Starting automated model re-calibration...")
    from train_model import train_gdm_model
    train_gdm_model(source_file, 'gdm_model.pkl')
    logging.info("Model re-calibration complete. System ready.")

if __name__ == "__main__":
    main()
