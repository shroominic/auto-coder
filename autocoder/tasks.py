import re
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from autocoder.templates import *
from database.models import Issue


def solve(issue: Issue):
    """ Solve the issue by using langchain and start a pull request """
    
