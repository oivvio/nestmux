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
import os
import argparse
import sys
import logging
import pathlib
import yaml
from string import Template
from pathlib import Path, PurePath

from nestmux import __version__

__author__ = "Oivvio Polite"
__copyright__ = "Oivvio Polite"
__license__ = "mit"


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Generate scripts to run nested tmux")

    return parser.parse_args(args)


def get_config():
    # Get the configfilename
    configfn = PurePath(Path.home(), ".nestmux", "config.yml")

    if not Path(configfn).exists():
        print(f"Please create a config file in {configfn}")
        exit()

    with open(configfn) as configfile:
        config = yaml.load(configfile, Loader=yaml.FullLoader)

    return config


def write_bashscript(config):
    print(config)
    parentfolder = Path(__file__).parent

    templatefn = Path(parentfolder, "templates", "bashtemplate.sh")
    template = Template(open(templatefn).read())
    context = {"configpath": os.path.expanduser(config["configpath"])}
    output = template.substitute(context)

    path = Path(config["path"], "nestmux")

    path.open("w").write(output)
    path.chmod(0o755)


def write_configfiles(config):
    for level in range(1, config["levels"] + 1):
        write_configfile(config, level)


def write_configfile(config, level):
    base_config = ""

    # Get the system base config
    if not ("skip_system_config" in config and config["skip_system_config"] == True):
        try:
            global_tmux_config = open("/etc/tmux.conf").read()
            base_config += global_tmux_config
            base_config += "\n"

        except BaseException as e:
            pass

    # Get the user config
    if not ("skip_user_config" in config and config["skip_user_config"] == True):
        try:
            user_tmux_config = open(os.path.expanduser("~/.tmux.conf")).read()
            base_config += user_tmux_config
            base_config += "\n"

        except BaseException as e:
            pass

    # Get any existing level specific config
    if not ("skip_level_config" in config and config["skip_level_config"] == True):
        try:
            level_tmux_config = open(
                os.path.expanduser(f"~/.nestmux/extraconfig_level{level}")
            ).read()
            base_config += level_tmux_config
            base_config += "\n"

        except BaseException as e:
            print(e)

    # Read the standard
    template = Template(("unbind C-b\n" "set -g prefix C-$escape_key\n"))
    index = level - 1
    context = {"escape_key": config["escape_keys"][index]}
    output = template.substitute(context)

    path = Path(os.path.expanduser(config["configpath"]), f"nestmuxconfig_level{level}")

    with (path.open("w")) as fh:
        if base_config:
            fh.write(base_config)
            fh.write("\n")
        fh.write(output)


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    # setup_logging(args.loglevel)
    # _logger.debug("Starting crazy calculations...")
    # print("The {}-th Fibonacci number is {}".format(args.n, fib(args.n)))

    # _logger.info("Script ends here")
    config = get_config()
    write_bashscript(config)
    write_configfiles(config)


def run():
    """
    Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
