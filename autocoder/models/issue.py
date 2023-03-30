import re
import requests
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from .codebase import Codebase
from .templates import *


class Issue:
    """ Represents an issue on a git repository """
    def __init__(self, repository, issue_number: int):
        self.repository = repository
        self.issue_number = issue_number
        self.issue_info = self._fetch_issue_info()
        self.branch_name = self._create_branch()
    
    def solve(self):
        """ Solve the issue by using langchain and start a pull request """
        chatgpt = ChatOpenAI(model="gpt-4", verbose=True)
        info_dict = {
            "repo_name": self.repository.name, 
            "repo_keywords": self.repository.keywords, 
            "repo_description": self.repository.description, 
            "issue_title": self.title, 
            "issue_number": self.issue_number,
            "issue_description": self.body, 
            "code_tree": self.repository.codebase.tree
            }
        
        print("Starting issue solving process")
        
        files_chain = LLMChain(llm=chatgpt, prompt=get_important_files, verbose=True)
        files_ok = False
        tries = 0
        while not files_ok:
            relevant_files_response = files_chain.run(info_dict)
            if relevant_files_response:
                print(relevant_files_response)
                relevant_file_paths = re.findall(r"'.*?'", relevant_files_response)
                files_ok = self.codebase.validate_file_paths(relevant_file_paths)
            else: 
                print("No files found try again", relevant_files_response)
                tries += 1
            if tries > 5: raise Exception("No files found")
            
        print("Relevant Files:", relevant_file_paths)
        
        relevant_files_dict = {}
        for file in relevant_file_paths:
                file_content = self.codebase.show_file(file.strip("'"))
                relevant_files_dict[file] = file_content
        
        info_dict["relevant_files"] = str(relevant_files_dict)
        
        print("Generate repo summary:")
        repo_chain = LLMChain(llm=chatgpt, prompt=get_repo_summary, verbose=True)    
        info_dict["repo_summary"] = repo_chain.run(info_dict)
        
        print("Generate issue summary:")
        issue_chain = LLMChain(llm=chatgpt, prompt=get_issue_summary, verbose=True)
        info_dict["issue_summary"] = issue_chain.run(info_dict)
        
        what_files_to_change = LLMChain(llm=chatgpt, prompt=get_files_to_change, verbose=True)
        files_ok = False
        tries = 0
        while not files_ok:
            changes = what_files_to_change.run(info_dict)
            files_to_change = re.match(r"files_to_change = \[(.*?)\]", changes)
            new_files = re.match(r"new_files = \[(.*?)\]", changes)
            print(files_to_change)
            print(new_files)
            if new_files:
                new_file_paths = re.findall(r"'.*?'", new_files.group(1))
                change_file_paths = re.findall(r"'.*?'", files_to_change.group(1))
            elif files_to_change:
                change_file_paths = re.findall(r"'.*?'", files_to_change.group(1))
                files_ok = self.codebase.validate_file_paths(change_file_paths)
                print("No files found try again", files_to_change)
                tries += 1
            if tries > 5: raise Exception("No files found")
        
        print("Files to change:\n", change_file_paths, "\n")
        print("New Files:\n", new_file_paths, "\n")
        
        change_files_dict = {}
        for file in change_file_paths:
            try:
                file_content = self.codebase.show_file(file.strip("'"))
                info_dict["file_content"] = file_content
                new_file_content = LLMChain(llm=chatgpt, prompt=change_file, verbose=True).run(info_dict)
                print(new_file_content)
                new_file_content2 = LLMChain(llm=chatgpt, prompt=change_file2, verbose=True).run(info_dict)
                print(new_file_content2)
                change_files_dict[file] = new_file_content
            except FileNotFoundError:
                print(f"File {file} not found")
        for file, content in change_files_dict.items():
            print(file)
            print(content)
        
        # TODO: test the code and repeat until it works
        
        # TODO: create a pull request

    def _fetch_issue_info(self):
        issue_api_url = f"https://api.github.com/repos/{self.repository.owner}/{self.repository.repo}/issues/{self.issue_number}"
        headers = {}
        if self.repository.access_token:  # Add the access token to the headers if provided
            headers["Authorization"] = f"Bearer {self.repository.access_token}"
        issue_response = requests.get(issue_api_url, headers=headers)  # Pass headers to the request
        return issue_response.json()

    def _create_branch(self):
        """ Create a branch for the issue """
        branch_name = f"issue-{self.issue_number}"
        self.repository.create_branch(branch_name)
        return branch_name
    
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

    @property
    def codebase(self) -> Codebase:
        return self.repository.codebase
    
    def __repr__(self) -> str:
        return f"Issue({self.repository}, {self.issue_number})"
    
    def __str__(self) -> str:
        return f"{self.repository} - {self.title}"