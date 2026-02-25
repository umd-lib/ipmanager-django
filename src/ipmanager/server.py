#!/usr/bin/env python
"""Server startup script."""

import click
from waitress import serve

from ipmanager.wsgi import application


@click.command()
@click.option(
    '--listen',
    default='0.0.0.0:3001',
    help='Address and port to listen on. Default is "0.0.0.0:3001".',
    metavar='[ADDRESS]:PORT',
)
def run(listen: str):
    serve(application, listen=listen, threads=8)
