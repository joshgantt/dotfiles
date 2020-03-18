#!/bin/bash

rofi_command="rofi -columns 4 -lines 1 -m 0 -theme themes/powermenu.rasi"

# Each of the icon is a selectable element
#options=$'\n\n\n\n'
options=$'\n\n\n'
#options=$'1\n2\n3\n4'

chosen="$(echo "$options" | $rofi_command -dmenu)"
case $chosen in
    ) # Lock the screen
        betterlockscreen -l
        ;;
    ) # Suspend
        betterlockscreen -s
        ;;
    ) # Shutdown the computer
        systemctl poweroff
        ;;
    ) # Reboot the computer
        systemctl reboot
        ;;
    # ) # Log out of the current session
    #     i3-msg exit
    #     ;;
esac
