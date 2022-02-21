import argparse
import logging

__version__ = "1"
__author__ = "Patrick Beagan"
__copyright__ = "Patrick Beagan"
__license__ = "MIT"

import sys

from src.imdbscraper.runtime import Runtime

_logger = logging.getLogger(__name__)


def parse_args(args):
    parser = argparse.ArgumentParser(description="Just a Fibonacci demonstration")
    parser.add_argument(
        "--version",
        action="version",
        version="imdbscraper {ver}".format(ver=__version__),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


if __name__ == "__main__":
    args = sys.argv[1:]
    args = parse_args(args)
    Runtime(_logger).run(args)
