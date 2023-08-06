from requests import get as get_request
from sqlalchemy import Column, Integer, ForeignKey
from autocoder.codebase import Codebase
from autocoder.templates import *

from ..utils import get, create, get_or_create
from ..base import Base


class Issue(Base):
    """ 
    Represents an issue on a git repository
    """
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"))
    issue_number = Column(Integer, nullable=False)

    def __init__(self, repository_id, issue_number: int, repository=None):
        self.repository_id = repository_id
        self.issue_number = issue_number
        self.issue_info = self._fetch_issue_info(repository=repository)
        # self.branch_name = self._create_branch() # Check for access token before creating branch
    
    @classmethod
    async def from_url(cls, issue_url: str, access_token=None):
        """ Create an issue from a url """
        from .repository import Repository
        
        repo_url, issue_number = issue_url.split("/issues/")
        issue_number = int(issue_number)
        
        repository = await get_or_create(Repository, repo_url=repo_url, access_token=access_token)
        return await get_or_create(cls, repository_id=repository.id, issue_number=issue_number)
        
    def _fetch_issue_info(self, repository=None):
        issue_api_url = f"https://api.github.com/repos/{repository.owner}/{repository.repo}/issues/{self.issue_number}"
        headers = {}
        if repository.access_token:  # Add the access token to the headers if provided
            headers["Authorization"] = f"Bearer {repository.access_token}"
        issue_response = get_request(issue_api_url, headers=headers)  # Pass headers to the request
        return issue_response.json()

    def _create_branch(self):
        """ Create a branch for the issue """
        branch_name = f"autocoder-issue-{self.issue_number}"
        self.repository.create_branch(branch_name)
        return branch_name
    
    @property
    async def repository(self):
        if hasattr(self, "_repository"):
            return self._repository
        else:
            from .repository import Repository
            repository = await get(Repository, id=self.repository_id)
            self._repository = repository
            return repository
    
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