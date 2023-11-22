import os
import typer
import libtmux

from .lib import read_config
from .lib import get_next_nestinglevel
from .lib import new_session
from .lib import attach_session


class NoCompletionTyper(typer.Typer):
    """
    A subclass of Typer that removes the 
        --install-completion 
        --show-completion
    flags
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, add_completion=False, **kwargs)

    def get_command(self, ctx: typer.Context):
        self.registered_groups = {}
        return get_command(self, ctx)

app = NoCompletionTyper()


@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    """
    Invoked without a command runs new-session
    """
    if not ctx.invoked_subcommand:
        start_and_attach_new_session()


@app.command(name="new-session")
def start_and_attach_new_session():
    """ Create new session and attach to it. """
    config = read_config()
    server = libtmux.server.Server(socket_name=config["socket_name"])
    nesting_level = get_next_nestinglevel(server, config)

    try:
        prefix = config["prefixes"][nesting_level]
    except IndexError:
        raise BaseException("Too deep")

    session = new_session(prefix, server)

    if nesting_level == 0:
        attach_session(session,config)
    else:
        #Unset TMUX environment variable
        tmux_env = os.environ["TMUX"]
        del(os.environ["TMUX"])

        attach_session(session,config)

        #Reset TMUX
        os.environ = tmux_env

    #parts = cmd.split(" ")
    #print(parts[0], parts)

    #os.execlp('sh', 'sh', '-c', cmd)

@app.command()
def list_sessions():
    """List sessions."""
    config = read_config()
    cmd = f"tmux -L {config['socket_name']} list-sessions"
    os.system(cmd)

def main():
    app()
