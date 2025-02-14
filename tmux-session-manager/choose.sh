#!/bin/bash
#change my path
saveDir="$HOME/.tmux/resurrect/"

# choose a saved session
savedSession=${saveDir}$(ls -t ${saveDir} | tail -n +2 | fzf)

# update symbolic link
if [[ -n "$name" ]]; then
  ln -sf ${savedSession} ${saveDir}last
  tmux display-message "Changed session :D"
fi

# in tmux.conf
# set -g @resurrect-hook-pre-restore-all 'bash ~/scripts/tmux-session-manager/choose.sh'
