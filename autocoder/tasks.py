import re
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from autocoder.templates import *
from database.models import Issue


def solve(issue: Issue):
    """ Solve the issue by using langchain and start a pull request """
    chatgpt = ChatOpenAI(model="gpt-4", verbose=True)
    info_dict = {
        "repo_name": issue.repository.name, 
        "repo_keywords": issue.repository.keywords, 
        "repo_description": issue.repository.description, 
        "issue_title": issue.title, 
        "issue_number": issue.issue_number,
        "issue_description": issue.body, 
        "code_tree": issue.repository.codebase.tree
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
            files_ok = issue.codebase.validate_file_paths(relevant_file_paths)
        else: 
            print("No files found try again", relevant_files_response)
            tries += 1
        if tries > 5: raise Exception("No files found")
        
    print("Relevant Files:", relevant_file_paths)
    
    relevant_files_dict = {}
    for file in relevant_file_paths:
            file_content = issue.codebase.show_file(file.strip("'"))
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
            files_ok = issue.codebase.validate_file_paths(change_file_paths)
            print("No files found try again", files_to_change)
            tries += 1
        if tries > 5: raise Exception("No files found")
    
    print("Files to change:\n", change_file_paths, "\n")
    print("New Files:\n", new_file_paths, "\n")
    
    change_files_dict = {}
    for file in change_file_paths:
        try:
            file_content = issue.codebase.show_file(file.strip("'"))
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
