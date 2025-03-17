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
        
    def discard_undesired_fixing_commits(self, commits):
        self.sort_commits(commits)
        modified_files = defaultdict(list)
        to_remove = []

        for commit in Repository(self.path_to_repo, since=self.from_date, to=self.to_date).traverse_commits():
            i = 0
            while i < len(commit.modified_files):
                mf = commit.modified_files[i]
                if (
                    mf.change_type == ModificationType.MODIFY
                    and mf.new_path
                    and mf.new_path.endswith('.py')
                ):
                    modified_files[commit.hash].append(mf.new_path)
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

        if not self.python_files:
            self.get_modified_files()

        commit_dates = {commit: self.get_commit_date(commit) for commit in self.python_files.keys()}
        sorted_commits = sorted(commit_dates.items(), key=lambda x: x[1])  
        current_rev = max(commit_dates.values())  

        for commit_hash, commit_date in sorted_commits:
            for file_path in self.python_files[commit_hash]:
                d = (current_rev - commit_date).days  
                risk_scores[file_path] += 1 / (2 ** d) 

        return risk_scores

class PythonFixingCommitClassifier(FixingCommitClassifier):
    def __init__(self, commit):
        super().__init__(commit)
