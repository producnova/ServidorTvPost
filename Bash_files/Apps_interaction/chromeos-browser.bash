#!/bin/sh

cd ~/.cache/chromium/Default/Cache/
find . -name '*'|xargs rm -r;

sudo sed -i 's+exit_type":"Crashed+exit_type":"Normal+g' /home/pi/.config/chromium/Default/Preferences
echo "dato chromium cambiado"

#Chromium
chromium-browser %U --user-agent="Mozilla/5.0 (X11; CrOS armv7l 12371.89.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36" --start-maximized --new-window $1 ||
chromium %U --user-agent="Mozilla/5.0 (X11; CrOS armv7l 12371.89.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36" --start-maximized --new-window $1
