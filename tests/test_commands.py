# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
import os

import pytest
from click.testing import CliRunner

from travis_sphinx.main import main

DOC_DIR = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'docs',
    'source')

DOC_WITH_WARNING_DIR = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'docs',
    'source_with_warning')


@pytest.fixture
def builded_doc():
    runner = CliRunner()
    with runner.isolated_filesystem() as tmpDir:
        # the default output should be doc/build
        output_dir = os.path.join(tmpDir, 'doc', 'build')
        result = runner.invoke(main, ['build', '-s', DOC_DIR])
        assert result.exit_code == 0, result.output
        yield output_dir


@pytest.fixture
def travis_env():
    env = {'PYTEST': '1',
           'TRAVIS_BRANCH': 'master',
           'TRAVIS_PULL_REQUEST': 'false',
           'TRAVIS_REPO_SLUG': 'org/travis-sphinx',
           'GH_TOKEN': 'token'}
    return env


def test_build():
    runner = CliRunner()
    with runner.isolated_filesystem() as tmpDir:
        # the default output should be doc/build
        output_dir = os.path.join(tmpDir, 'doc', 'build')
        # before the run the directory should not exists
        assert not os.path.exists(output_dir)
        result = runner.invoke(main, ['build', '-s', DOC_DIR])
        assert result.exit_code == 0, result.output
        # after the run target dir must exists
        assert os.path.exists(output_dir)
        # and an contans at least the index.html file
        assert os.path.exists(os.path.join(output_dir, 'index.html'))


def test_buid_with_warning():
    runner = CliRunner()
    with runner.isolated_filesystem() as tmpDir:
        # sphinx will issue warnings when generating the documentations.
        # these warning are interpreted as errors.
        result = runner.invoke(main, ['build', '-s', DOC_WITH_WARNING_DIR])
        assert result.exception, result.output
        # test the disable of warnings
        result = runner.invoke(main, ['build',
                                      '-s',
                                      DOC_WITH_WARNING_DIR,
                                      '-n'])
        assert result.exit_code == 0, result.output


def test_deploy_default(builded_doc, travis_env):
    runner = CliRunner()
    result = runner.invoke(
        main, ['-o', builded_doc, 'deploy'], env=travis_env)
    assert result.exit_code == 0, result.output
    assert result.output == 'ghp-import -p -f -n -r ' \
                            'https://token@github.com/org/travis-sphinx.git ' \
                            '-m Update\ documentation %s\n' % builded_doc


def test_deploy_commit_message(builded_doc, travis_env):
    runner = CliRunner()
    result = runner.invoke(
        main, ['-o', builded_doc, 'deploy', '-m', 'commit message'],
        env=travis_env)
    assert result.exit_code == 0, result.output
    assert result.output == 'ghp-import -p -f -n -r ' \
                            'https://token@github.com/org/travis-sphinx.git ' \
                            '-m commit\ message %s\n' % builded_doc


def test_deploy_branch(builded_doc, travis_env):
    runner = CliRunner()
    result = runner.invoke(
        main, ['-o', builded_doc, 'deploy', '-b', 'mybranch'], env=travis_env)
    assert result.exit_code == 0, result.output
    assert not result.output
    travis_env['TRAVIS_BRANCH'] = 'mybranch'
    result = runner.invoke(
        main, ['-o', builded_doc, 'deploy', '-b', 'mybranch'], env=travis_env)
    assert result.exit_code == 0, result.output
    assert result.output == 'ghp-import -p -f -n -r ' \
                            'https://token@github.com/org/travis-sphinx.git ' \
                            '-m Update\ documentation %s\n' % builded_doc


def test_deploy_cname(builded_doc, travis_env):
    runner = CliRunner()
    result = runner.invoke(
        main, ['-o', builded_doc, 'deploy', '-c', 'test.org'], env=travis_env)
    assert result.exit_code == 0, result.output
    assert result.output == 'ghp-import -p -f -n -r ' \
                            'https://token@github.com/org/travis-sphinx.git ' \
                            '-c test.org '\
                            '-m Update\ documentation %s\n' % builded_doc


def test_deploy_on_pr(builded_doc, travis_env):
    # deploy is not launched on PR
    runner = CliRunner()
    travis_env['TRAVIS_PULL_REQUEST'] = 'true'
    result = runner.invoke(
        main, ['-o', builded_doc, 'deploy'], env=travis_env)
    # by default the deploy is not done if we are on a PR
    assert result.exit_code == 0, result.output
    assert result.output == ''
