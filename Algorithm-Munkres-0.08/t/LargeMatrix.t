# LargeMatrix.t version 0.01
#
# Copyright (C) 2005 - 2006
#
# Anagha Kulkarni, University of Minnesota Duluth
# kulka020@d.umn.edu
#
# Ted Pedersen, University of Minnesota Duluth
# tpederse@d.umn.edu

# A script to run tests on the Algorithm::Mukres module.
# The following are among the tests run by this script:
# This test case checks the module performance for a matrix of size 25x25
# 1. Try loading the Algorithm::Munkres i.e. is it added to the @INC variable
# 2. Compare the lengths of the Solution array and the Output array.
# 3. Compare each element of the Solution array and the Output array.

use strict;
use warnings;

use Test::More tests => 27;

BEGIN { use_ok('Algorithm::Munkres') };

my @mat = (
	[ 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45],
	[ 3.6, 11.2, 10, 3, 5, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45,],
	[ 9, 7, 15.5, 1, 6, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45,],
	[ 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45],
	[ 3.6, 11.2, 10, 3, 5, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45,],
	[ 9, 7, 15.5, 1, 6, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45,],
	[ 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45],
	[ 3.6, 11.2, 10, 3, 5, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45,],
	[ 9, 7, 15.5, 1, 6, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45,],
	[ 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45],
	[ 3.6, 11.2, 10, 3, 5, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45,],
	[ 9, 7, 15.5, 1, 6, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45,],
	[ 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45],
	[ 3.6, 11.2, 10, 3, 5, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45,],
	[ 9, 7, 15.5, 1, 6, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45,],
	[ 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45],
	[ 3.6, 11.2, 10, 3, 5, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45,],
	[ 9, 7, 15.5, 1, 6, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45,],
	[ 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45],
	[ 3.6, 11.2, 10, 3, 5, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45,],
	[ 9, 7, 15.5, 1, 6, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45,],
	[ 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45],
	[ 3.6, 11.2, 10, 3, 5, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45,],
	[ 9, 7, 15.5, 1, 6, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45,],
	[ 9, 7, 15.5, 1, 6, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45, 11.4, 1, 90, 10, 45,],
	);

my @soln = (1,0,3,5,2,6,7,4,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24);

my @assign_out = ();
my $i = 0;

assign(\@mat,\@assign_out);

#Compare the lengths of the Solution array and the Output array.
is($#soln, $#assign_out, 'Compare the lengths of the Solution array and the Output array.');

#Compare each element of the Solution array and the Output array.
for($i = 0; $i <= $#assign_out; $i++)
{
	is($soln[$i], $assign_out[$i], "Compare $i element of the Solution array and the Output array")	
}

__END__