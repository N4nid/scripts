#!/bin/bash
#change my path
saveDir="$HOME/.tmux/resurrect/"

# choose a saved session
savedSession=${saveDir}$(ls -t ${saveDir} | tail -n +2 | fzf --tmux center)

# update symbolic link
ln -sf ${savedSession} ${saveDir}last
tmux display-message "Changed session :D"

# in tmux.conf
# set -g @resurrect-hook-pre-restore-all 'bash ~/scripts/tmux-session-manager/choose.sh'
