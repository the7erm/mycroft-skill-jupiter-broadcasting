#!/bin/bash
export DISPLAY=":0.0"
nohup firefox "$@" &>/dev/null
