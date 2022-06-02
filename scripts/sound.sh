#!/bin/bash
#call command with [audio file] [volume [0-100]]

#amixer sset Master $50%

aplay ~/Desktop/arcade.wav
sleep 1
aplay ~/Desktop/whoosh.wav