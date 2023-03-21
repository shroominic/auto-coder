from os import getenv
from dotenv import load_dotenv
from argparse import ArgumentParser
from models import Repository


def main():
    parser = ArgumentParser(description='Process a GitHub issue link')
    parser.add_argument('issue', help='Link to the GitHub issue')

    # parse cli args
    issue_url = parser.parse_args().issue
    repo_url, issue_number = issue_url.split("/issues/")

    repo = Repository(repo_url, getenv("GITHUB_TOKEN"))
    issue = repo.get_issue(issue_number)

    issue.solve()


if __name__ == '__main__':
    load_dotenv()
    main()