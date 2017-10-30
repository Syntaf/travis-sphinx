# -*- coding: utf-8 -*-
import logging

import click
from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution('acsoo').version
except DistributionNotFound:
    # package is not installed
    __version__ = 'dev'

__notice__ = '''%(prog)s, version %(version)s

travis-sphinx'''


class ColoredFormatter(logging.Formatter):

    COLORS = {
        'DEBUG': dict(dim=True),
        'INFO': dict(),
        'WARNING': dict(fg='yellow'),
        'ERROR': dict(fg='red'),
        'CRITICAL': dict(fg='white', bg='red'),
    }

    def format(self, record):
        res = super(ColoredFormatter, self).format(record)
        return click.style(res, **self.COLORS[record.levelname])


@click.group()
@click.version_option(version=__version__, message=__notice__)
@click.option('-v', '--verbose', count=True)
@click.option(
    '-o', '--outdir',
    type=click.Path(dir_okay=True, file_okay=False, exists=False),
    help='Directory to put html docs, default is target',
    default='doc/build',
    show_default=True
)
@click.pass_context
def main(ctx, outdir, verbose):
    ctx.obj= dict(outdir=outdir)

    if verbose > 1:
        level = logging.DEBUG
    elif verbose > 0:
        level = logging.INFO
    else:
        level = logging.WARNING

    logger = logging.getLogger()
    channel = logging.StreamHandler()
    channel.setFormatter(ColoredFormatter())
    logger.setLevel(level)
    logger.addHandler(channel)
