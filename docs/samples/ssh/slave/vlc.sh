#!/bin/bash
export DISPLAY=":0.0"
nohup vlc "$@" &>/dev/null
