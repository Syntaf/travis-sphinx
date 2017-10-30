# -*- coding: utf-8 -*-
import logging

import click
import sphinx

from .main import main

_logger = logging.getLogger(__name__)


@click.command(
    help="Build sphinx documentation."
)
@click.option(
    '-s', '--source',
    type=click.Path(dir_okay=True, file_okay=False, exists=True),
    help='Source directory of sphinx docs',
    default='doc/source',
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
    args = ['-b html']
    if not nowarn:
        args.append('-W')
    if sphinx.build_main(args + [source, outdir]):
        click.ClickException("Error building sphinx doc")


main.add_command(build)
