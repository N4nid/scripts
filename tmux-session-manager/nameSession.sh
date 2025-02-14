#!/bin/bash
# change my path
saveDir="$HOME/.tmux/resurrect/"

sessionToName=$(ls -t ${saveDir} | fzf)
printf "To abort use Ctr-c or leave empty\n"
printf "New name for ${sessionToName}: \n"
read name
printf ${name}

# abort if name is empty
if [[ -n "$name" ]]; then
  cd ${saveDir}
  mv ${sessionToName} ${name}
  rm last
  ln -sf ${name} last
  tmux display-message "Done :3"
else
  tmux display-message "aborted"
fi

# in tmux.conf
# set -g @resurrect-hook-post-save-all 'tmux display-popup -E "~/scripts/tmux-session-manager/nameSession.sh"'
# bind N run-shell -b 'tmux display-popup -E "~/scripts/tmux-session-manager/nameSession.sh"'
