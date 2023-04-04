from requests import get as get_request
from sqlalchemy import Column, Integer, String, ForeignKey
from autocoder.codebase import Codebase
from autocoder.templates import *

from ..base import Base


class Issue(Base):
    """ 
    Represents an issue on a git repository
    """
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    repository_id = Column(Integer, ForeignKey("repositories.id"))

    def __init__(self, repository, issue_number: int):
        self.repository = repository
        self.issue_number = issue_number
        self.issue_info = self._fetch_issue_info()
        self.branch_name = self._create_branch()
    
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