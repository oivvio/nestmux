nestmux
=======

## TODO: 

Rewrite without writing config files. Escape key can be specified on the commandline like so. 

    tmux new-session -n MySession \; set-option -g prefix C-a \; bind-key C-a send-prefix
	
Here we also need to check the current NESTMUX_LEVEL and increment by 1, picking up the write escape key for the next level.


## Nested tmux

A configfile defines how many layers of nesting we want to have, and
what escape sequence each level should have.

A script that takes the config file and spits out a set of
shell scripts that are what the 
user then installs.

Or we could go with pip install.

	pip install nestmux

Generate config files for all levels

Insert 

# unset TMUX; tmux -f /tmp/level2 -S level2


And then we can do whatever is best

Any level can be attached to another terminal. And then reattached again.

A helper script that lets you: move windows / children around.
First lists available sources to move
Then lists available destinations


# PYTHONPATH

During development 

	export PYTHONPATH=/home/oivvio/coderepositories/nestmux/nestmux/src/
	
So that I can run the command with out installing into my virtualenv on every run.
