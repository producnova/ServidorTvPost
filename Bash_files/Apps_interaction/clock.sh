#!/bin/sh
color_fondo="$1"
color_letras="$2"
width_1=""
#height_1=""
width_2=""
#height_2=""
#width_3=""
#height_3=""

function widths_heights(){
	regex='([0-9]):([0-9]+)x([0-9]+)'
	value=$( cat ~/TvPost/Resolutions/new_resolutions.txt )

	#Get the number of lines to assign variables
	number_lines=$( wc -l < ~/TvPost/Resolutions/new_resolutions.txt)


	while IFS= read -r line; do
		[[ $line =~ $regex ]]

		if [ ${BASH_REMATCH[1]} == 1 ]; then
			width_1=${BASH_REMATCH[2]}
			#height_1=${BASH_REMATCH[3]}
		fi
		
		if [ ${BASH_REMATCH[1]} == 2 ]; then
			#width_2=${BASH_REMATCH[2]}
			height_2=${BASH_REMATCH[3]}
		fi
		
		#~ if [ ${BASH_REMATCH[1]} == 3 ]; then
			#~ width_3=${BASH_REMATCH[2]}
			#~ height_3=${BASH_REMATCH[3]}
		#~ fi
		
	done < <( cat ~/TvPost/Resolutions/new_resolutions.txt )
	return
}

widths_heights;
#runs the app
python3 /home/pi/TvPost/Py_files/Apps/clock_qt.py ${color_fondo} ${color_letras} &

#Check fore new apps
nueva_id=$( bash ~/TvPost/Bash_files/Apps_interaction/check_new_app_opened.sh )

#moves the window
reloj=${nueva_id}
echo ${reloj}
#xdotool windowmove $reloj 1500 $height_2;
#wmctrl -i -r $reloj -e 0,1300,$height_2,-1,-1
echo "x = $width_1"
echo "y = $height_2"

#Writing the id to later kill it
echo "4:${reloj}-" >> ~/TvPost/Resolutions/window_id.txt
