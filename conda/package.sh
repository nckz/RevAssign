#!/bin/bash
CHANNEL=nckz
OUTPUT=`conda build ./ --output`
conda build ./ -c $CHANNEL
anaconda upload -c $CHANNEL $OUTPUT -f
