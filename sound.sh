#!/bin/bash
#call command with [audio file] [volume [0-100]]

amixer set Master $2%

aplay /home/pi/Desktop/Surg/sound/$1
