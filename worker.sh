#!/bin/bash
while (true); do
   if (shopt -s nullglob dotglob; f=(/home/jono/queue/*); ((! ${#f[@]}))); then
       sleep 20;
   else
        python worker.py --config-path /home/jono/
   fi
done
