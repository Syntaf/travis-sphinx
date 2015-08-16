import os
import sys
import subprocess
import getopt

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

def usage():
    print 'Usage: travis-sphinx [options] {actions}\n'
    print 'Options:\n  -h, --help\t\tProvide information on script or following action\n' + \
          '  -s, --source\t\tSource directory of sphinx docs, default is docs/source'
    print 'Actions:\n  build\t\tBuild sphinx documentation\n  deploy\t\tDeploy sphinx docs to travis branch'

def main():
    source_dir = 'docs/source'
    # Print usage if no arguments entered
    if len(sys.argv) == 1:
        print 'travis-sphinx v0.0.1'
        usage()
        exit(0)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hs:', ['help', 'source='])

    except getopt.GetoptError as err:
        print str(err) + ', see --help for valid arguments'
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        elif opt in ('s', '--source'):
            source_dir = arg

    print source_dir