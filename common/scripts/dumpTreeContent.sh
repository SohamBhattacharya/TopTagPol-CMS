#!/bin/bash

FILE=$1
TREE=$2

ROOT_CMD=".ls\n_file0->Get(\"${TREE}\")->Print()\n"
#echo $ROOT_CMD

printf $ROOT_CMD | root -l $FILE 
