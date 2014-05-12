#!/usr/bin/perl -w
################################################################################
#giScrub.pl:
#Takes a file that contains gene information and pulls out the data related to
#gene NCBI ID and gene function.  This populates a table linking NCBI ID and
#gene function.
#
#THIS SCRIPT WAS SCRAPPED EARLY IN PIPELINE DEVELOPMENT AND WAS NOT COMPLETED
#
#Created by: Thomas Rossi
################################################################################

use strict;
use warnings;

my $usageMsg = q(   Usage: giScrub.pl fastafile

          Extract gene NCBIID and gene function data.

          Output is a file detailing NCBIID and gene function );

#main
&checkUsage();              # comment this line if assigning file name above

my $seqFile = $ARGV[ 0 ];   # comment this line if assigning file name above
my $filename = "OUT-$seqFile";

open(OUTFILE, ">$filename");

open ( IN, $seqFile )  or die "Unable to open: ".$seqFile ;


# grab the first line and start processing
my $inLine = <IN>;

while ( $inLine )
{
   
   my @lineArr = split ('\|', $inLine); #split line to get individual elements
   
   print "$inLine";
   print OUTFILE "$lineArr[3]$lineArr[4]";
   
   $inLine = <IN>;    # last line read is either next header or null
}

#checkUsage
sub checkUsage()
{
   if ( @ARGV == 0 || $ARGV[0] eq "-h" )
   {
      print STDERR "$usageMsg\n";
      exit;
   }
}