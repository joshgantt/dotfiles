#!/bin/bash

function run {
  if ! pgrep $1 ;
  then
    $@&
  fi
}

feh --bg-fill ~/pictures/background
compton -b
xfce4-power-manager
nm-applet &
#pulseaudio -D
pasystray &
