#!/bin/bash
while (true); do
   if (shopt -s nullglob dotglob; f=(/home/jono/source/queue/*); ((! ${#f[@]}))); then
       echo "The queue is empty."
       sleep 10;
   else
        python worker.py --config-path /home/jono/source/
   fi
done
