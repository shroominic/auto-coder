from requests import get as get_request
from sqlalchemy import Column, Integer, ForeignKey
from autocoder.codebase import Codebase
from autocoder.templates import *

from ..base import SpecialBase
from ..engine import session


class Issue(SpecialBase):
    """ 
    Represents an issue on a git repository
    """
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"))
    issue_number = Column(Integer, nullable=False)

    def __init__(self, repository_id, issue_number: int):
        self.repository_id = repository_id
        self.issue_number = issue_number
        self.issue_info = self._fetch_issue_info()
        # self.branch_name = self._create_branch() # Check for access token before creating branch
    
    @classmethod
    def from_url(cls, issue_url: str, access_token=None):
        """ Create an issue from a url """
        from .repository import Repository
        
        repo_url, issue_number = issue_url.split("/issues/")
        issue_number = int(issue_number)
        repository = Repository.get_or_create(session, repo_url=repo_url, access_token=access_token)
        return cls.get_or_create(session, repository_id=repository.id, issue_number=issue_number)
        
    def _fetch_issue_info(self):
        issue_api_url = f"https://api.github.com/repos/{self.repository.owner}/{self.repository.repo}/issues/{self.issue_number}"
        headers = {}
        if self.repository.access_token:  # Add the access token to the headers if provided
            headers["Authorization"] = f"Bearer {self.repository.access_token}"
        issue_response = get_request(issue_api_url, headers=headers)  # Pass headers to the request
        return issue_response.json()

    def _create_branch(self):
        """ Create a branch for the issue """
        branch_name = f"autocoder-issue-{self.issue_number}"
        self.repository.create_branch(branch_name)
        return branch_name
    
    @property
    def repository(self): 
        from .repository import Repository
        return Repository.get(session, id=self.repository_id)
    
    @property
    def title(self) -> str: return self.issue_info['title']

    @property
    def state(self) -> str: return self.issue_info['state']

    @property
    def author(self) -> str: return self.issue_info['user']['login']

    @property 
    def created_at(self) -> str: return self.issue_info['created_at']

    @property
    def updated_at(self) -> str: return self.issue_info['updated_at']

    @property
    def body(self) -> str: return self.issue_info['body']

    @property
    def codebase(self) -> Codebase: return self.repository.codebase
    
    def __repr__(self) -> str: return f"Issue({self.repository}, {self.issue_number})"
    
    def __str__(self) -> str: return f"{self.repository} - {self.title}"