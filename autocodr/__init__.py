"""
AUTO CODER - A tool to take the job of all programmers
Solves your issues by creating pull requests for you

final version will be a website or a cli tool
input: github repo url and issue number

bot is cloning the repo and create a class with it that conbains
files and issues
at least a single test case needs to exist in the repo to continues
maybe just running the program and doing a healthcheck is enough
if the test case is not passed, the bot will not continue and try again
code is generating by running a lot of prompt engeneering over the codebase
this includes:
- finding the location where to put the code
- writing instructions for itself
- commenting the code to improve understanding
- iterating over the codebase to write a summary into memory
- using the 4096 tokens as stack to put information and not only use it to store previous messages
"""
