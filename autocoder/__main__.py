import argparse
from autocoder.models import Repository
    

# Set up argument parser
parser = argparse.ArgumentParser(description='Process a GitHub issue link')
parser.add_argument('issue', help='Link to the GitHub issue')

# Parse the command line arguments
issue_url = parser.parse_args().issue
repo_url, issue_number = issue_url.split("/issues/")

repo = Repository(repo_url)
issue = repo.get_issue(issue_number)

issue.solve()
