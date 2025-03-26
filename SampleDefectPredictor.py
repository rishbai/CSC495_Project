from datetime import datetime
from pydriller.repository import Repository
from collections import defaultdict
from repominer.mining.base import BaseMiner, FixingCommitClassifier
from pydriller import ModificationType


class PythonMiner(BaseMiner):
    def __init__(self, config):
        super().__init__(
            config["url_to_repo"],
            config["clone_repo_to"],
            config["branch"]
        )
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

            i = 0
            while i < len(commit.modified_files):
                mf = commit.modified_files[i]
                if (
                    mf.change_type == ModificationType.MODIFY
                    and mf.new_path
                    and mf.new_path.endswith('.py')
                ):
                    modified_files[commit.hash].append(mf.new_path)
                    self.developer_data[dev_email]["files_modified"].add(mf.new_path)

                    # Check if commit message contains bug-fix keywords
                    if any(keyword in commit.msg.lower() for keyword in ["fix", "bug", "issue"]):
                        self.developer_data[dev_email]["bug_fixes"] += 1
                    break
                i += 1
            if i == len(commit.modified_files):
                to_remove.append(commit.hash)
        
        commits = [commit_hash for commit_hash in commits if commit_hash not in to_remove]
        return modified_files

    def ignore_file(self, path_to_file, content):
        return not path_to_file.endswith('.py')
    
    def get_modified_files(self):
        """
        Retrieves modified Python files using discard_undesired_fixing_commits.
        """
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
        """Fetches the commit date for a given commit hash using PyDriller."""
        repo = Repository(self.path_to_repo)  
        for commit in repo.traverse_commits():
            if commit.hash == commit_hash:
                return commit.author_date  
        return None

    def calculate_risk(self):
        risk_scores = defaultdict(float)
        mod_counts = defaultdict(int)
        bug_fix_counts = defaultdict(int)
        churn_data = defaultdict(lambda: {"added": 0, "removed": 0})
        author_experience = {}

        if not self.python_files:
            self.get_modified_files()

        # Map commits to dates
        commit_dates = {commit: self.get_commit_date(commit) for commit in self.python_files}
        if not commit_dates:
            print("No modified files found in this date range. Exiting risk calculation.")
            return risk_scores

        current_rev_date = max(commit_dates.values())

        for commit in Repository(self.path_to_repo, since=self.from_date, to=self.to_date).traverse_commits():
            commit_date = commit.author_date
            dev_email = commit.author.email
            author_experience.setdefault(dev_email, []).append(commit_date)

            for mf in commit.modified_files:
                if not mf.new_path or not mf.new_path.endswith('.py'):
                    continue

                file_path = mf.new_path
                mod_counts[file_path] += 1

                if any(keyword in commit.msg.lower() for keyword in ["fix", "bug", "issue"]):
                    bug_fix_counts[file_path] += 1

                churn_data[file_path]["added"] += len(mf.diff_parsed["added"])
                churn_data[file_path]["removed"] += len(mf.diff_parsed["deleted"])

        for file_path in set(list(mod_counts) + list(bug_fix_counts)):
            recent_bug_risk = 0.0
            for commit_hash, files in self.python_files.items():
                if file_path in files:
                    d = (current_rev_date - commit_dates[commit_hash]).days
                    recent_bug_risk += 1 / (2 ** d)

            freq_mod_risk = mod_counts[file_path]
            bug_fix_risk = bug_fix_counts[file_path]
            churn_risk = churn_data[file_path]["added"] + churn_data[file_path]["removed"]

            # Developer risk: average # of days since their first commit
            dev_risk = 0.0
            for dev, dates in author_experience.items():
                first = min(dates)
                days_since = (current_rev_date - first).days
                if file_path in self.developer_data[dev]["files_modified"]:
                    dev_risk += 1 / (1 + days_since)

            # Final weighted risk score
            score = (
                0.4 * recent_bug_risk +
                0.2 * bug_fix_risk +
                0.2 * freq_mod_risk +
                0.1 * churn_risk +
                0.1 * dev_risk
            )
            risk_scores[file_path] = round(score, 4)

        # Debug print
        print("\nDeveloper Contributions:")
        for dev_email, stats in self.developer_data.items():
            print(f"Developer: {dev_email}, Commits: {stats['commits']}, Bug Fixes: {stats['bug_fixes']}, Files Modified: {len(stats['files_modified'])}")

        print("\nRisk Scores (File -> Score):")
        for f, s in sorted(risk_scores.items(), key=lambda x: -x[1]):
            print(f"{f} -> {s}")

        return risk_scores


class PythonFixingCommitClassifier(FixingCommitClassifier):
    def __init__(self, commit):
        super().__init__(commit)
