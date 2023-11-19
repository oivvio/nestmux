# Nestmux - nested tmux

Running nested sessions of `tmux` is a bit of a hassle. `nestmux` is here to make it easier.

## Installation

    pip install nestmux

## Usage

The first invocation of `nestmux` will create a new `tmux` session with the prefix key `C-h`.

Invoking `nestmux` again inside the first session will create a nested session with the prefix key `C-n`.

Invoking `nestmux` again inside the second session will create a second nested session with the prefix key `C-b`.

## Things to fix

- Add user configuration of prefix keys and arbitrary nesting depth.

- Replace `attach_session` with a function replaces the current python process with the `tmux` process we attach to, instead of adding the `tmux` process as a child process of the current python process.

- Add a video to the README.
