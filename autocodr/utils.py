from aiohttp import ClientSession
from autocodr.database import models

def raiser(exception: Exception):
    raise exception


async def fetch_issue_info(
    self,
    issue: models.Issue,
    repository: models.Repository
) -> IssueInfo:
    issue_api_url = (
        "https://api.github.com/repos"
        f"/{repository.owner}/{repository.name}"
        f"/issues/{issue.number}"
    )
    
    headers = {}
    if repository.access_token:
        headers["Authorization"] = f"Bearer {repository.access_token}"
    
    async with ClientSession() as session:
        async with session.get(issue_api_url, headers=headers) as response:
            return await response.json()
        
def create_branch(self, branch_name):
    repo = Repo(self.codebase.path)

    try:
        repo.git.checkout("-b", branch_name)
        repo.git.push("--set-upstream", "origin", branch_name)
    except GitCommandError as e:
        if "branch named" in str(e) and "already exists" in str(e):
            print(f"A branch named '{branch_name}' already exists. Switching to the existing branch.")
            repo.git.checkout(branch_name)
        else:
            raise e

def _extract_repo_info(self):
    parts = self.repo_url.split("/")
    owner = parts[3]
    repo = parts[4]
    return owner, repo

def _fetch_repo_info(self):
    repo_api_url = f"https://api.github.com/repos/{self.owner}/{self.repo}"
    headers = {}
    if self.access_token:  # Add the access token to the headers if provided
        headers["Authorization"] = f"Bearer {self.access_token}"
    repo_response = get_request(repo_api_url, headers=headers)  # Pass headers to the request
    return repo_response.json()


if __name__ == "__main__":
    issue_api_url = (
        "https://api.github.com/repos"
        f"/shroominic/codebox-api"
        f"/issues/3"
    )
    import requests  # type: ignore
    response = requests.get(issue_api_url)
    print(response.json())
    # async with ClientSession() as session:
    #     async with session.get(issue_api_url) as response:
    #         return await response.json()
