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

from typing import List  # noqa: F401
from libqtile import qtile
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import hook
from libqtile.command import lazy
from datetime import datetime as dt
import os
import subprocess
from libqtile.utils import send_notification

# When application launched automatically focus it's group
@hook.subscribe.client_new
def modify_window(client):
    #if (client.window.get_wm_transient_for() or client.window.get_wm_type() in floating_types):
    #    client.floating = True

    for group in groups:  # follow on auto-move
        match = next((m for m in group.matches if m.compare(client)), None)
        if match:
            targetgroup = client.qtile.groups_map[group.name]  # there can be multiple instances of a group
            targetgroup.cmd_toscreen(toggle=False)
            break


# Work around for matching Spotify
import time

@hook.subscribe.client_new
def slight_delay(window):
	time.sleep(0.04)

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    #subprocess.Popen([home + '/.config/qtile/autostart.sh'])

# Add th, nd or st to the date - use custom_date in text box
def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

def custom_date():
	return custom_strftime('%A {S} %B %Y - %H:%M', dt.now())

from libqtile.utils import send_notification

mod = "mod4"

terminal = 'alacritty'
home = os.path.expanduser('~')

MYCOLORS = [
    '#073642',
    '#dc322f',
    '#00ff2a',
    '#b58900',
    '#268bd2',
    '#d33682',
    '#2aa198',
    '#eee8d5'
]

BLACK = MYCOLORS[0]
RED = MYCOLORS[1]
GREEN = MYCOLORS[2]
YELLOW = MYCOLORS[3]
BLUE = MYCOLORS[4]
MAGENTA = MYCOLORS[5]
CYAN = MYCOLORS[6]
WHITE = MYCOLORS[7]

keys = [

    # Switch between windows in current stack pane
    Key([mod], "Down", lazy.layout.down(),
        desc="Move focus down in stack pane"),
    Key([mod], "Up", lazy.layout.up(),
        desc="Move focus up in stack pane"),

    Key([mod], "Left", lazy.layout.left()),
	Key([mod], "Right", lazy.layout.right()),
	Key([mod, "shift"], "Left", lazy.layout.shuffle_left()),
	Key([mod, "shift"], "Right", lazy.layout.shuffle_right()),
	Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
	Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
	Key([mod, "mod1"], "j", lazy.layout.flip_down()),
	Key([mod, "mod1"], "k", lazy.layout.flip_up()),
	Key([mod, "mod1"], "h", lazy.layout.flip_left()),
	Key([mod, "mod1"], "l", lazy.layout.flip_right()),
	Key([mod, "control"], "j", lazy.layout.grow_down()),
	Key([mod, "control"], "k", lazy.layout.grow_up()),
 	Key([mod, "control"], "h", lazy.layout.grow_left()),
	Key([mod, "control"], "l", lazy.layout.grow_right()),
	Key([mod], "n", lazy.layout.normalize()),
	Key([mod], "h",
             lazy.layout.grow(),
             lazy.layout.increase_nmaster(),
             desc='Expand window (MonadTall), increase number in master pane (Tile)'
             ),
         Key([mod], "l",
             lazy.layout.shrink(),
             lazy.layout.decrease_nmaster(),
             desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
             ),
    Key([mod], "Return", lazy.spawn('alacritty')),
    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next(),
        desc="Switch window focus to other pane(s) of stack"),
    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate(),
        desc="Swap panes of split stack"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod,"shift"], "q", lazy.window.kill(), desc="Kill focused window"),

    #Set layout to tree
    Key([mod],'w',lazy.layout.TreeTab),
    # Qtile system keys
    #
    Key([mod, "control"], "r", lazy.restart(), desc="Restart qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Rofi
    Key([mod], "d", lazy.spawn("rofi -modi drun,run -show drun -sidebar-mode -terminal termite -color-window '#000000, #000000, #000000' -color-normal '#000000, #b3e774, #000000, #b3e774, #000000' -color-active '#000000, #b3e774, #000000, #b3e774, #000000' -color-urgent '#000000, #b3e774, #000000, #b3e774, #000000'")),
    Key([mod], "m", lazy.spawn("/home/majkel/scripts/micmute.sh")),
    Key([mod,'shift'], "m", lazy.spawn("/home/majkel/scripts/micunmute.sh")),

    # Terminal apps
    Key([mod], "F3", lazy.spawn("alacritty -e bluetoothctl")),
    Key([mod], "F4", lazy.spawn("alacritty -e alsamixer")),

    # emacs
    Key([mod,"shift"],'e',lazy.spawn("emacs")),
    # ------------ Hardware Configs ------------
    # Volume
    Key([], "XF86AudioMute", lazy.spawn('amixer -D pulse sset Master toggle')),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -D pulse sset Master 10%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -D pulse sset Master 10%+")),


    # Brightness
    Key([], "XF86MonBrightnessDown", lazy.spawn('xbacklight -dec 5')),
    Key([], "XF86MonBrightnessUp", lazy.spawn('xbacklight -inc 5')),


    # Save screen to screenshots folder
	Key([mod, 'control','shift'], "s", lazy.spawn("/usr/bin/spectacle -br -o /Pictures/Screenshots/screenshot_%d_%m_%Y_%H_%M_%S.png && xclip -sel clip -t image/png ) /Pictures/Screenshots/screenshot_%d_%m_%Y_%H_%M_%S.png")),
	# Capture region of screen to clipboard
	Key([mod, "shift"], "s", lazy.spawn("/usr/bin/spectacle -bcr")),
]

