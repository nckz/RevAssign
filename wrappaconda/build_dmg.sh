#!/bin/bash
# Author: Nick Zwart
# Date: 2015nov04
#
# Bundle the RevAssign.app in a dmg for distribution.
# git clone https://github.com/andreyvit/create-dmg.git

# Make sure root is running this script.
#   root is needed for:
#       -creating a disk image
#       -copying a root owned app from /Applications
if [ "$(id -u)" != "0" ]; then
    echo "You must be a root user to modify the $DEST directory" 2>&1
    echo "build aborted."
    exit 1
fi

VERSION="0.1.0"

YPOS_TRG=150
XPOS_TRG=600

YPOS_LNK=350
XPOS_LNK=600

ICON_SIZE=128
WINDOW_SIZE="700 550" # same size as the background image
BKGND_IMG=../icon.png

VOLUME_NAME=REVASSIGN_$VERSION
TARGET=RevAssign.app
TARGET_DIR=/Applications
OUTPUT_DMG=RevAssign_$VERSION.dmg
TMP_DIR=./tmp

# clean tmp directory
if [ -d "$TMP_DIR" ]; then
    echo "Removing current tmp dir $TMP_DIR ..."
    rm -rf $TMP_DIR
fi
echo "Making tmp dir $TMP_DIR ..."
mkdir -p $TMP_DIR

# copy so that the Finder doesn't get its grubby mitts on the file while packaging.
echo "copy $TARGET to $TMP_DIR ..."
cp -R $TARGET_DIR/$TARGET $TMP_DIR/

# clean working directory
if [ -f "$OUTPUT_DMG" ]; then
    echo "Removing currently installed $OUTPUT_DMG ..."
    rm -rf $OUTPUT_DMG
fi

# bundle in dmg
./create-dmg/create-dmg --volname $VOLUME_NAME \
    --background $BKGND_IMG \
    --window-size $WINDOW_SIZE \
    --icon-size $ICON_SIZE \
    --icon $TARGET $XPOS_TRG $YPOS_TRG \
    --app-drop-link $XPOS_LNK $YPOS_LNK \
    $OUTPUT_DMG $TMP_DIR/$TARGET
