# -*- coding: utf-8 -*-
import logging
import os

import click

from .main import main
from .tools import check_call
from .tools import log_cmd

_logger = logging.getLogger(__name__)


@click.command(
    help="Deploy sphinx docs to gh_pages branch by pulling from output dir."
)
@click.option(
    '-b', '--branches',
    help='Comma separated list of branches to build on',
    default='master',
    show_default=True
)
@click.option(
    '-c', '--cname',
    help='Write a CNAME file with the given CNAME.'
)
@click.option(
    '-m', '--message',
    default='Update documentation',
    help='The commit message to use on the target branch.',
    show_default=True
)
@click.pass_context
def deploy(ctx, branches, cname, message):
    """
    Deploy built docs to gh-pages, uses ``GH_TOKEN`` for pushing built
    documentation files located in *target/doc* to gh

    If the environment variable ``GH_REPO_SLUG`` is set, the docs will be
    deployed to the specified github repository. Otherwise, the environment
    variable of the travis build will be used (``TRAVIS_REPO_SLUG``).

    """
    branch = os.environ.get('TRAVIS_BRANCH', '')
    pr = os.environ.get('TRAVIS_PULL_REQUEST', '')
    token = os.environ.get('GH_TOKEN', '')
    repo = os.environ.get('GH_REPO_SLUG')
    if repo is None:
        repo = os.environ.get('TRAVIS_REPO_SLUG', '')
    tag = os.environ.get('TRAVIS_TAG', '')
    is_pytest_mode = 'PYTEST' in os.environ
    outdir = ctx.obj['outdir']
    if token is None:
        click.ClickException("ERROR: GH_TOKEN is missing!")

    branches = branches.split(',')
    if (branch in branches and (pr == 'false')) or tag:
        remote = 'https://%s@github.com/%s.git' % (token, repo)
        call = ['ghp-import', '-p', '-f', '-n', '-r', remote]
        if cname:
            call.extend(['-c', cname])
        if message:
            call.extend(['-m', message])
        call.append(outdir)
        _logger.info('uploading docs...')
        if is_pytest_mode:
            log_cmd(call, echo=True)
        else:
            check_call(call)
        _logger.info('success!')
    else:
        _logger.info("Deploy triggered for non-master branch '%s': skipping "
                     "deploy", branch)


main.add_command(deploy)
