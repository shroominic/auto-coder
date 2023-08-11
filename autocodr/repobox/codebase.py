from codeboxapi import CodeBox  # type: ignore
from github.Repository import Repository


class CodeBase(CodeBox):
    def __init__(self, repository: Repository, access_token=None):
        super().__init__()
        self.repository = repository
        self.access_token = access_token

    async def astart(self, repository: Repository, access_token=None):
        await super().astart()
        await self.arun(
            "import os; os.mkdir('.codebase'); os.chdir('.codebase');"   
        )
        # setup git credentials for pushing and forking
        await self.bash(
            f"git clone {repository.clone_url} .",
            f"git config --global user.email 'github@autocodr.com'",
            f"git config --global user.name 'AutoCodr'",
            f"git config --global credential.helper store"
        )
        if access_token:
            await self.bash(
                f"git config --global credential.helper '!f() {{ echo username=git; echo password={access_token}; }}; f'"
            )
        await self.bash(
            "git config --global push.default simple"
        )
    
    async def bash(self, *commands: str) -> str:
        return (
            await self.arun(
                "os.system('" + "; ".join(commands) + "')"
            )
        ).content
    
    async def read_file(self, relative_path: str) -> bytes | None:
        return (
            await self.adownload(relative_path)
        ).content
    
    async def show_tree(self) -> str | None:
        return (
            await self.arun("os.walk('.')")
        ).content

    async def show_file(self, relative_path: str) -> str | None:
        # TODO: check max string length
        return (
            await self.arun(f"open('{relative_path}').read()")
        ).content

    async def file_exists(self, relative_path) -> bool:
        # TODO: test this
        return (
            await self.arun(f"os.path.exists('{relative_path}')")
        ).content == "True"

    async def validate_file_paths(self, file_paths):
        # TODO test this
        return bool((
            await self.arun(
                f"import re; all([re.search(r'.*\\..*', path)"
                " is not None for path in {file_paths}])"
            )
        ).content)

    async def create_file(self, relative_path, content) -> bool:
        return relative_path in (
            await self.aupload(relative_path, content)
        ).status

    async def change_file(self, relative_path: str, changes: list[list[str]]) -> bool:
        return (
            await self.arun(
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
                os.system(f"black {relative_path}")
                """
            )
        ).type != "error"

    async def delete_file(self, relative_path) -> None:
        await self.bash(f"rm {relative_path}")

    async def commit_changes(self, message) -> None:
        await self.bash("git add .")
        await self.bash(f"git commit -m '{message}'")
        await self.bash("git push origin master")

    def __repr__(self) -> str:
        return f"Codebase({self.repository}"
