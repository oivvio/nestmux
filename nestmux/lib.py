import os
import json

from pathlib import Path
from typing import cast, List, TypedDict


from libtmux.server import Server
from libtmux.session import Session

import subprocess

class Config(TypedDict):
    prefixes: List[str]
    socket_name: str


def get_server(config: Config) -> Server:
    return Server(socket_name=config["socket_name"])

def read_config() -> Config:
    """
    Read the config from ~/.config/nestmux/nestmux.json 
    If that file does not exist or is not valid json, fall back to the default config.
    """
    
    # Set the default config
    result = cast(Config,{"prefixes": ["C-h", "C-n", "C-b"], "socket_name": "NESTMUX"})
    try:
        home = Path.home()
        config_path = home / ".config" / "nestmux" / "nestmux.json"

        if config_path.exists():
            result = cast(Config, json.loads(config_path.open().read()))

    except json.decoder.JSONDecodeError:
        print("Config file invalid, falling back to default config")

    return result    

def new_session(prefix:str, server: Server) -> Session:
    """ Create a new session and set it's prefix key """
    session = server.new_session()

    session.set_option("prefix", prefix)
    if prefix != "C-b":
        session.cmd("bind-key", prefix, "send-prefix")
        session.cmd("unbind", "C-b")

    return session


def attach_session(session: Session, config: Config, detach=True):
    # this should be  os.execvp

    socket_name = config["socket_name"]
    detach_str = " -d " if detach else ""
    cmd = f"tmux -L {socket_name} attach-session -t '{session.name}' {detach_str} "
    os.system(cmd)


def get_next_nestinglevel(server: Server, config: Config) -> int:
    """Figure out how deeply nested we are and return the next nesting level """

    try:
        socket_name, pid, session_id = os.environ["TMUX"].split(",")
        last_part_of_socket_name = socket_name.split("/")[-1]
        if last_part_of_socket_name != config["socket_name"]:
            msg=("Do not you nestmux inside tmux session that are not handled by nestmux")
            raise BaseException(msg)
        else:
            session = cast(Session,server.sessions.get(pid=pid, id=f"${session_id}"))
            prefix = cast(str,session.show_option("prefix"))

            index_of_current_prefix =  config["prefixes"].index(prefix)
            index_of_next_prefix = index_of_current_prefix + 1
            return index_of_next_prefix


    except KeyError:
        # We are not in a TMUX session, so we are at nesting level 0
        return 0
