#!/bin/sh
amixer set Capture nocap && notify-send -u critical -t 1000000000 -- 'muted'
