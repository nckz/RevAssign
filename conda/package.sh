#!/bin/bash
OUTPUT=`conda build ./ --output`
conda build ./
anaconda upload $OUTPUT --force
