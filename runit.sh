#author swetha
#
#! /bin/sh
#
#This script receives input data file path, 1 or 2 target words. Then start Main.py.
#
#Example 1: ./runit.sh teamdata/commit.xml commit
#Example 2: ./runit.sh teamdata/government_year.xml government year

if [ $# = 1 ]   #if 2 arguments found, pass input file and target words to Main.py
then
    python Main.py $1 $2 
else    #otherwise, echo error
    echo "wrong number of arguments"
fi
