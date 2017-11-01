# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import logging
import os
import subprocess
import sys
from distutils.spawn import find_executable as _fe

import click

_logger = logging.getLogger(__name__)


def _escape(s):
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace('\'', '\\\'')
    s = s.replace('&', '\\&')
    s = s.replace('|', '\\|')
    s = s.replace('>', '\\>')
    s = s.replace('<', '\\<')
    s = s.replace(' ', '\\ ')
    return s


def cmd_string(cmd):
    return " ".join([_escape(s) for s in cmd])


def log_cmd(cmd, cwd=None, level=logging.DEBUG, echo=False):
    s = cmd_string(cmd)
    if echo:
        click.echo(click.style(s, bold=True))
    _logger.log(level, '%s$ %s', cwd or '.', s)


def call(cmd, cwd=None, log_level=logging.DEBUG, echo=False):
    _adapt_executable(cmd)
    log_cmd(cmd, cwd=cwd, level=log_level, echo=echo)
    try:
        return subprocess.call(cmd, cwd=cwd)
    except subprocess.CalledProcessError:
        raise click.ClickException(cmd_string(cmd))


def check_call(cmd, cwd=None, log_level=logging.DEBUG, echo=False):
    _adapt_executable(cmd)
    log_cmd(cmd, cwd=cwd, level=log_level, echo=echo)
    try:
        return subprocess.check_call(cmd, cwd=cwd)
    except subprocess.CalledProcessError:
        raise click.ClickException(cmd_string(cmd))


def check_output(cmd, cwd=None, log_level=logging.DEBUG, echo=False):
    _adapt_executable(cmd)
    log_cmd(cmd, cwd=cwd, level=log_level, echo=echo)
    try:
        return subprocess.check_output(cmd, cwd=cwd)
    except subprocess.CalledProcessError:
        raise click.ClickException(cmd_string(cmd))


def _adapt_executable(cmd):
    cmd[0] = _find_executable(cmd[0])


def _find_executable(exe):
    python_dir = os.path.dirname(sys.executable)
    exe_path = os.path.join(python_dir, exe)
    if os.path.exists(exe_path):
        return exe_path
    exe_path = _fe(exe)
    if exe_path:
        return exe_path
    raise RuntimeError("%s executable not found" % (exe, ))
