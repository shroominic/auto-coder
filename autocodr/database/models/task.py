from uuid import UUID
from github import Issue, Repository, Github
from sqlmodel import Field

from autocodr import settings
from .base import Base


class Task(Base, table=True):
    """
    Represents an task to be completed by the autocodr
    Currently, this is just for solving a github issue.
    """
    
    issue_number: int
    repository_label: str
    access_token: str | None
    user_id: UUID = Field(foreign_key="user.id", nullable=False)
    
    def get_repo_and_issue(
        self
    ) -> tuple[Repository.Repository, Issue.Issue]:
        return (
            repo := Github(
                self.access_token
                or settings.GITHUB_ACCESS_TOKEN
            ).get_repo(self.repository_label),
            repo.get_issue(self.issue_number)
        )

    

if __name__ == "__main__":
    from uuid import uuid4
        
    task = Task(
        issue_number=1,
        repository_label="shroominic/codebox-api",
        access_token=None,
        user_id=uuid4()
    )
    repo, issue = task.get_repo_and_issue()
    print(repo.get_git_tree(sha=repo.default_branch))
