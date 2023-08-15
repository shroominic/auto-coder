import re

from autocodr.chain.shortcuts import get_code_response, get_file_paths, get_multiple_file_paths, get_response
from autocodr.chain.templates import (
    change_file,
    coding_system_prompt,
    important_files,
    issue_summary,
    new_file,
    prepare_changes,
    repo_summary,
)

# from autocodr.schemas import TaskResult
from autocodr.database import models
from autocodr.repobox import CodeBase


async def solve_issue(
    task: models.Task,
):  # -> TaskResult:
    """Solve the issue by using langchain and start a pull request"""
    repository, issue = task.get_repo_and_issue()
    codebase = await CodeBase.from_repo(repository)

    context = {
        "repo_name": repository.name,
        "repo_keywords": repository.get_topics(),
        "repo_description": repository.description,
        "issue_title": issue.title,
        "issue_number": str(task.issue_number),
        "issue_description": issue.body,
        "code_tree": repository.get_git_tree(sha=repository.default_branch),
    }

    relevant_file_paths = await get_file_paths(
        important_files,
        "relevant_files",
        # validation=repository.codebase.validate_file_paths,
        **context
    )

    relevant_files_dict: dict[str, str] = {}

    context["relevant_files"] = str(
        relevant_files_dict.update([(path, await codebase.show_file(path) or "") for path in relevant_file_paths])
        or relevant_files_dict
    )

    context["repo_summary"] = await get_response(repo_summary, system=coding_system_prompt, **context)

    async def get_files(retry=3):
        try:
            context["issue_summary"] = await get_response(issue_summary, system=coding_system_prompt, **context)

            file_modifications = await get_multiple_file_paths(prepare_changes, **context)

            new_files = file_modifications["new_files"]
            files_to_change = file_modifications["change_files"]

            print("New files:", new_files)
            print("Files to change:", files_to_change)
            if not await codebase.validate_file_paths(files_to_change):
                raise ValueError("Some files to change do not exist in the codebase.")

            if any([await codebase.file_exists(f) for f in new_files]):
                raise ValueError("Some new files already exist in the codebase.")

            return new_files, files_to_change

        except Exception as e:
            if retry > 0:
                print("Retrying...", e)
                return await get_files(retry=retry - 1)
            else:
                raise e

    new_files, files_to_change = await get_files()

    print("New files:", new_files)
    print("Files to change:", files_to_change)

    new_files_dict = {}
    for path in new_files:
        context["file_path"] = path

        new_file_content = await get_code_response(new_file, **context)

        new_files_dict[path] = new_file_content

    change_files_dict = {}
    for path in files_to_change:
        context["file_path"] = path
        context["file_content"] = await codebase.show_file(path)

        changes_content = await get_code_response(change_file, system_instruction=coding_system_prompt, **context)

        tuple_pattern = re.compile(r"\((\d+),\s*\'(.*?)\',\s*\'(.*?)\'\)", re.DOTALL)
        tuples = tuple_pattern.findall(changes_content)

        change_files_dict[path] = [(int(line), action, change) for line, action, change in tuples]

    for file, content in new_files_dict.items():
        await codebase.create_file(file, content)
        print("Created:", file, "\nwith content:", content, "\n")

    for file, changes in change_files_dict.items():
        await codebase.change_file(file, changes)
        print("Changed:", file, "\nwith changes:", changes, "\n")

    await codebase.commit_changes("Solved issue using GPT-4")
