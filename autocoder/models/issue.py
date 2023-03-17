import requests


class Issue:
    def __init__(self, repository, issue_number: int):
        self.repository = repository
        self.issue_number = issue_number
        self.issue_info = self._fetch_issue_info()

    def solve(self):
        """ Solve the issue by using GPT4 and start a pull request """
        print("Solving issue: ", self)
        
    def _fetch_issue_info(self):
        issue_api_url = f"https://api.github.com/repos/{self.repository.owner}/{self.repository.repo}/issues/{self.issue_number}"
        issue_response = requests.get(issue_api_url)
        return issue_response.json()

    @property
    def title(self) -> str:
        return self.issue_info['title']

    @property
    def state(self) -> str:
        return self.issue_info['state']

    @property
    def author(self) -> str:
        return self.issue_info['user']['login']

    @property
    def created_at(self) -> str:
        return self.issue_info['created_at']

    @property
    def updated_at(self) -> str:
        return self.issue_info['updated_at']

    @property
    def body(self) -> str:
        return self.issue_info['body']
    
    def __repr__(self) -> str:
        return f"Issue({self.repository}, {self.issue_number})"
    
    def __str__(self) -> str:
        return f"{self.repository} - {self.title}"