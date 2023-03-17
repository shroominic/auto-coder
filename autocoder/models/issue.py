import requests


class Issue:
    """ 
    Represents an issue in a repository
    Issues are seen as TODOs in the codebase
    They need to get solved by the bot
    """
    
    def __init__(self, issue_url):
        self.issue_url = issue_url
        self.owner, self.repo, self.issue_number = self._extract_issue_info()
        self.repo_info = self._fetch_repo_info()
        self.issue_info = self._fetch_issue_info()
        
    def solve(self):
        """ 
        Solves the issue by creating a pull request
        """
        pass  # TODO implement this

    def _extract_issue_info(self):
        parts = self.issue_url.split("/")
        owner = parts[3]
        repo = parts[4]
        issue_number = parts[6]
        return owner, repo, issue_number

    def _fetch_repo_info(self):
        repo_api_url = f"https://api.github.com/repos/{self.owner}/{self.repo}"
        repo_response = requests.get(repo_api_url)
        return repo_response.json()

    def _fetch_issue_info(self):
        issue_api_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/issues/{self.issue_number}"
        issue_response = requests.get(issue_api_url)
        return issue_response.json()

    @property
    def repo_name(self):
        return self.repo_info['name']

    @property
    def repo_owner(self):
        return self.repo_info['owner']['login']

    @property
    def repo_description(self):
        return self.repo_info['description']

    @property
    def repo_stars(self):
        return self.repo_info['stargazers_count']

    @property
    def repo_forks(self):
        return self.repo_info['forks_count']

    @property
    def issue_title(self):
        return self.issue_info['title']

    @property
    def issue_state(self):
        return self.issue_info['state']

    @property
    def issue_author(self):
        return self.issue_info['user']['login']

    @property
    def issue_created_at(self):
        return self.issue_info['created_at']

    @property
    def issue_updated_at(self):
        return self.issue_info['updated_at']

    @property
    def issue_body(self):
        return self.issue_info['body']
