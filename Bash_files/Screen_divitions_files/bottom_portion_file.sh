#!/bin/sh

#Resolutions
width_1=""
height_1=""
width_2=""
height_2=""
width_3=""
height_3=""

regex='([0-9]):([0-9]+)x([0-9]+)'
value=$( cat ~/TvPost/Resolutions/new_resolutions.txt )

#Get the number of lines to assign variables
number_lines=$( wc -l < ~/TvPost/Resolutions/new_resolutions.txt)


while IFS= read -r line; do
	[[ $line =~ $regex ]]

	if [ ${BASH_REMATCH[1]} == 1 ]; then
		width_1=${BASH_REMATCH[2]}
		height_1=${BASH_REMATCH[3]}
	fi
	
	if [ ${BASH_REMATCH[1]} == 2 ]; then
		width_2=${BASH_REMATCH[2]}
		height_2=${BASH_REMATCH[3]}
	fi
	
	if [ ${BASH_REMATCH[1]} == 3 ]; then
		width_3=${BASH_REMATCH[2]}
		height_3=${BASH_REMATCH[3]}
	fi
	
done < <( cat ~/TvPost/Resolutions/new_resolutions.txt )

file_in_screen_1="$1"

file_type=$( bash ~/TvPost/Bash_files/Screen_divitions_files/regex_bottom_file.sh "${file_in_screen_1}" )

#Moves to the correct portion of the screen
xdotool mousemove 10 $(( ${height_1} + 10 ))
xdotool click 1;

#If matches gif open with ristretto
if [ ${file_type} == "image_nopng" ]
then

	#runs the app
	ristretto $file_in_screen_1 &
	
	#Check fore new apps
	nueva_id=$( bash ~/TvPost/Bash_files/Apps_interaction/check_new_app_opened.sh )
	
	#moves the window
	active_window_3=${nueva_id}
	xdotool windowmove $active_window_3 0 $(( ${height_1} + 10 ))
	
	#goes fullscreen
	xdotool getactivewindow key F11
	xdotool getactivewindow key ctrl+shift+0
	#Writing the id to later kill it
	echo "3:${active_window_3}-" >> ~/TvPost/Resolutions/window_id.txt
	exit
fi

#If matches a png, jpg, or jpeg open with image viewer
if [ ${file_type} == "image_png" ]
then

	#runs the app
	gpicview $file_in_screen_1 &
	
	#Check fore new apps
	nueva_id=$( bash ~/TvPost/Bash_files/Apps_interaction/check_new_app_opened.sh )
	
	#moves the window
	active_window_3=${nueva_id}
	xdotool windowmove $active_window_3 0 $(( ${height_1} + 10 ))
	
	#goes fullscreen
	xdotool getactivewindow key F11 
	
	#Writing the id to later kill it
	echo "3:${active_window_3}-" >> ~/TvPost/Resolutions/window_id.txt
	exit
fi

#If it matches a video open with vlc
if [ ${file_type} == "local_video" ]
then

	#runs the app
	vlc -A alsa,none --alsa-audio-device default --repeat $file_in_screen_1 &
	
	#Check fore new apps
	nueva_id=$( bash ~/TvPost/Bash_files/Apps_interaction/check_new_app_opened.sh )
	
	#moves the window
	active_window_3=${nueva_id}
	xdotool windowmove $active_window_3 0 $(( ${height_1} + 10 ))
	
	#Wait 1.5 seconds and then goes fullscreen
	#goes fullscreen
	sleep 1.5
	xdotool getactivewindow key f
	
	#Writing the id to later kill it
	echo "3:${active_window_3}-" >> ~/TvPost/Resolutions/window_id.txt
	exit
fi

#If it matches a youtube link, open and play in full screen
if [ ${file_type} == "online_youtube" ]
then

	#Opening and moving Chrome. Waiting seconds and go fullscreen
	bash ~/TvPost/Bash_files/Apps_interaction/bottom_chromeos-browser.bash $file_in_screen_1 &

	#Check fore new apps
	nueva_id=$( bash ~/TvPost/Bash_files/Apps_interaction/check_new_app_opened.sh )
	
	#moves the window
	active_window_3=${nueva_id}
	xdotool windowmove $active_window_3 0 $(( ${height_1} + 10 ))
	sleep 20
	
	#goes fullscreen
	xdotool getactivewindow key f
	
	echo "3:${active_window_3}-" >> ~/TvPost/Resolutions/window_id.txt
	exit
fi

#If it matches a url open with chromium
if [ ${file_type} == "online_browser" ]
then

	#runs the app
	bash ~/TvPost/Bash_files/Apps_interaction/chromeos-browser.bash $file_in_screen_1 &
	
	#Check fore new apps
	nueva_id=$( bash ~/TvPost/Bash_files/Apps_interaction/check_new_app_opened.sh )
	
	#moves the window
	active_window_3=${nueva_id}
	xdotool windowmove $active_window_3 0 $(( ${height_1} + 10 ))

	#Writing the id to later kill it
	echo "3:${active_window_3}-" >> ~/TvPost/Resolutions/window_id.txt
	exit
fi
