from datetime import datetime
from SampleDefectPredictor import PythonMiner
import os
import json
import pandas as pd

def compare_with_ground_truth(predicted_files, ground_truth_file, config_url, config_start_date, config_end_date):
    """
    Compares the output of defect predictor model with the ground truth CSV file filtered by URL and dates.
    """
    # Load ground truth
    df = pd.read_csv(ground_truth_file)
    
    # Convert date columns in ground truth to datetime (YYYY-MM-DD format)
    df['from_date'] = pd.to_datetime(df['from_date'], format='%Y-%m-%d')  
    df['to_date'] = pd.to_datetime(df['to_date'], format='%Y-%m-%d')      
    
    # Convert config.json dates to datetime (YYYY-MM-DD)
    config_from = pd.to_datetime(config_start_date, format='%Y-%m-%d') 
    config_to = pd.to_datetime(config_end_date, format='%Y-%m-%d')  
    
    # Filter ground truth entries by URL and date range
    mask = (
        (df['github_url'] == config_url) &
        (config_from >= df['from_date']) &
        (config_to <= df['to_date'])
    )
    df_filtered = df[mask]
    
    # Collect all modified files from filtered entries
    ground_truth_files = set()
    for file_list in df_filtered['risky_files']:
        files = [os.path.basename(f.strip()) for f in file_list.split(',')]
        ground_truth_files.update(files)
    
    # Flatten predicted files dictionary to get a set of modified file paths
    predicted_files_set = set()
    for file_list in predicted_files.values():
        predicted_files_set.update([os.path.basename(f) for f in file_list])
    
    # Calculate true positives, false positives, and false negatives
    true_positives = predicted_files_set.intersection(ground_truth_files)
    false_positives = predicted_files_set - ground_truth_files
    false_negatives = ground_truth_files - predicted_files_set
    
    # Print mismatched details
    print("\nFalse Positives (Files predicted but not in ground truth):")
    for fp in false_positives:
        print(fp)
    
    print("\nFalse Negatives (Files in ground truth but not predicted):")
    for fn in false_negatives:
        print(fn)
    
    # Compute evaluation metrics
    accuracy = len(true_positives) / (len(true_positives) + len(false_positives) + len(false_negatives)) if (len(true_positives) + len(false_positives) + len(false_negatives)) > 0 else 0
    print(f"\nAccuracy: {accuracy:.2f}")
    
    return ground_truth_files

def harness_function():
    """
    A harness function to execute the PythonMiner class and get outputs.
    """
    # Load configuration from config.json
    config_file = "config.json"
    with open(config_file, "r") as file:
        config = json.load(file)
    
    # Extract config parameters
    config_url = config['url_to_repo']
    config_start_date = config['from_date']
    config_end_date = config['to_date']
    
    # Initialize the PythonMiner class with the configurations
    miner = PythonMiner(config)
    
    # Retrieve modified Python files
    risky_files = miner.get_modified_files()
    
    # Flatten modified files dictionary to remove commit-level grouping
    all_predicted_files = set()
    for file_list in risky_files.values():
        all_predicted_files.update([os.path.basename(f) for f in file_list])
    
    print("Risky Python files:", all_predicted_files)
    
    # Calculate risk scores
    print("\nCalculating risk scores...")
    risk_scores = miner.calculate_risk()
    print("\nRisk Scores (File Name -> Risk Value):")
    for file_name, risk_value in risk_scores.items():
        print(f"{os.path.basename(file_name)} -> {risk_value}")
    
    # Extract top 3 risky files
    if risk_scores:
        top_3_risky = sorted(risk_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        top_3_files = {os.path.basename(file) for file, _ in top_3_risky}
        
        print("\nTop 3 Risky Files:")
        for file, score in top_3_risky:
            print(f"  - {os.path.basename(file)} -> {score}")

        # Compare only the top 3 risky files with ground truth
        ground_truth_file = "ground_truth.csv"
        print("\nComparing Top 3 Risky Files with Ground Truth...")
        ground_truth_files = compare_with_ground_truth(
            {"predicted": list(top_3_files)},  
            ground_truth_file,
            config_url,
            config_start_date,
            config_end_date
        )
    else:
        print("\nNo risk scores calculated.")

# Execute the harness function
if __name__ == "__main__":
    harness_function()