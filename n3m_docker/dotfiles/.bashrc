#!/bin/bash

if [ -e /usr/share/terminfo/x/xterm-256color ]; then
        export TERM='xterm-256color'
else
        export TERM='xterm-color'
fi

shopt -s histappend
shopt -s checkwinsize

if [ -r "$HOME/.tmux-completion.bash" ]; then
  source $HOME/.tmux-completion.bash
fi

if [ -r "$HOME/.git-completion.bash" ]; then
  source $HOME/.git-completion.bash
fi

parse_git_branch() {
     git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}
export PS1="\u@\h \[\033[32m\]\w\[\033[33m\]\$(parse_git_branch)\[\033[00m\] $ "
export HISTSIZE='100000'
export HISTCONTROL=ignoredups:erasedups 
shopt -s histappend
export PROMPT_COMMAND="history -a; history -n; $PROMPT_COMMAND"

export DATABASE_URL="postgresql:///n3mdb?client_encoding=utf8"

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8

PATH=$PATH:/usr/lib/postgresql/9.5/bin
export PATH

