#!/usr/bin/python
from github import Github
from getpass import getpass
from git import Repo
import os
import sys


g = None # github api object

# read accesstoken if exists
# - you can create at 'github - settings - developer settings - personal access tokens'
accesstoken = None

try:
    with open('github-accesstoken') as token_file:
        accesstoken = token_file.read()
        print('accesstoken file found! ' + accesstoken)
        g = Github(accesstoken)
except FileNotFoundError:
    print('github-accesstoken file not found!')

if accesstoken is None:
    print('<welcome github!>')
    username = input('input username: ')
    password = getpass('input password: ')
    print()
    g = Github(username, password)

if accesstoken:
    print('login succeed!')

user = g.get_user()
repos = user.get_repos(type="private")

base_dir = os.path.expanduser('~/Documents/GitHub/')

if not os.path.exists(base_dir):
    print('cannot find github local repos base dir. so exit.')
    print('> base dir: ' + base_dir)
    print('- do you use no-windows os?')
    print('- do you install github client?')
    sys.exit()

# if not os.path.exists(base_dir):
    # os.makedirs(base_dir)

print('<repositories sorted by name>')
sorted_repos = sorted(repos, key=lambda repo: repo.name)
for repo in sorted_repos:
    https_url = f'https://github.com/wminos/{repo.name}.git'
    print(f'>> {repo.name}: {https_url}')

    target_dir = os.path.join(base_dir, repo.name)
    print('> target dir: ' + target_dir)
    if os.path.exists(target_dir):
        print('already folder exist so pass')
    else:
        print("not found folder, so let's clone")
        Repo.clone_from(https_url, target_dir)
