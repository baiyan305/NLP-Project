#author swetha
#
#This script installs necessary packages needed for the running of our system.
#
#1.scipy. It is used for clustering.
#2.csh. Since we need to call shell command to run Sensecluster_scorer perl script, so we use csh instead of bash.
#3.builder-essential. We need it to compile Algorithm-Munkres.
#4.Algorithm-Munkres. Module for Sensecluster_scorer

sudo apt-get update
echo "===================================="
echo "============install scipy==========="
echo "===================================="
sudo apt-get install python-scipy
echo "===================================="
echo "============install csh============="
echo "===================================="
sudo apt-get install csh
echo "===================================="
echo "============install make============"
echo "===================================="
sudo apt-get install build-essential
echo "===================================="
echo "===========install Munkres=========="
echo "===================================="
cd Algorithm-Munkres-0.08
sudo perl Makefile.PL
sudo make
sudo make install 
