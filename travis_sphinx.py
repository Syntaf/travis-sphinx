import os
import sys
import subprocess

def run(*args):
    ret = subprocess.call(args, stdout=sys.stdout, stderr=sys.stderr)
    if ret != 0:
        exit(ret)

def build():
    pass

def deploy():
    branch = os.environ['TRAVIS_BRANCH']
    pr = os.environ['TRAVIS_PULL_REQUEST']
    token = os.environ['GH_TOKEN']
    repo = os.environ['TRAVIS_REPO_SLUG']

    if branch == 'master' and pr == 'false':
        print 'uploading docs...'
        sys.stdout.flush()
        run('git', 'clone', 'https://github.com/davisp/ghp-import')
        run('./ghp-import/ghp-import', '-n', 'target/doc/build')
        run('git', 'push', '-fq', 'https://%s@github.com/%s.git'
            % (token, repo), 'gh-pages)')

def main():
    print 'hi'