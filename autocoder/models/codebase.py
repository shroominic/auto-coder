from git import Repo
import os
import re


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
    
    def show_file(self, relative_path) -> str:
        with open(os.path.join(self.path, relative_path), "r") as f:
            return f.read()
        
    def file_exists(self, relative_path) -> bool:
        print(os.path.join(self.path, relative_path))
        try:
            return os.path.exists(os.path.join(self.path, relative_path))
        except Exception as e:
            print(e)
            return False
    
    def validate_file_paths(self, file_paths) -> bool:
        return all([
                re.search(r".*\..*", path) is not None
                for path in file_paths
            ]) and all([
                self.file_exists(path.strip("'"))
                for path in file_paths
            ])
            
    def create_file(self, relative_path, content) -> None:
        with open(os.path.join(self.path, relative_path), "w") as f:
            f.write(content)
            
    def change_file(self, relative_path, content) -> None:
        with open(os.path.join(self.path, relative_path), "w") as f:
            f.write(content)
    
    def delete_file(self, relative_path) -> None:
        os.remove(os.path.join(self.path, relative_path))
        
    def commit_changes(self, message) -> None:
        repo = Repo(self.path)
        
        repo.git.add(A=True)
        repo.index.commit(message)
        origin = repo.remote(name='origin')
        origin.push()
    
    def _clone_repository(self):
        repo_path = self.PATH + self.repository.name
        if not os.path.exists(repo_path):
            # Pass the access token as an environment variable for the git clone command
            os.environ['GIT_ASKPASS'] = f'echo {self.repository.access_token}'
            os.environ['GIT_TERMINAL_PROMPT'] = '0'
            Repo.clone_from(self.repository.repo_url, repo_path)
        return repo_path

    def __repr__(self) -> str:
        return f"Codebase({self.repository})"

    def __str__(self) -> str:
        return f"{self.repository} - {self.codebase}"
