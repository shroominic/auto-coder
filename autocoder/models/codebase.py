# should represent the local codebase of a repository


class Codebase:
    def __init__(self, repository):
        self.repository = repository
        self.path = self._clone_repository()

    @property
    def tree(self) -> str:
        """ Return a tree of the codebase """
        pass
    
    def show_file(self, file_path) -> str:
        """ Return the contents of a file in the codebase """
        pass
    
    def _clone_repository(self):
        return "path/to/codebase"

    def __repr__(self) -> str:
        return f"Codebase({self.repository})"

    def __str__(self) -> str:
        return f"{self.repository} - {self.codebase}"