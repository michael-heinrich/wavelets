#!/bin/bash

# define the display
DISPLAY=$(grep -oP "(?<=nameserver ).+" /etc/resolv.conf):0.0
#DISPLAY= $(grep -oP "(?<=nameserver ).+" /etc/resolv.conf):0.0
# print the display
echo $DISPLAY

# export the display
export DISPLAY


# export DISPLAY=`grep -oP "(?<=nameserver ).+" /etc/resolv.conf`:0.0