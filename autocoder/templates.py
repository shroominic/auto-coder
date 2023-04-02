from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate


coding_system_prompt = SystemMessagePromptTemplate.from_template(
    template=
        "You are a coding assistant solving tasks for developers."
        "Tasks are represented as issues on GitHub repositories."
        "Be verbose and precise in your responses.\n"
        "The following is a conversation about solving issue {issue_title} #{issue_number} on {repo_name}.\n"
    )

important_files = HumanMessagePromptTemplate.from_template(template=
"""
Which files are important to read for gaining understanding of the codebase?\n
Codebase: \n{code_tree}\n
For example in a python project you might want to look at the 'requirements.txt' file to understand which technologies are used in the project.\n
# Reply like this and make sure pathes are in 'single quotes' and not "double quotes":
relevant_files = [
    'path/to/file1.txt',  # do not start with ./ or /
    'path/to/file2.js',
    ...
    # max 4 files so choose wisely
]
""")

repo_summary = HumanMessagePromptTemplate.from_template(
    template=
        "Summarize what this repository is about and what it does.\n"
        "Repository name: {repo_name}\n"
        "Repository description: {repo_description}\n"
        "Repository keywords: {repo_keywords}\n"
        "Repository codebase: \n{code_tree}\n"
        "Relevant files: \n{relevant_files}\n"
        "Describe the technologies used and the structure of the codebase. "
        "Please be as detailed and precise as possible but keep it short.\n"
    )

issue_summary = HumanMessagePromptTemplate.from_template(
    template=
        "Repository Summary: \n{repo_summary}\n"
        "Issue title: {issue_title}\n"
        "Issue description: {issue_description}\n"
        "Describe step by step (abstract) how to implement the issue and what files are relevant. "
        "Be precise and keep it short.\n"
    )

what_files_to_change = HumanMessagePromptTemplate.from_template(
    template=
    "Repository description: {repo_summary}\n"
    "Issue description: {issue_summary}\n"
    "What files need to be changed to solve the issue?\n"
    "Reply like this and make sure pathes are in 'single quotes' and not \"double quotes\":\n"
    "files_to_change = [\n"
    "    'path/to/file1.txt',  # do not start with ./ or /\n"
    "    'path/to/file2.js',\n"
    "    ...\n"
    "]\n"
)

prepare_changes = HumanMessagePromptTemplate.from_template(
    template=
    "Repository description: {repo_summary}\n"
    "Issue description: {issue_summary}\n"
    "What files need to be changed to solve the issue?\n"
    "What new files need to be created?\n"
    "Reply like this:\n"
    "files_to_change = [\n"
    "    'path/to/file1.txt',  # do not start with ./ or /\n"
    "    'path/to/file2.js',\n"
    "    ...\n"
    "]\n"
    "new_files = [\n"
    "    'path/to/new_file1.py',\n"
    "    ...\n"
    "]\n"
    "# write paths using 'single quotes'\n"
)

change_file = HumanMessagePromptTemplate.from_template(
    template=
    "Repository description: {repo_summary}\n"
    "Issue description: {issue_summary}\n"
    "What changes need to be made to this file {file_path} to solve the issue?\n"
    "File content: \n{file_content}\n"
    "Reply with a codeblock of the new file content.\n"
)

change_file2 = HumanMessagePromptTemplate.from_template(
    template=
"""
Repository description:
{repo_summary}
Issue description:
{issue_summary}
First write a detailed instruction on how to change the file {file_path}.
File content:
{file_content}
"""
"""
Then create a list called "changes",
write down all changes as a dictionary and 
reply with a codeblock like this:
```python
changes = [
    # (line_number, "old code", "new code")
    (1, "import example", "import newexample"),
    (4, "class foo", "class bar"),
    ...
]
```
"""
)
    


get_important_files = ChatPromptTemplate.from_messages([coding_system_prompt, important_files])
get_repo_summary = ChatPromptTemplate.from_messages([coding_system_prompt, repo_summary])
get_issue_summary = ChatPromptTemplate.from_messages([coding_system_prompt, issue_summary])
get_files_to_change = ChatPromptTemplate.from_messages([coding_system_prompt, prepare_changes])