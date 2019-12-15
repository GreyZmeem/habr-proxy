#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from typing import Final

from aiohttp import web
from app.application import AppConfig, create_app
from app.proxy import const

_host: Final[str] = "0.0.0.0"
_port: Final[int] = 8080


def get_parser() -> ArgumentParser:
    """Build argument parser."""
    parser = ArgumentParser(description="iVelum proxy")
    parser.add_argument(
        "-l",
        "--len",
        nargs="?",
        type=int,
        const=const.word_length,
        default=const.word_length,
        help="Word length",
        dest="word_length",
    )
    parser.add_argument(
        "-t",
        "--text",
        nargs="?",
        type=str,
        const=const.word_append,
        default=const.word_append,
        help="Text appended to words",
        dest="word_append",
    )
    parser.add_argument(
        "-u",
        "--up",
        "--upstream",
        nargs="?",
        type=str,
        const=const.upstream,
        default=const.upstream,
        help="Upstream URL (e.g. 'https://example.com')",
        dest="upstream",
    )
    parser.add_argument(
        "--host",
        nargs="?",
        type=str,
        const=_host,
        default=_host,
        help="HTTP server listen address",
        dest="host",
    )
    parser.add_argument(
        "--port",
        nargs="?",
        type=int,
        const=_port,
        default=_port,
        help="HTTP server listen port",
        dest="port",
    )
    return parser


def run():
    """Run main application server."""
    parser = get_parser()
    args = parser.parse_args()

    app_config = AppConfig(
        upstream=args.upstream,
        length=args.word_length,
        append=args.word_append,
    )
    app = create_app(app_config)
    web.run_app(app, host=args.host, port=args.port)


if __name__ == "__main__":
    run()  # type: ignore
