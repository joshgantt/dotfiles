# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.config import Key, Screen, Group, Drag, Click, ScratchPad, DropDown
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.log_utils import logger

from typing import List  # noqa: F401

import subprocess
from pathlib import Path
import os
import json

# Open the pywal generated json color scheme; set colors from it
with open("/home/josh/.cache/wal/colors.json", "r") as f:
    theme = json.load(f)

BACKGROUND = theme["special"]["background"]
FOREGROUND = theme["special"]["foreground"]

COLOR0 = theme["colors"]["color0"]
COLOR1 = theme["colors"]["color1"]
COLOR2 = theme["colors"]["color2"]
COLOR3 = theme["colors"]["color3"]
COLOR4 = theme["colors"]["color4"]
COLOR5 = theme["colors"]["color5"]
COLOR6 = theme["colors"]["color6"]
COLOR7 = theme["colors"]["color7"]
COLOR8 = theme["colors"]["color8"]
COLOR9 = theme["colors"]["color9"]
COLOR10 = theme["colors"]["color10"]
COLOR11 = theme["colors"]["color11"]
COLOR12 = theme["colors"]["color12"]
COLOR13 = theme["colors"]["color13"]
COLOR14 = theme["colors"]["color14"]
COLOR15 = theme["colors"]["color15"]

mod = "mod4"
alt = "mod1"
TERMINAL = "termite"

groups = [Group(i) for i in "123456"]

def switch_screens(target_screen):
    '''Send the current group to the other screen.'''
    @lazy.function
    def _inner(qtile):
        current_group = qtile.screens[1 - target_screen].group
        qtile.screens[target_screen].set_group(current_group)

    return _inner

def focus_or_switch(group_name):
    '''
    Focus the selected group on the current screen or switch to the other
    screen if the group is currently active there
    '''
    @lazy.function
    def __inner(qtile):
        # Check what groups are currently active
        groups = [s.group.name for s in qtile.screens]
        try:
            # Jump to that screen if we are active
            index = groups.index(group_name)
            qtile.focus_screen(index)
        except ValueError:
            # We're not active so pull the group to the current screen
            qtile.current_screen.set_group(qtile.groups_map[group_name])

    return __inner

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

#@hook.subscribe.screen_change
#def restart_on_randr(qtile, ev):
#    qtile.cmd_restart()

