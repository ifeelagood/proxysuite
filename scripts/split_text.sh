#!/bin/bash

FILENAME=$1
LINECOUNT=$2


BASENAME=${FILENAME%.*}
EXT=${FILENAME##*.}

OUTNAME="${BASENAME}${LINECOUNT}.${EXT}"

echo $OUTNAME
if [[ ! -f $FILENAME ]]; then
	echo "File not found"
	exit 1
fi

head -n $LINECOUNT $FILENAME > $OUTNAME
