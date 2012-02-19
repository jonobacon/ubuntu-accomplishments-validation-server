#!/bin/bash
while (true); do
   if (shopt -s nullglob dotglob; f=(/home/jono/queue/*); ((! ${#f[@]}))); then
       echo "The queue is empty."
       sleep 20;
   else
        python worker.py --config-path /home/jono/
   fi
done
