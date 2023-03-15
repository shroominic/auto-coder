import argparse

from autocoder.models import Issue
    

# Set up argument parser
parser = argparse.ArgumentParser(description='Process a GitHub issue link')
parser.add_argument('issue', help='Link to the GitHub issue')

# Parse the command line arguments
args = parser.parse_args()

issue: Issue = args.issue

print(f'Processing GitHub issue: {issue}')

issue.solve()
