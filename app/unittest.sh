#!/bin/bash

source common.sh

cd src
for d in `find . -type d ` ; do
    echo ${d}
    python -m unittest discover -v ${d}
done 
