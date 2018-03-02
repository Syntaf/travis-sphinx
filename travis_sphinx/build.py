# -*- coding: utf-8 -*-
import logging

import click
try:
    # Sphinx 1.7+
    from sphinx.cmd.build import build_main
    sphinx_version_at_least_1_7 = True
except AttributeError:
    from sphinx import build_main
    sphinx_version_at_least_1_7 = False

from .main import main

_logger = logging.getLogger(__name__)


@click.command(
    help="Build sphinx documentation."
)
@click.option(
    '-s', '--source',
    type=click.Path(dir_okay=True, file_okay=False, exists=True),
    help='Source directory of sphinx docs',
    default='docs/source',
    show_default=True
)
@click.option(
    '-n', '--nowarn',
    type=click.BOOL,
    is_flag=True,
    help='Do not error on warnings',
)
@click.pass_context
def build(ctx, source, nowarn):
    """
    Build documentation from ``source``, placing built files in
    ``target``.
    """
    _logger.info('building documentation')
    outdir = ctx.obj['outdir']

    if sphinx_version_at_least_1_7:
        # args have to be specified this way for 1.7+, otherwise one gets
        # "Builder name  html not registered or available through entry point"
        # See https://github.com/sphinx-doc/sphinx/issues/4623
        args = ['-b', 'html']
    else:
        args = ['-b html']

    if not nowarn:
        args.append('-W')
    if build_main(args + [source, outdir]):
        raise click.ClickException("Error building sphinx doc")


main.add_command(build)
