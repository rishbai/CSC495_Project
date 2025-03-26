from datetime import datetime
from SampleDefectPredictor import PythonMiner
import os
import json
import pandas as pd


def compare_with_ground_truth(predicted_files, ground_truth_file):
    """
    Compares the output of PythonMiner with the ground truth CSV file.
    
    :param predicted_files: Dictionary {commit_hash: [modified_files]}
    :param ground_truth_file: Path to the ground truth CSV file
    """
    # Load ground truth
    df = pd.read_csv(ground_truth_file)
    ground_truth_files = set(df['modified_files'].dropna().tolist())  # Convert to set for easy comparison
    
    # Flatten predicted files dictionary to get a set of modified file paths
    predicted_files_set = set()
    for file_list in predicted_files.values():
        predicted_files_set.update(file_list)
    
    # Calculate true positives, false positives, and false negatives
    true_positives = predicted_files_set.intersection(ground_truth_files)
    false_positives = predicted_files_set - ground_truth_files
    false_negatives = ground_truth_files - predicted_files_set
    
    # Print comparison results
    print(f"Total Files in Ground Truth: {len(ground_truth_files)}")
    print(f"Total Files Predicted by the defect predictor: {len(predicted_files_set)}")
    
    # Print mismatched details
    print("\nFalse Positives (Files predicted but not in ground truth):")
    for fp in false_positives:
        print(fp)
    
    print("\nFalse Negatives (Files in ground truth but not predicted):")
    for fn in false_negatives:
        print(fn)
    
    # Compute evaluation metrics
    precision = len(true_positives) / (len(true_positives) + len(false_positives)) if (len(true_positives) + len(false_positives)) > 0 else 0
    recall = len(true_positives) / (len(true_positives) + len(false_negatives)) if (len(true_positives) + len(false_negatives)) > 0 else 0
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    print(f"\nPrecision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1 Score: {f1_score:.2f}")

def harness_function():
    """
    A harness function to execute the PythonMiner class and get outputs.
    """
    # Load configuration from config.json
    config_file = "config.json"
    with open(config_file, "r") as file:
        config = json.load(file)
    
    # Initialize the PythonMiner class with the configurations
    miner = PythonMiner(config)
    
    # Retrieve modified Python files
    print("Retrieving modified Python files...")
    modified_files = miner.get_modified_files()
    
    # Flatten modified files dictionary to remove commit-level grouping
    all_predicted_files = set()
    for file_list in modified_files.values():
        all_predicted_files.update(file_list)
    
    print("Modified files debug output:", all_predicted_files)
    
    # Compare with ground truth
    ground_truth_file = "ground_truth.csv"
    print("\nComparing with Ground Truth...")
    compare_with_ground_truth({"predicted": list(all_predicted_files)}, ground_truth_file)
    
    # Calculate risk scores
    print("\nCalculating risk scores...")
    risk_scores = miner.calculate_risk()
    print("\nRisk Scores (File Name -> Risk Value):")
    for file_name, risk_value in risk_scores.items():
        print(f"{file_name} -> {risk_value}")

# Execute the harness function
if __name__ == "__main__":
    harness_function()
