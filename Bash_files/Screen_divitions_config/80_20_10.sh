#!/bin/sh
#Data

width_pixel="$1"
width_mm="$2"
height_pixel="$3"
height_mm="$4"
width_pixel_80="$5"
width_mm_80="$6"
height_pixel_80="$7"
height_mm_80="$8"
adapter="$9"
active_monitors="${10}"

#First monitor 80% width and 90% height
#width_pixel_80=$(( width_pixel * 80/100 ))
#width_mm_80=$(( width_mm * 80/100 ))
#height_pixel_90=$(( height_pixel * 90/100 ))
#height_mm_90=$(( height_mm * 90/100 ))

#Second monitor 20% width and 90% height (Already calculated)
width_pixel_20=$(( width_pixel - width_pixel_80 ))
width_mm_20=$(( width_mm - width_mm_80 ))

#Third monitor 100% width and 10% height
height_pixel_10=$(( height_pixel - height_pixel_80 ))
height_mm_10=$(( height_mm - height_mm_80 ))


#echo "width_pixel: $width_pixel"
#echo "width_mm: $width_mm"
#echo "height_pixel: $height_pixel"
#echo "height_mm: $height_mm"
#echo "width_pixel_80: $width_pixel_80"
#echo "width_mm_80: $width_mm_80"
#echo "height_pixel_80: $height_pixel_80"
#echo "height_mm_80: $height_mm_80"
#echo "height_pixel_10: $height_pixel_10"
#echo "height_mm_10: $height_mm_10"
#echo "adapter: $adapter"
#echo "adapter: $active_monitors"

#Get the values of the new percentajes:
new_screens_values() {
	echo "Screen 1:${width_pixel_80}x${height_pixel_80}" > ~/TvPost/Resolutions/new_resolutions.txt
	echo "Screen 2:${width_pixel_20}x${height_pixel_80}" >> ~/TvPost/Resolutions/new_resolutions.txt
	echo "Screen 3:${width_pixel}x${height_pixel_10}" >> ~/TvPost/Resolutions/new_resolutions.txt
}
	
function split_screen_80_20_10() {
	xrandr --setmonitor ${adapter}~1 ${width_pixel_80}/${width_mm_80}x${height_pixel_80}/${height_mm_80}+0+0 ${adapter}
	xrandr --setmonitor ${adapter}~2 ${width_pixel_20}/${width_mm_20}x${height_pixel_80}/${height_mm_80}+${width_pixel_80}+0 none
	xrandr --setmonitor ${adapter}~3 ${width_pixel}/${width_mm}x${height_pixel_10}/${height_mm_10}+0+${height_pixel_80} none
	
}

function only_10() {
	xrandr --setmonitor ${adapter}~3 ${width_pixel}/${width_mm}x${height_pixel_10}/${height_mm_10}+0+${height_pixel_80} none
	
}

#It only creates the monitors if the 80/20/10 is not
#already selected

#Creates monitor 80/20/10
if [ ${active_monitors} == 1 ]; then
	#echo "entré al if"
	#Creates the screens
	split_screen_80_20_10
	
	#Calling the function to write the new values in txt
	new_screens_values
	
	echo "Cambiado a 802010"
fi
	
#If there are 2 active_monitors then deletes them and recreates them
if [ ${active_monitors} == 2 ]; then
	xrandr --delmonitor ${adapter}~1
	xrandr --delmonitor ${adapter}~2
	
	#Creates the screens
	split_screen_80_20_10
	
	#Calling the function to write the new values in txt
	new_screens_values
	
	echo "Cambiado a 802010"
fi

#Si el reloj viene off y hay 3 pantallas, hacer nada
#If there are 3 active_monitors then deletes them and recreates them
if [ ${active_monitors} == 3 ]; then
	xrandr --delmonitor ${adapter}~3
	
	#Creates the screens
	only_10
	
	#Calling the function to write the new values in txt
	new_screens_values
	
	echo "Cambiada porción 3 "
fi
