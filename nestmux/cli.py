import os
import libtmux
from typing import cast, List

from libtmux.server import Server
from libtmux.session import Session

PREFIXES = ["C-h", "C-n", "C-b"]
SOCKET_NAME="NESTMUX"

def new_session(prefix:str, server: Server) -> Session:
    """ Create a new session and set it's prefix key """
    session = server.new_session()

    if prefix != "C-b":
        session.set_option("prefix", prefix)
        session.cmd("bind-key", prefix, "send-prefix")
        session.cmd("unbind", "C-b")

    return session

def attach_session(session: Session):
    # this should be  os.execvp
    # breakpoint()
    os.system(f"tmux -L {SOCKET_NAME} attach-session -t '{session.name}'")

def get_nestinglevel(server: Server, prefixes: List[str]=PREFIXES) -> int:
    """Figure out how deeply nested we are and return the right prefix key to use"""

    try:
        socket_name, pid, session_id = os.environ["TMUX"].split(",")
        last_part_of_socket_name = socket_name.split("/")[-1]
        if last_part_of_socket_name != SOCKET_NAME:
            msg=("Do not you nestmux inside tmux session that are not handled by nestmux")
            raise BaseException(msg)
        else:
            session = cast(Session,server.sessions.get(pid=pid, id=f"${session_id}"))
            prefix = cast(str,session.show_option("prefix"))

            index_of_current_prefix = PREFIXES.index(prefix)
            index_of_next_prefix = index_of_current_prefix + 1
            return index_of_next_prefix


    except KeyError:
        # We are not in a TMUX session, so we are at nesting level 0
        return 0

def start_and_attach_new_session():


    server = libtmux.server.Server(socket_name=SOCKET_NAME)
    nesting_level = get_nestinglevel(server)

    try:
        prefix = PREFIXES[nesting_level]
    except IndexError:
        raise BaseException("Too deep")

    session = new_session(prefix, server)

    if nesting_level == 0:
        attach_session(session)
    else:
        #Unset TMUX environment variable
        old_tmux = os.environ["TMUX"]
        del(os.environ["TMUX"])

        #attach the session
        attach_session(session)

        #Reset TMUX
        os.environ = old_tmux

    #parts = cmd.split(" ")
    #print(parts[0], parts)

    #os.execlp('sh', 'sh', '-c', cmd)

def main():
    start_and_attach_new_session()