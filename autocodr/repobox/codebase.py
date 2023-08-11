from codeboxapi import CodeBox  # type: ignore
from github.Repository import Repository

class CodeBase(CodeBox):
    def __init__(self):
        super().__init__()
        self.codebox = CodeBox()
        
    @classmethod
    async def from_repo(cls, repository: Repository, access_token=None):
        codebase = cls()
        await codebase._clone(repository, access_token)
        return codebase

    async def _clone(self, repository: Repository, access_token=None):
        await self.codebox.arun(
            f"import os; os.system('git clone {repository.clone_url} .')"
        )
        
    
    async def read_file(self, relative_path: str) -> bytes | None:
        return (
            await self.codebox.adownload(relative_path)
        ).content
    
    async def show_tree(self) -> str | None:
        return (
            await self.codebox.arun("import os; os.walk('.')")
        ).content

    async def show_file(self, relative_path: str) -> str | None:
        # TODO: check max string length
        return (
            await self.codebox.arun(f"open('{relative_path}').read()")
        ).content

    async def file_exists(self, relative_path) -> bool:
        # TODO: test this
        return (
            await self.codebox.arun(f"import os; os.path.exists('{relative_path}')")
        ).content == "True"

    async def validate_file_paths(self, file_paths):
        # TODO test this
        return bool((
            await self.codebox.arun(
                f"import re; all([re.search(r'.*\\..*', path)"
                " is not None for path in {file_paths}])"
            )
        ).content)

    async def create_file(self, relative_path, content) -> bool:
        return relative_path in (
            await self.codebox.aupload(relative_path, content)
        ).status

    async def change_file(self, relative_path: str, changes: list) -> bool:
        return (
            await self.codebox.arun(
                f"""
                with open('{relative_path}', 'r') as f:
                    lines = f.readlines()
                    
                for line_number, action, new_code in {changes}:
                    if action == 'add':
                        lines.insert(line_number, '\\n' + new_code)
                    elif action == 'overwrite':
                        lines[line_number] = new_code + '\\n'
                    elif action == 'delete':
                        del lines[line_number]
                
                with open('{relative_path}', 'w') as f:
                    f.writelines(lines)
                    
                # format file with black
                import os
                os.system(f"black {relative_path}")
                """
            )
        ).type != "error"

    async def delete_file(self, relative_path) -> None:
        # os.remove(os.path.join(self.path, relative_path))
        pass

    async def commit_changes(self, message) -> None:
        # self.repository.create_branch("autocoder-solving-issue")
        # repo = Repo(self.path)

        # repo.git.add(A=True)
        # repo.index.commit(message)
        # origin = repo.remote(name='origin')
        # origin.push()
        pass

    def _clone_repository(self):
        # repo_path = self.PATH + self.repository.name
        # if not os.path.exists(repo_path):
        #     # Pass the access token as an environment variable for the git clone command
        #     os.environ['GIT_ASKPASS'] = f'echo {self.repository.access_token}'
        #     os.environ['GIT_TERMINAL_PROMPT'] = '0'
        #     Repo.clone_from(self.repository.repo_url, repo_path)
        # return repo_path
        pass

    def __repr__(self) -> str:
        return f"Codebase({self.repository}"
