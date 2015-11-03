#!/bin/bash
# wrap into an app using wrappaconda
WRAPPACONDA=$1
$WRAPPACONDA -n RevAssign -t ../RevAssign.py -o --py2 -c nckz -p revassign
