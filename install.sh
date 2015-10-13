#author swetha
#
#This script installs necessary packages needed for the running of our system.
#
#1.Python 3.
#2.lxml. It is a external library for parsing XML file. It is stronger than Python built-in XML parser.
#3.csh. Since we need to call shell command to run Sensecluster_scorer perl script, so we use csh instead of bash.
#4.builder-essential. We need it to compile Algorithm-Munkres.
#5.Algorithm-Munkres. Module for Sensecluster_scorer

sudo apt-get update
echo "===================================="
echo "==========install python 3=========="
echo "===================================="
sudo apt-get install python3
echo "===================================="
echo "==========install lxml=============="
echo "===================================="
sudo apt-get install python3-lxml
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