keys = [
    # Switch between windows in current stack pane
    # Move windows up or down in current stack

    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right()),
    Key([mod, "control"], "Left", switch_screens(0), lazy.next_screen()),
    Key([mod, "control"], "Right", switch_screens(1), lazy.next_screen()),
    Key([mod, alt], "Down", lazy.layout.grow_down()),
    Key([mod, alt], "Up", lazy.layout.grow_up()),
    Key([mod, alt], "Left", lazy.layout.grow_left()),
    Key([mod, alt], "Right", lazy.layout.grow_right()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),    

    # Toggle between different layouts as defined below
    Key([mod, "control"], "space", lazy.next_layout()),
    # Toggle Floating
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),
    # Toggle Fullscreen
    Key([mod], "f", lazy.window.toggle_fullscreen()),


    Key([mod], "q", lazy.window.kill()),
    Key([mod], "d", lazy.spawncmd()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "shift"], "Escape", lazy.shutdown()),

    # Launch applications
    Key([mod], "Return", lazy.spawn(TERMINAL)),
    Key([mod], "e", lazy.spawn('thunar')),

    Key([mod], "l", lazy.spawn('betterlockscreen -l')),
    Key([mod, "shift"], "s", lazy.spawn('cliptool')),

    # Audio/media controls
    Key([], "XF86AudioRaiseVolume", lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ +5%')),
    Key([], "XF86AudioLowerVolume", lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ -5%')),
    Key([], "XF86AudioMute", lazy.spawn('pactl set-sink-mute @DEFAULT_SINK@ toggle')),
    Key([], "XF86AudioMicMute", lazy.spawn('pactl set-source-mute @DEFAULT_SOURCE@ toggle')),
    Key([], "XF86AudioPlay", lazy.spawn('playerctl play-pause')),
    Key([], "XF86AudioNext", lazy.spawn('playerctl next')),
    Key([], "XF86AudioPrev", lazy.spawn('playerctl previous')),
    Key([], "XF86AudioStop", lazy.spawn('playerctl stop'))
]

for i in groups:
    keys.extend([
        Key([mod, "control"], i.name, lazy.group[i.name].toscreen()),
        Key([mod], i.name, focus_or_switch(i.name)),

        Key([mod, "shift"], i.name, lazy.window.togroup(i.name))
    ])

groups.append(ScratchPad("scratchpad", [
    DropDown("term", "termite --title 'Dropdown Terminal'",
        on_focus_lost_hide=True, x=0.1, y=0.0, width=0.8, height=0.7, warp_pointer=False),
    DropDown("spotify", "spotify", on_focus_lost_hide=True, x=0.1, y=0.0, width=0.8, height=0.8, warp_pointer=False)
]))
keys.append(Key([mod], "grave", lazy.group["scratchpad"].dropdown_toggle("term")))
keys.append(Key([mod], "Tab", lazy.group["scratchpad"].dropdown_toggle("spotify")))

layouts = [
    #layout.Max(),
    #layout.Stack(num_stacks=2),
    layout.Bsp(margin=8, fair=False, border_focus=COLOR6, border_normal=COLOR8),
    layout.Floating(border_focus=COLOR4, border_normal=COLOR8)
    #layout.Tile()
]

widget_defaults = dict(
    font='DejaVuSans',
    fontsize=14,
    padding=3,
    background=BACKGROUND,
    foreground=FOREGROUND
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        #top=bar.Gap(size=35),
        top=bar.Bar(
            [
                widget.TextBox("B", font='OpenLogos', fontsize=23, name="logo", background=COLOR6, foreground=BACKGROUND),
                widget.TextBox(
                    text="◢", fontsize=50, padding=0, background=COLOR6, foreground=BACKGROUND
                ),
                widget.CurrentLayoutIcon(scale=.65),
                widget.GroupBox(center_aligned=True, this_current_screen_border=COLOR6, urgent_border=COLOR1),
                widget.WindowName(),
                widget.Prompt(),
                widget.CPUGraph(
                    border_color=FOREGROUND,
                    graph_color=COLOR4,
                    border_width=1,
                    line_width=1,
                    type="line",
                    width=40
                ),
                widget.MemoryGraph(
                    border_color=FOREGROUND,
                    graph_color=COLOR5,
                    border_width=1,
                    line_width=1,
                    type="line",
                    width=40
                ),
                widget.NetGraph(
                    border_color=FOREGROUND,
                    graph_color=COLOR6,
                    border_width=1,
                    line_width=1,
                    type="line",
                    width=40
                ),
                # widget.Battery(format='{percent:2.0%}', low_foreground=COLOR1, padding=0),
                # widget.BatteryIcon(theme_path='/usr/share/icons/Papirus/24x24/panel', padding=0),
                widget.Systray(icon_size=24),
                widget.TextBox(
                    text="◢", fontsize=50, padding=0, foreground=COLOR6
                ),
                widget.Clock(fontsize=20, format='%T', background=COLOR6, foreground=BACKGROUND)
            ],
            28,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
#main = None
follow_mouse_focus = False
bring_front_click = False
cursor_warp = True
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wname': 'dukemed.webex.com is sharing your screen.'},
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
    {'wmclass': 'pavucontrol'},
    {'wmclass': 'gcr-prompter'},
    {'wmclass': 'nm-connection-editor'},
    {'wmclass': 'zoom'},
    {'wmclass': 'Xephyr'}
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "Qtile"
