#!/bin/bash
CHANNEL=nckz
OUTPUT=`conda build ./ --output`
conda build ./
anaconda upload -u $CHANNEL $OUTPUT --force
