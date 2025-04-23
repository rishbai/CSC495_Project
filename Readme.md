# Defect Predictor using RepoMiner

This project provides an implementation of a Defect Predictor by leveraging RepoMiner and PyDriller to analyze commit history and predict the risk associated with files in a given revision. It extends the RepoMiner example and includes risk calculation based on commit history.

## Features
- Traverse Git repositories to identify modified Python files.
- Classify fixing commits using a `FixingCommitClassifier`.
- Calculate risk scores for Python files based on bug revisions and modification frequency.

# Setup Instructions


## Installation
Follow the steps below to set up and run the project:

### 1. Clone the repository

```bash
git clone https://github.com/rishbai/CSC495_Project.git
```

### 2. Build the docker file
Create a docker image (see Dockerfile) for the project: 
```bash
docker build -t defect-predictor .
```

### 3. Run the project
Run the docker container from the image. See instruction RUN at the end of Dockerfile. It will execute the harness function within a docker container, print the results, and exit.
```bash
docker run --rm -it defect-predictor
```
### 4. Running Batch Evaluation with `run_all_configs.py`

To evaluate your defect predictor across multiple repositories or configurations, you can use the `run_all_configs.py` script. This script automates the process of running the predictor on a series of configuration files and prints risk scores and accuracy results for each.

#### To run:

```bash
python run_all_configs.py
```


  #### Expected output:
  ```plaintext
  Running config 1/21...
Risk Scores (File Name -> Risk Value):
transcribe.py -> 149.4837
decoding.py -> 110.4011
utils.py -> 73.1007
...

Top 3 Risky Files:
  - transcribe.py -> 149.4837
  - decoding.py -> 110.4011
  - utils.py -> 73.1007

False Positives (Files predicted but not in ground truth):
decoding.py

False Negatives (Files in ground truth but not predicted):
timing.py

Accuracy: 0.50

  ```

  ### Explanation of outputs:
  - **Modified Files**: Lists all Python files that were modified during the specified period, based on the defect predictor analysis.
  - **Comparison with Ground Truth**: 
    The comparison is based on a ground truth file, which contains a list of files modified between a start and end date. This ground truth data is compared with the predictions made by the sample defect predictor model to assess its accuracy.
    - **False Positives**: Files that were predicted by the model but are not in the ground truth.
    - **False Negatives**: Files that are in the ground truth but were not predicted by the model.
    - **Precision, Recall, and F1 Score**: Metrics that summarize the prediction accuracy of the model.
  - **Risk Scores**: Displays the calculated risk scores for each modified file.
  

## Overview of files

  ### SampleDefectPredictor.py:
  - This is the core logic for defect prediction. It performs the following:
    - **Repository Analysis**: Uses PyDriller to scan Git commit history for Python files modified in the configured date range.
    - **Fix Detection**: Tags commits as fixing commits using a rule-based keyword search (e.g., "fix", "bug", "issue").
    - **Risk Calculation**: Assigns a risk score to each file based on:
      - Number of distinct contributors who modified it.
      - Frequency of modifications across commits.
      - Whether it was involved in fixing commits.
    - **Output**: Returns a set of predicted risky files along with their associated risk scores.
  ### harness.py
  - This script runs the defect predictor (SampleDefectPredictor.py) logic to generate a list of modified files, calculate their risk scores, and compare the results with a ground truth file. Please note that this file should not be modified, as your implementation is expected to function using it as is.
 ### run_all_configs.py:
  - Automates the execution of the defect predictor using multiple configuration files.
    - Iterates over all .json files in a specified directory.
    - Loads each config file and runs the prediction process.
    - Prints precision, recall, and F1 score for each configuration.
  - Useful for benchmarking the model across various repositories, branches, or time intervals.
  - File is used primarily for running multiple tests simultaneously. Not neccesary for system deployment
  ### requirements.txt
  - Lists all the dependencies and libraries required to run the project seamlessly.
  ### ground_truth.csv
  - Provides a reference dataset containing start and end dates along with the modified files. It is used to compare expected results with actual outputs. You can test various scenarios by customizing this file.
  ### config.json
  - Allows you to specify the repository to be tested, the local path where it should be cloned, the branch to analyze, and the start and end dates for conducting tests within a specified time frame.
  ### Docker 
  - Sets up the necessary environment with Python, Git, dependencies, and your project files to run the defect predictor seamlessly inside a container.
