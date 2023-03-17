import requests
from .issue import Issue


class Repository:
    def __init__(self, repo_url):
        self.repo_url = repo_url
        self.owner, self.repo = self._extract_repo_info()
        self.repo_info = self._fetch_repo_info()

    def get_issue(self, issue_number) -> Issue:
        return Issue(self, issue_number)
    
    def _extract_repo_info(self):
        parts = self.repo_url.split("/")
        owner = parts[3]
        repo = parts[4]
        return owner, repo

    def _fetch_repo_info(self):
        repo_api_url = f"https://api.github.com/repos/{self.owner}/{self.repo}"
        repo_response = requests.get(repo_api_url)
        return repo_response.json()

    @property
    def name(self) -> str:
        return self.repo_info['name']

    @property
    def description(self) -> str:
        return self.repo_info['description']
    
    def __repr__(self) -> str:
        return f"Repository({self.name})"
    
    def __str__(self) -> str:
        return self.name
