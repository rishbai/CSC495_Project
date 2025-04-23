import pandas as pd
import json
import os

GROUND_TRUTH_PATH = "ground_truth.csv"
CONFIG_PATH = "config.json"

def run_harness():
    os.system("python3 harness.py")

def generate_and_run_configs(csv_path):
    df = pd.read_csv(csv_path)

    for idx, row in df.iterrows():
        config = {
            "url_to_repo": row["github_url"],
            "clone_repo_to": "/app/Testing",
            "branch": row["branch"],
            "from_date": row["from_date"],
            "to_date": row["to_date"]
        }

        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=4)

        print(f"\nRunning config {idx+1}/{len(df)}...")
        run_harness()

if __name__ == "__main__":
    generate_and_run_configs(GROUND_TRUTH_PATH)