# Groups with matches

workspaces = [
    {"name": "I", "key": "1"},
    {"name": "II", "key": "2"},
    {"name": "III", "key": "3"},
    {"name": "IV", "key": "4"},
    {"name": "V", "key": "5"},
    {"name": "VI", "key": "6"},
]

groups = []
for workspace in workspaces:
    matches = workspace["matches"] if "matches" in workspace else None
    groups.append(Group(workspace["name"], matches=matches, layout="monadtall"))
    keys.append(Key([mod], workspace["key"], lazy.group[workspace["name"]].toscreen()))
    keys.append(Key([mod, "shift"], workspace["key"], lazy.window.togroup(workspace["name"])))

##### DEFAULT THEME SETTINGS FOR LAYOUTS #####
layout_theme = {"border_width": 3,
                "margin": 0,
                "border_focus": BLUE,
                "border_normal": BLACK
                }

layouts = [
    layout.Bsp(**layout_theme),
    layout.TreeTab(),
    layout.MonadTall(**layout_theme),
    # layout.Stack(num_stacks=2, **layout_theme),
    # layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Columns(),
    # layout.Matrix(),
     # layout.MonadWide(),
     # layout.RatioTile(),
     layout.Tile(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='Overpass Mono',
    fontsize=12,
    padding=2,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(

                wallpaper='~/Downloads/image.png',
                wallpaper_mode='fill',
        top=bar.Bar(
            [
                widget.GroupBox(borderwidth=2,disable_drag=True ,inactive='969696',this_current_screen_border='eee8d5', this_screen_border='eee8d5', font='Overpass Mono', fontsize=15, highlight_method='line'),
                widget.CurrentLayoutIcon(scale = 0.7),
                widget.CurrentLayout(**widget_defaults),
                widget.Net(format='{down} {up}'),
                widget.Prompt(**widget_defaults),
                widget.Spacer(),
                widget.GenPollText(func=custom_date, update_interval=1, **widget_defaults),
                widget.Spacer(),
                widget.Spacer(length = 10),
                widget.TextBox(text="Mic: "),
                widget.GenPollText(update_interval=1,padding=5,func=lambda: subprocess.check_output(os.path.expanduser("~/scripts/micvol.sh")).decode('utf-8')),
                widget.TextBox(
                    text=":",
                    padding=5,
                    foreground=WHITE,
                    fontsize=16
                ),

                widget.Battery(padding=5),
                widget.Volume(emoji=True,**widget_defaults),
                widget.Volume(**widget_defaults),
                widget.TextBox(
                    Font='Font Awesome',
                    text=":",
                    padding=5,
                    foreground=WHITE,
                    fontsize=14
                ),
                widget.Backlight(brightness_file='/sys/class/backlight/intel_backlight/brightness',change_command="xbacklight -set {0}",max_brightness_file="/sys/class/backlight/intel_backlight/max_brightness",**widget_defaults),
                widget.GenPollText(update_interval=1, **widget_defaults, func=lambda: subprocess.check_output(os.path.expanduser("~/scripts/network.sh")).decode(), mouse_callbacks = { 'Button3': lambda: qtile.cmd_spawn('alacritty -e nmtui', shell=True)}),
                widget.Wlan(interface='wlp2s0',format='{essid}',mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(os.path.expanduser("alacritty -e nmtui"), shell=True)},**widget_defaults),
            ],
            25,background = '#1d1f21' ,margin=[0, 0, 0, 0] # N E S W
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
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    Match(title='Quit and close tabs?'),
    Match(wm_type='utility'),
    Match(wm_type='notification'),
    Match(wm_type='toolbar'),
    Match(wm_type='splash'),
    Match(wm_type='dialog'),
    Match(wm_class='Conky'),
    Match(wm_class='Firefox'),
    Match(wm_class='file_progress'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
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
