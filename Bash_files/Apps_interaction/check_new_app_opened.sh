#!/bin/sh

#Get all the currently running apps
running_apps=$(wmctrl -l|echo $(awk '{print $1}'))

while [ 1=1 ]; do
	#Check if the new list is eqyal to the old list
	if [ "${running_apps}" != "$(wmctrl -l|echo $(awk '{print $1}'))" ]; then
		listado=( echo $(wmctrl -l|echo $(awk '{print $1}')) )
		#Get the last opened app
		nuevoid=${listado[-1]}
		echo "$( echo $((${nuevoid})))"
		exit;
	fi
done
exit
