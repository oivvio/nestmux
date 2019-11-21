# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
[options.entry_points] section in setup.cfg:

    console_scripts =
         fibonacci = nestmux.skeleton:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""

import argparse
import sys
import logging

from nestmux import __version__

__author__ = "Oivvio Polite"
__copyright__ = "Oivvio Polite"
__license__ = "mit"


def fib(n):
    """Fibonacci example function

    Args:
      n (int): integer

    Returns:
      int: n-th Fibonacci number
    """
    assert n > 0
    a, b = 1, 1
    for i in range(n - 1):
        a, b = b, a + b
    return a


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Generate scripts to run nested tmux")

    # parser.add_argument(
    #     "--version", action="version", version="nestmux {ver}".format(ver=__version__)
    # )

    # parser.add_argument(
    #     "-v",
    #     "--verbose",
    #     dest="loglevel",
    #     help="set loglevel to INFO",
    #     action="store_const",
    #     const=logging.INFO,
    # )

    # parser.add_argument(
    #     "-vv",
    #     "--very-verbose",
    #     dest="loglevel",
    #     help="set loglevel to DEBUG",
    #     action="store_const",
    #     const=logging.DEBUG,
    # )

    return parser.parse_args(args)


# def setup_logging(loglevel):
#     """Setup basic logging

#     Args:
#       loglevel (int): minimum loglevel for emitting messages
#     """
#     logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
#     logging.basicConfig(
#         level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
#     )


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    # setup_logging(args.loglevel)
    # _logger.debug("Starting crazy calculations...")
    # print("The {}-th Fibonacci number is {}".format(args.n, fib(args.n)))
    print("hello")
    # _logger.info("Script ends here")


def run():
    """
    Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
