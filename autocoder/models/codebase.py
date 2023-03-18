from git import Repo
import os


class Codebase:
    """ should represent the local codebase of a repository """
    PATH = "autocoder/.codebases/"
    
    def __init__(self, repository):
        self.repository = repository
        self.path = self._clone_repository()
        self.ignore = [".git"]

    @property
    def tree(self) -> str:
        tree = []
        for folder, _, files in os.walk(self.path):
            if all([ignore not in folder for ignore in self.ignore]):
                folder_relative = os.path.relpath(folder, self.path)
                for file in files:
                    tree.append(os.path.join(folder_relative, file))
        return "\n".join(tree)
    
    def show_file(self, file_path) -> str:
        with open(os.path.join(self.path, file_path), "r") as f:
            return f.read()
    
    def _clone_repository(self):
        repo_path = self.PATH + self.repository.name
        if not os.path.exists(repo_path):
            Repo.clone_from(self.repository.repo_url, repo_path)
        return repo_path

    def __repr__(self) -> str:
        return f"Codebase({self.repository})"

    def __str__(self) -> str:
        return f"{self.repository} - {self.codebase}"