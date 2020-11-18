#!/bin/sh

color_fondo="$1"
color_letras="$2"

#echo "Color elegido: ${color_fondo}"

#runs the app
python3 /home/pi/TvPost/Py_files/Apps/clock_qt.py ${color_fondo} ${color_letras} &

#Check fore new apps
nueva_id=$( bash ~/TvPost/Bash_files/Apps_interaction/check_new_app_opened.sh )

#moves the window
reloj=${nueva_id}
echo ${reloj}

#Writing the id to later kill it
echo "4:${reloj}-" >> ~/TvPost/Resolutions/window_id.txt
