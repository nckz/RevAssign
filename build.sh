#!/bin/sh
# Brief: For building Qt4 UI

set -x
set -e

## QT4 UI (C to PYTHON)
# osx
pyuic4-2.7 window.ui -o windowUi.py -x

# ubuntu
#pyuic4 window.ui -o windowUi.py -x
