#! /bin/sh

if [ $# = 2 ]
then
    python3 Main.py $1 $2 
elif [ $# = 3 ]
then
    python3 Main.py $1 $2 $3
else
    echo "wrong number of arguments"
fi
