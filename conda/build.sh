#!/bin/bash

set -x
set -e

# copy to site-packages
mkdir -p $SP_DIR/RevAssign
cp -R * $SP_DIR/RevAssign/

exit
