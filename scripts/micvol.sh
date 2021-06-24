#!/bin/sh

DEFAULT_SOURCE_INDEX=$(pacmd list-sources | grep "\* index:" | cut -d' ' -f5)

display_volume() {
	if [ -z "$volume" ]; then
	  echo "No Mic Found"
	else
	  volume="${volume//[[:blank:]]/}"
	  if [[ "$mute" == *"yes"* ]]; then
	    echo "[$volume]"
	  elif [[ "$mute" == *"no"* ]]; then
	    echo "$volume"
	  else
	    echo "$volume !"
	  fi
	fi
}
if [ -z "$2" ]; then
	volume=$(pacmd list-sources | grep "index: $DEFAULT_SOURCE_INDEX" -A 7 | grep "volume" | awk -F/ '{print $2}')
	mute=$(pacmd list-sources | grep "index: $DEFAULT_SOURCE_INDEX" -A 11 | grep "muted")
	display_volume
else
	volume=$(pacmd list-sources | grep "$2" -A 6 | grep "volume" | awk -F/ '{print $2}')
	mute=$(pacmd list-sources | grep "$2" -A 11 | grep "muted" )
	display_volume
fi
