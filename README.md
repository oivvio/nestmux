# Nestmux - Run nested tmux sessions with ease

Running nested sessions of `tmux` is a bit of a hassle. `nestmux` is here to make it easier.

## Installation

    pip install nestmux

## Usage

The first invocation of `nestmux` will create a new `tmux` session with the prefix key `C-h`.

Invoking `nestmux` again inside the first session will create a nested session with the prefix key `C-n`.

Invoking `nestmux` again inside the second session will create a second nested session with the prefix key `C-b`.

## Configuration

`nestmux` is configured with a json file located at `~/.config/nestmux/nestmux.json`. The default configuration is

```
{
	"prefixes": ["C-h", "C-n", "C-b"],
	"socket_name": "NESTMUX"
}
```

`prefixes` is an arbitrarily long ordered list of prefix keys, where the first element will be the prefix key for the first nesting level and so on. The length of this list controls the maximum nesting depth.

`socket_name` is the name of the `tmux` socket. There's rarely a point in setting this to anything other than the default.

## Things to fix

- Replace `attach_session` with a function replaces the current python process with the `tmux` process we attach to, instead of adding the `tmux` process as a child process of the current python process.

- Add a video to the README.

- Change to TOML for config

- Nicer error messages.

- Command to validate config.

- Command to show config.

- Modify attach-session to have an option to only allow attaching of session that have the "right" nesting level. And make this the default.

- In list-sessions display the nestinglevel and wheater it's can be attached from the current context.

- new-session  should take an optional name argument. This should be checked for uniqueness. If it's not unique, append a count. 

- In list-sessions display whether the session is attached or not.

- attach-session is not able to attach from within another session
