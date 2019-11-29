#!/bin/bash

NAME=$$1

# Figure out which nesting level we are at
if [ -z "$$NESTMUXLEVEL" ]
then
      LEVEL=1
else
    # If we are in tmux rename the window we are in
    PARENTSOCKETPATH="nestmuxlevel$$NESTMUXLEVEL"
    tmux -L $$PARENTSOCKETPATH rename-window $$NAME
    
    LEVEL=$$((NESTMUXLEVEL + 1))
fi

# Set the sessionname
SOCKETPATH="nestmuxlevel$$LEVEL"

# Set the config file
CONFIGFILE="$configpath/nestmuxconfig_level$$LEVEL"

# IF WE ARE NOT AT THE LAST LEVEL
unset TMUX

# Put the current level into the environment
export NESTMUXLEVEL=$$LEVEL



# Start tmux
# tmux -S $$SOCKETPATH -f $$CONFIGFILE -n $$NAME
tmux -L $$SOCKETPATH -f $$CONFIGFILE new-session -s $$NAME
