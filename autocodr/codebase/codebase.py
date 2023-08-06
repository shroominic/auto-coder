from codeboxapi import CodeBox  # type: ignore


class CodeBase(CodeBox):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repository = None
        self.path = self._clone_repository()
        self.ignore = [".git"]
        
    def show_tree(self):
        # tree = []
        # for folder, _, files in os.walk(self.path):
        #     if all([ignore not in folder for ignore in self.ignore]):
        #         folder_relative = os.path.relpath(folder, self.path)
        #         for file in files:
        #             tree.append(os.path.join(folder_relative, file))
        # return "\n".join(tree)
        pass
    
    def show_file(self, relative_path):
        # with open(os.path.join(self.path, relative_path), "r") as f:
        #     return f.read()
        pass
        
    def file_exists(self, relative_path):
        # print(os.path.join(self.path, relative_path))
        # try:
        #     return os.path.exists(os.path.join(self.path, relative_path))
        # except Exception as e:
        #     print(e)
        #     return False
        pass
    
    def validate_file_paths(self, file_paths):
        # return all([
        #         re.search(r".*\..*", path) is not None
        #         for path in file_paths
        #     ]) and all([
        #         self.file_exists(path.strip("'"))
        #         for path in file_paths
        #     ])
        pass
            
    def create_file(self, relative_path, content) -> None:
        # file_path = os.path.join(self.path, relative_path)
        # with open(file_path, "w") as f:
        #     f.write(content)
        
        # # format file with black
        # os.system(f"black {file_path}")     
        pass
            
            
    def change_file(self, relative_path: str, changes: list) -> None:
        """ Apply changes to file 
        example_changes = [
            # (line_number, action, "new code")
            (0, 'add', "import example"),
            (4, 'overwrite', "def foo():"),
            ...
        ]
        """
        # file_path = os.path.join(self.path, relative_path)
        # with open(file_path, 'r') as f:
        #     lines = f.readlines()

        # for line_number, action, new_code in changes:
        #     if action == 'add':
        #         lines.insert(line_number, '\n' + new_code)
        #     elif action == 'overwrite':
        #         lines[line_number] = new_code + '\n'
        #     elif action == 'delete':
        #         del lines[line_number]

        # with open(file_path, 'w') as f:
        #     f.writelines(lines)
        
        # # format file with black
        # os.system(f"black {file_path}")
        pass
    
    def delete_file(self, relative_path) -> None:
        # os.remove(os.path.join(self.path, relative_path))
        pass
        
    def commit_changes(self, message) -> None:
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
