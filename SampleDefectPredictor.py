from datetime import datetime
from pydriller.repository import Repository
from collections import defaultdict
from repominer.mining.base import BaseMiner, FixingCommitClassifier
from pydriller import ModificationType
import os
import math
import re
import nltk
import numpy as np


BUG_KEYWORDS = ["fix", "bug", "issue", "resolve", "patch", "repair", "error", "fault"]

def is_bug_fix_commit(msg):
    return any(keyword in msg.lower() for keyword in BUG_KEYWORDS)


class PythonMiner(BaseMiner):
    def __init__(self, config):
        super().__init__(config["url_to_repo"], config["clone_repo_to"], config["branch"])
        self.FixingCommitClassifier = PythonFixingCommitClassifier
        self.clone_repo_to = config["clone_repo_to"]
        self.python_files = []
        self.from_date = datetime.strptime(config["from_date"], "%Y-%m-%d")
        self.to_date = datetime.strptime(config["to_date"], "%Y-%m-%d")
        self.developer_data = defaultdict(lambda: {"commits": 0, "files_modified": set(), "bug_fixes": 0})

    def discard_undesired_fixing_commits(self, commits):
        self.sort_commits(commits)
        modified_files = defaultdict(list)
        to_remove = []

        

        for commit in Repository(self.path_to_repo, since=self.from_date, to=self.to_date).traverse_commits():
            dev_email = commit.author.email
            self.developer_data[dev_email]["commits"] += 1

            for mf in commit.modified_files:
                if (
                    mf.change_type == ModificationType.MODIFY
                    and mf.new_path
                    and not self.ignore_file(mf.new_path, None)
                ):
                    modified_files[commit.hash].append(mf.new_path)
                    self.developer_data[dev_email]["files_modified"].add(mf.new_path)

                    if is_bug_fix_commit(commit.msg):  # Replaced hardcoded keywords with helper function ***
                        self.developer_data[dev_email]["bug_fixes"] += 1
                    break
            else:
                to_remove.append(commit.hash)

        commits = [commit_hash for commit_hash in commits if commit_hash not in to_remove]
        return modified_files

    def ignore_file(self, path_to_file, content):
        if not path_to_file.endswith('.py'):
            return True
        path = path_to_file.lower()
        return (
            'test' in path or 'tests' in path or
            os.path.basename(path).startswith('test_') or
            'unittest' in path or 'pytest' in path
        )

    def get_modified_files(self):
        commits = [commit.hash for commit in Repository(
            self.path_to_repo,
            clone_repo_to=self.clone_repo_to,
            only_in_branch=self.branch,
            since=self.from_date,
            to=self.to_date
        ).traverse_commits()]
        self.python_files = self.discard_undesired_fixing_commits(commits)
        return self.python_files

    def get_commit_date(self, commit_hash):
        for commit in Repository(
            self.path_to_repo,
            since=self.from_date,
            to=self.to_date
        ).traverse_commits():
            if commit.hash == commit_hash:
                return commit.author_date
        return None


    # Count how many times each file is imported by others
    def analyze_imports(self):
        import_counts = defaultdict(int)
        for root, _, files in os.walk(self.path_to_repo):
            for file in files:
                if file.endswith(".py"):
                    try:
                        with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            for other_file in files:
                                if other_file.endswith(".py") and other_file != file:
                                    base = other_file.replace(".py", "")
                                    if f"import {base}" in content or f"from {base}" in content:
                                        import_counts[other_file] += 1
                    except Exception:
                        continue
        return import_counts
    
    def calculate_risk(self):
        risk_scores = defaultdict(float)
        mod_counts = defaultdict(int)
        bug_fix_counts = defaultdict(int)
        churn_data = defaultdict(lambda: {"added": 0, "removed": 0})
        author_experience = {}

        if not self.python_files:
            self.get_modified_files()

        commit_dates = {commit: self.get_commit_date(commit) for commit in self.python_files}
        if not commit_dates:
            print("No modified files found in this date range.")
            return {}

        current_rev_date = max(commit_dates.values())

        rename_map = {}
        # collect rename chains
        for commit in Repository(self.path_to_repo, since=self.from_date, to=self.to_date).traverse_commits():
            for mf in commit.modified_files:
                if mf.change_type == ModificationType.RENAME and mf.old_path and mf.new_path:
                    rename_map[mf.old_path] = mf.new_path

        # resolve file path to latest name
        def resolve_latest_path(path):
            seen = set()
            while path in rename_map and path not in seen:
                seen.add(path)
                path = rename_map[path]
            return path

        # process file modifications with resolved paths
        for commit in Repository(self.path_to_repo, since=self.from_date, to=self.to_date).traverse_commits():
            commit_date = commit.author_date
            dev_email = commit.author.email
            author_experience.setdefault(dev_email, []).append(commit_date)

            for mf in commit.modified_files:
                if not mf.new_path or self.ignore_file(mf.new_path, None):
                    continue

                file_path = resolve_latest_path(mf.new_path)

                mod_counts[file_path] += 1

                if is_bug_fix_commit(commit.msg):
                    bug_fix_counts[file_path] += 1

                churn_data[file_path]["added"] += len(mf.diff_parsed["added"])
                churn_data[file_path]["removed"] += len(mf.diff_parsed["deleted"])

        recent_bug_risks = {}
        freq_mod_risks = {}
        bug_fix_risks = {}
        churn_risks = {}
        dev_risks = {}

        # Using log-decayed recent bug weighting (instead of 1 / 2^d)
        for commit_hash, files in self.python_files.items():
            for file_path in files:
                file_path = resolve_latest_path(file_path)
                recent_bug_risks.setdefault(file_path, 0.0)
                d = (current_rev_date - commit_dates[commit_hash]).days
                recent_bug_risks[file_path] += 1 / math.log2(2 + d)

        for file_path in mod_counts:
            freq_mod_risks[file_path] = mod_counts[file_path]
        for file_path in bug_fix_counts:
            bug_fix_risks[file_path] = bug_fix_counts[file_path]
        for file_path, churn in churn_data.items():
            churn_risks[file_path] = churn["added"] + churn["removed"]
        for file_path in mod_counts:
            dev_risks[file_path] = 0.0
            for dev, dates in author_experience.items():
                first = min(dates)
                days_since = (current_rev_date - first).days
                if file_path in self.developer_data[dev]["files_modified"]:
                    dev_risks[file_path] += 1 / (1 + days_since)

        import_counts = self.analyze_imports()
        import_risks = {f: import_counts.get(os.path.basename(f), 0) for f in mod_counts}
        # scale weights based on variance of each factor
        def safe_variance(vals):
            return np.var(list(vals.values())) if vals else 0.0

        vars = {
            "recent": safe_variance(recent_bug_risks),
            "bugfix": safe_variance(bug_fix_risks),
            "freq": safe_variance(freq_mod_risks),
            "churn": safe_variance(churn_risks),
            "dev": safe_variance(dev_risks),
            "import": safe_variance(import_risks)
        }


        total_variance = sum(vars.values())
        if total_variance == 0:
            total_variance = 1.0

        # Normalize each variance to get a weight for that factor
        weights = {}
        for key, value in vars.items():
            weights[key] = value / total_variance


        for file_path in set(mod_counts) | set(bug_fix_counts):
            recent_bug_risk = 0.0
            for commit_hash, files in self.python_files.items():
                if file_path in [resolve_latest_path(f) for f in files]:
                    d = (current_rev_date - commit_dates[commit_hash]).days
                    recent_bug_risk += 1 / math.log2(2 + d)

            dev_risk = 0.0
            for dev, dates in author_experience.items():
                first = min(dates)
                days_since = (current_rev_date - first).days
                if file_path in self.developer_data[dev]["files_modified"]:
                    dev_risk += 1 / (1 + days_since)

            # Final weighted score using variance-based weights
            score = (
                weights["recent"] * recent_bug_risks.get(file_path, 0.0) +
                weights["bugfix"] * bug_fix_risks.get(file_path, 0.0) +
                weights["freq"] * freq_mod_risks.get(file_path, 0.0) +
                weights["churn"] * churn_risks.get(file_path, 0.0) +
                weights["dev"] * dev_risks.get(file_path, 0.0) +
                weights["import"] * import_risks.get(file_path, 0.0)
            )

            file_name = os.path.basename(file_path)
            risk_scores[file_name] += round(score, 4)

        return risk_scores


class PythonFixingCommitClassifier(FixingCommitClassifier):
    def __init__(self, commit):
        super().__init__(commit)
