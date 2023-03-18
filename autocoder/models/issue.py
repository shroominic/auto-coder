import requests
from utils import ChatGPTSession


class Issue:
    def __init__(self, repository, issue_number: int):
        self.repository = repository
        self.issue_number = issue_number
        self.issue_info = self._fetch_issue_info()

    def solve(self):
        """ Solve the issue by using GPT4 and start a pull request """
        session = ChatGPTSession()
        session.history.append({
            "role": "system",
            "content": f"""
            The following is a conversation about solving issue {self.issue_number} on {self.repository}.
            Title: {self.title}
            Description: {self.body}
            Project paths: {self.repository.codebase.tree}
            """
            }) 
        session.history.append({
            "role": "user",
            "content": f"""
            What files are relevant to this issue? 
            Create a list "read" and a list "write" and put all files as path in there to solve the issue.
            Format it like this:
            read = ["path/to/file1.py", "path/to/file2.py"]
            write = ["path/to/file3.py"]
            Reply only with a code block containing the lists.
            """
            })
        # TODO: Check if answer is valid and regex match lists into variables
        
        # TODO: go over all read files and summarize them
        
        # TODO: go over all write files and do changes
        
        # TODO: test the code and repeat until it works
        
        # TODO: create a pull request
        
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