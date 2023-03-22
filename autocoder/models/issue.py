import requests
from promptkit import ChatGPTSession
from promptkit.tools import summarize
import re


class Issue:
    """ Represents an issue on a git repository """
    def __init__(self, repository, issue_number: int):
        self.repository = repository
        self.issue_number = issue_number
        self.issue_info = self._fetch_issue_info()

    def solve(self):
        """ Solve the issue by using GPT4 and start a pull request """
        session = ChatGPTSession(model="gpt-3.5-turbo")
        session.add_system(
            f"""
            The following is a conversation about solving issue {self.issue_number} on {self.repository}.
            Title:
            {self.title}
            
            Description:
            {self.body}
            
            Your task is to solve the issue by using the codebase of the repository.
            """
        )
        session.add_user(
            f"""
            First write a detailed instruction on how to solve the issue.
            Explain what technologies are used and what files are relevant.
            
            Codebase:
            {self.repository.codebase.tree}
            
            Create a list called "relevant_files" and 
            write down all files as path that are relevant for solving the issue.
            
            Reply with a codeblock like this:
            ```python
            relevant_files = [
                "path/to/file1.py",  # do not start with ./ or /
                "path/to/file2.py"
                ...
            ]
            ```
            """
        )
        response = session.get_response().get_codeblock()
        paths = re.findall(r"\"(.*?)\"", response)
        
        for path in paths:
            file_path = f"autocoder/.codebases/{self.repository.repo}/{path}"
            print(file_path)
            with open(file_path, "r") as file:
                file_content = file.read()
                summary = summarize(f"# {file_path}\nfile_content")
                print(summary)
                session.add_user(
                    f"""
                    Here is a summary of the file {file_path}:
                    {summary}
                    """
                )
                session.add_user(
                    f"""
                    Is this file relevant for solving the issue?
                    File path: {file_path}
                    Issue title: {self.title}
                    Issue description: {self.body}
                    Reply only with "Yes" or "No". 
                    """
                )
                is_yes = session.get_response().get_bool()
                print(is_yes)
                if is_yes:
                    session.add_user(
                        f"""
                        First write a detailed instruction on how to change the file {file_path}.
                        File content:
                        {file_content}
                        
                        Create a list called "changes",
                        write down all changes as a dictionary and 
                        reply with a codeblock like this:
                        """
                        """
                        ```python
                        changes = [
                            {"line": 1, "old": "old code", "new": "new code"},
                            {"line": 2, "old": "old code", "new": "new code"},
                            ...
                        ]
                        ```
                        """)
                    response = session.get_response().get_codeblock()
                    changes = re.findall(r"\"(.*?)\"", response)
                    for change in changes:
                        print(change)
        
        # TODO: test the code and repeat until it works
        
        # TODO: create a pull request

    def _fetch_issue_info(self):
        issue_api_url = f"https://api.github.com/repos/{self.repository.owner}/{self.repository.repo}/issues/{self.issue_number}"
        headers = {}
        if self.repository.access_token:  # Add the access token to the headers if provided
            headers["Authorization"] = f"Bearer {self.repository.access_token}"
        issue_response = requests.get(issue_api_url, headers=headers)  # Pass headers to the request
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