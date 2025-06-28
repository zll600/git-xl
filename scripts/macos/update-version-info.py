import os
import json
import re

# read build number, repo tag name and git commit hash from env vars 
build = os.getenv('GITHUB_RUN_ATTEMPT', '0')
if os.getenv('GITHUB_REF_TYPE') == 'tag':
  version = os.environ['GITHUB_REF_NAME']
else:
  version = '0.0.0'
commit = os.environ['GITHUB_SHA'][:7] if os.getenv('GITHUB_SHA') else 'dev'

print('-----------')
print('Version tag: %s' % version)
print('Build number: %s' % build)
print('Commit hash: %s' % commit)

major, minor, patch = version.split('.')
print(f'Version: {major}.{minor}.{patch}.{build}')
print('-----------')

# update src/cli.py (VERSION and COMMIT)
path = 'src/cli.py'
with open(path, 'r') as f:
    s = f.read()

s = re.sub(r"VERSION\s*=\s*('|\")\d+\.\d+\.\d+('|\")", f"VERSION = '{major}.{minor}.{patch}'", s, re.MULTILINE)
s = re.sub(r"GIT_COMMIT\s*=\s*('|\")[a-zA-Z0-9]*('|\")", f"GIT_COMMIT = '{commit}'", s, re.MULTILINE)

with open(path, 'w') as f:
    f.write(s)

print(f'Updated src/cli.py with version {major}.{minor}.{patch} and commit {commit}') 