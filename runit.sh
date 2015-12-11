#author swetha
#
#! /bin/sh
#
#This script receives input data file path then start Main.py.
#
#Example: ./runit.sh teamdata/commit.xml

if [ $# = 1 ]   #if 1 arguments found, pass input file and target words to Main.py
then
    python Main.py $1
else    #otherwise, echo error
    echo "wrong number of arguments"
fi
