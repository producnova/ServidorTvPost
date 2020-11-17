#!/bin/sh

link="$1"

echo $( echo $link | sed 's#add_TvPostReloj##g' )
