from requests import get as get_request
from git import Repo, GitCommandError
from sqlalchemy import Column, Integer, String, ForeignKey
from autocoder.codebase import Codebase
from ..base import Base
from .issue import Issue


class Repository(Base):
    """
    Represents a git repository of the user
    """
    __tablename__ = "repositories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    repo_url = Column(String, nullable=False)
    access_token = Column(String, nullable=True)  # TODO: encrypt this
    gptsummary = Column(String, nullable=True)
    
    def __init__(self, repo_url, access_token=None):  # Add an access_token parameter
        self.repo_url = repo_url
        self.access_token = access_token  # Store the access_token
        self.owner, self.repo = self._extract_repo_info()
        self.repo_info = self._fetch_repo_info()
        self.codebase = self._init_codebase()

    def get_issue(self, issue_number) -> Issue:
        return Issue(self, issue_number)
    
    def create_branch(self, branch_name):
        repo = Repo(self.codebase.path)
        
        try:
            repo.git.checkout('-b', branch_name)
            repo.git.push('--set-upstream', 'origin', branch_name)
        except GitCommandError as e:
            if "branch named" in str(e) and "already exists" in str(e):
                print(f"A branch named '{branch_name}' already exists. Switching to the existing branch.")
                repo.git.checkout(branch_name)
            else: raise e
    
    def _extract_repo_info(self):
        parts = self.repo_url.split("/")
        owner = parts[3]
        repo = parts[4]
        return owner, repo

    def _fetch_repo_info(self):
        repo_api_url = f"https://api.github.com/repos/{self.owner}/{self.repo}"
        headers = {}
        if self.access_token:  # Add the access token to the headers if provided
            headers["Authorization"] = f"Bearer {self.access_token}"
        repo_response = get_request(repo_api_url, headers=headers)  # Pass headers to the request
        return repo_response.json()
    
    def _init_codebase(self): return Codebase(self)
    
    @property
    def name(self) -> str: return self.repo_info['name']

    @property
    def description(self) -> str: return self.repo_info['description']
    
    @property
    def keywords(self) -> list: return self.repo_info['topics']
    
    def __repr__(self) -> str: return f"Repository({self.name})"
    
    def __str__(self) -> str: return self.name
