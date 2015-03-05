#!/bin/sh
# Brief: For building "the Decider" C routine and Qt4 UI

set -x
set -e

## C EXT MODULE
# build the extension module for sorting
python decutil_setup.py build_ext --inplace

## QT4 UI (C to PYTHON)
# osx
pyuic4-2.7 window.ui -o windowUi.py -x

# ubuntu
#pyuic4 window.ui -o windowUi.py -x
