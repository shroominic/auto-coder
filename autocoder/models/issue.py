

class Issue:
    """ 
    Represents an issue in a repository
    Issues are seen as TODOs in the codebase
    They need to get solved by the bot
    """
    
    def __init__(self, repo, issue_number):
        self.repo = repo
        self.issue_number = issue_number
        
        self.title = None
        self.description = None
        self.comments = []
        self.tags = []
        
    def solve(self):
        """ 
        Solves the issue by creating a pull request
        """
        pass  # TODO implement this