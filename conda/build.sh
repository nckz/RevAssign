#!/bin/bash

set -x
set -e

# copy to site-packages
mkdir -p $SP_DIR/RevAssign
cp -R * $SP_DIR/RevAssign/

# copy launcher
cp /bin/revassign $PREFIX/bin/

exit
