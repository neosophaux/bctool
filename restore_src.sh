#!/usr/bin/bash

SRC_LOC=$HOME/Work/apk/gg

if rm -rf $SRC_LOC/smali/* &> /dev/null; then
    if cp -r $SRC_LOC/smali_bak/* -t $SRC_LOC/smali; then
        echo "Restored."
    else
        echo "Failed. $SRC_LOC"
    fi
else
    echo "Failed. $SRC_LOC"
fi