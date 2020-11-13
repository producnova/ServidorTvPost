#!/bin/sh
echo "------------------------------"
echo "Instalando software de terceros..."
echo "------------------------------"
sudo apt-get install xdotool -y
echo "------------------------------"
echo "xdotool instalado correctamente"
echo "------------------------------"
sudo apt-get install wmctrl -y
echo "------------------------------"
echo "wmctrl instalado correctamente"
echo "------------------------------"
sudo apt-get install scrot -y
echo "------------------------------"
echo "scrot instalado correctamente"
echo "------------------------------"
sudo apt-get install ristretto -y
echo "------------------------------"
echo "ristretto instalado correctamente"
echo "------------------------------"
sudo apt-get install viewnior -y
echo "------------------------------"
echo "viewnior instalado correctamente"
echo "------------------------------"
sudo apt-get install xscreensaver -y
echo "------------------------------"
echo "xscreensaver instalado correctamente"
echo "------------------------------"
sudo apt-get install unclutter -y
echo "------------------------------"
echo "unclutter instalado correctamente"
echo "------------------------------"
cd ~/.config/
sudo mkdir lxsession
cd lxsession
sudo mkdir LXDE-pi
cd LXDE-pi
sudo cp /home/pi/TvPost/Bash_files/First_config/autostart .
echo "------------------------------"
echo "archivo autostart configurado correctamente"
echo "------------------------------"
curl -fsSL https://pi.vpetkov.net -o ventz-media-pi
sh ventz-media-pi
echo "------------------------------"
echo "Chromium Media Edition instalado correctamente"
echo "------------------------------"
sudo apt-get install x11vnc -y
echo "------------------------------"
echo "x11vnc instalado correctamente"
echo "------------------------------"
sudo bash ~/TvPost/noVNC/utils/launch.sh
xdotool key ctrl+alt+t
sleep 3
echo "------------------------------"
echo "noVNC configurado correctamente"
echo "------------------------------"
echo "Software de terceros instalados correctamente"
echo "------------------------------"
