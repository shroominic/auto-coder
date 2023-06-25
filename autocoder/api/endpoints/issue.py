from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi import Depends
from autocoder.database.models import Issue, User
from autocoder.api.utils.auth import authenticate_user

router = APIRouter()

class IssueCreate(BaseModel):
    """ Create an issue """
    issue_url: str
    access_token: str | None
    

@router.post("/issue/create")
async def create_issue(issue: IssueCreate, user: User = Depends(authenticate_user)):
    """ Create an issue in the database """
    try:
        Issue.from_url(
            issue_url = issue.issue_url, 
            access_token = issue.access_token or None
            )
        return JSONResponse(
            status_code=200, 
            content={"status": "ok"}
            )

    except Exception as e:
        return JSONResponse(
            status_code=400, 
            content={
                "status": "error", 
                "message": str(e)
            })

import re

from autocoder.database.models import Repository
from autocoder.langchain_shortcuts import (
    get_response,
    get_file_paths,
    get_code_response,
    extract_files,
)

@router.post("/issue/solve")
async def solve_issue(issue: IssueCreate, user: User = Depends(authenticate_user)):
    """ Solve the issue by using langchain and start a pull request """
    print(user.email)
    # return JSONResponse(
    #     status_code=200,
    #     content={"status": "ok"}
    # )
    
    issue_url = issue.issue_url
    repo_url, issue_number = issue_url.split("/issues/")

    repository = Repository(repo_url, issue.access_token or None)
    print(issue.access_token)
    issue: Issue = await repository.get_issue(issue_number)

    context = {
        "repo_name": repository.name, 
        "repo_keywords": repository.keywords, 
        "repo_description": repository.description, 
        "issue_title": issue.title, 
        "issue_number": str(issue.issue_number),
        "issue_description": issue.body, 
        "code_tree": repository.codebase.tree
    }

    coding_system_prompt = """
    You are a coding assistant solving tasks for developers.
    Tasks are represented as issues on GitHub repositories.
    Be verbose and precise in your responses.

    The following is a conversation about solving issue {issue_title} #{issue_number} on {repo_name}.
    """

    important_files_prompt = """
    Which files are important to read for gaining understanding of the codebase?

    Codebase: 
    {code_tree}

    For example in a python project you might want to look at the 'requirements.txt' file to understand which technologies are used in the project.\n
    Reply like this and make sure pathes are in 'single quotes' and not "double quotes":

    ```python
    relevant_files = [
        'path/to/file1.txt',  # do not start with ./ or /
        'path/to/file2.js',
        ...
        # max 4 files so choose wisely
    ]
    ```
    """

    relevant_file_paths = await get_file_paths(
        important_files_prompt, 
        "relevant_files",
        system_instruction=coding_system_prompt,
        validation=repository.codebase.validate_file_paths,
        **context
    )

    relevant_files_dict = {}
    for path in relevant_file_paths:
        path = path.strip("'") # TODO: remove this 
        relevant_files_dict[path] = repository.codebase.show_file(path)

    context["relevant_files"] = str(relevant_files_dict)
    relevant_files_dict

    repo_summary_prompt = """
    Summarize what this repository is about and what it does to have a better understanding and context of the codebase.
    Repository name:
    {repo_name}
    Repository description:
    {repo_description}
    Repository keywords:
    {repo_keywords}
    Repository codebase:
    {code_tree}
    Relevant files: 
    {relevant_files}

    Describe the technologies used and the structure of the codebase.
    Please be as detailed and precise as possible but keep it short.
    """

    context["repo_summary"] = await get_response(
        repo_summary_prompt, 
        system_instruction=coding_system_prompt, 
        **context
    )

    issue_summary_prompt = """
    Repository codebase:
    {code_tree}
    Repository Summary:
    {repo_summary}
    Issue title: 
    {issue_title}
    Issue description: 
    {issue_description}

    Describe step by step (abstract) how to implement the issue and what files are relevant.
    Be precise and keep it short.
    """

    get_changes_prompt = """
    Repository codebase:
    {code_tree}
    Repository description:
    {repo_summary}
    Issue description:
    {issue_summary}

    What files need to be changed to solve the issue?
    What new files need to be created?

    Write paths using 'single quotes'.
    Make sure to put only file paths that exist in the codebase/project directory in files_to_change.
    Respond with a codeblock like this:
    ```python
    new_files = [
        'path/to/new_file1.py', # do not start with ./ or /
        'path/to/new_file2.ipynb',
        ...
    ]

    files_to_change = [
        'path/to/file1.txt',  # do not start with ./ or /
        'path/to/file2.js',
        ...
    ]
    ```
    """

    async def get_files(retry=3):
        try:
            context["issue_summary"] = await get_response(
                issue_summary_prompt,
                system_instruction=coding_system_prompt,
                verbose=True,
                **context
            )
            
            files_to_change = await get_response(
                get_changes_prompt,
                system_instruction=coding_system_prompt,
                verbose=True,
                **context
            )

            new_files = extract_files(files_to_change, "new_files")
            files_to_change = extract_files(files_to_change, "files_to_change")

            print("New files:", new_files)
            print("Files to change:", files_to_change)
            if not repository.codebase.validate_file_paths(files_to_change):
                raise ValueError("Some files to change do not exist in the codebase.")

            if any(repository.codebase.file_exists(f) for f in new_files): 
                raise ValueError("Some new files already exist in the codebase.")

            return new_files, files_to_change
        
        except Exception as e:
            if retry > 0:
                print("Retrying...", e)
                return await get_files(retry=retry-1)
            else: raise e


    new_files, files_to_change = await get_files()

    print("New files:", new_files)
    print("Files to change:", files_to_change)

    new_file_prompt = """
    Repository description:
    {repo_summary}

    Issue description:
    {issue_summary}

    Implement this file {file_path} to solve the issue.
    After completion this the file will be created and added to the codebase.
    Reply with a codeblock containing the content of the new file.
    """

    new_files_dict = {}
    for path in new_files:
        context["file_path"] = path
        
        new_file_content = await get_code_response(
            new_file_prompt,
            system_instruction=coding_system_prompt,
            **context
        )
        
        new_files_dict[path] = new_file_content



    change_file = """
    Repository description:
    {repo_summary}
    Issue description:
    {issue_summary}
    First write a detailed instruction on how to change the file {file_path}.

    # [Begin file content]
    {file_content}
    # [Eind file content]

    """
    """

    Then create a list called "changes".
    This list should contain tuples of the form (line_number, action, "new code").
    Action can be one of the following:
    - add: insert a new line of code at the line with the given number and shift all following lines down
    - overwrite: overwrite the line with the given number
    - delete: delete the line with the given number

    Write down all changes and 
    reply with a codeblock like this:
    ```python
    # (line_number, 'action', 'new code')
    # make sure use 'single quotes' and not "double quotes" or `backticks` like in this example:
    changes = [
        (0, 'add', 'import newexample'),
        (4, 'overwrite', 'def foo():'),
        (5, 'add', '    print("hello world")'),
        (6, 'delete', '    print("bar")'),
        ...
    ]
    ```
    """

    change_files_dict = {}
    for path in files_to_change:
        context["file_path"] = path
        context["file_content"] = repository.codebase.show_file(path)
        
        changes_content = await get_code_response(
            change_file,
            system_instruction=coding_system_prompt,
            **context
        )
        
        tuple_pattern = re.compile(r"\((\d+),\s*\'(.*?)\',\s*\'(.*?)\'\)", re.DOTALL)
        tuples = tuple_pattern.findall(changes_content)
        
        change_files_dict[path] = [
            (int(line), action, change) 
            for line, action, change in tuples
        ]

    for file, content in new_files_dict.items():
        repository.codebase.create_file(file, content)
        print("Created:", file, "\nwith content:", content, "\n")
        
    for file, changes in change_files_dict.items():
        repository.codebase.change_file(file, changes)
        print("Changed:", file, "\nwith changes:", changes, "\n")

    repository.codebase.commit_changes("Solved issue using GPT-4")