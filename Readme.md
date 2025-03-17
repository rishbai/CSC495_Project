# Defect Predictor using RepoMiner

This project provides an implementation of a Defect Predictor by leveraging RepoMiner and PyDriller to analyze commit history and predict the risk associated with files in a given revision. It extends the RepoMiner example and includes risk calculation based on commit history.

## Features
- Traverse Git repositories to identify modified Python files.
- Classify fixing commits using a `FixingCommitClassifier`.
- Calculate risk scores for Python files based on bug revisions and modification frequency.

# Setup Instructions

## Prerequisites
- Python version **<3.9**.
- Git version **>=2.38.0**.
- Dependencies listed in `requirements.txt`.

## Installation
Follow the steps below to set up and run the project:

### 1. Install the required Python libraries
- Make sure you have Python installed (less than version 3.9). Create a virtual environment using the following commands:

```bash
python -m venv myenv
```
- Activate the virtual environment.
  
For Linux/macOS:
```bash
source myenv/bin/activate
```
For windows:
```bash
.\myenv\Scripts\activate
```
- After activating the environment, use the following command to install the required dependencies:
```bash
pip install -r requirements.txt
```
- Additionally, download the spaCy statistical model `en_core_web_sm` for use with the `FixingCommitClassifier`:
```bash
python -m spacy download en_core_web_sm
```

### 2. Update Configuration file
Provide the repository URL and target clone directory for defect prediction in the config file. For example:
```bash
url_to_repo = "https://github.com/sample_user/sample_repo.git"
clone_repo_to = "C:\\path_to_directory"
branch = "master"
from_date="YYYY-MM-DD"
to_date="YYYY-MM-DD"
```

### 3. Run the project
Run the harness function to execute the `PythonMiner` class and generate results:
```bash
python harness.py
```

### 4. Outputs
- **Modified Files**: Lists all Python files that were modified.
- **Risk Scores**: Displays the calculated risk scores for each file.

### Example Output
```plaintext
Retrieving modified Python files...
Modified files debug output: {'commit_hash1': ['file1.py', 'file2.py'], 'commit_hash2': ['file3.py']}

Calculating risk scores...

Risk Scores (File Name -> Risk Value):
file1.py -> 1.23
file2.py -> 0.67
file3.py -> 2.45
```

