#!/usr/bin/perl -w
################################################################################
#giScrub.pl:
#THIS FILE WAS SCRAPPED EARLY IN PIPELINE DEVELOPMENT AND WAS NOT COMPLETED
#IT SERVES NO PURPOSE IN OUR PIPELINE, WAS NOT DEBUGGED, AND SHOULD NOT BE USED
#
#Created by: Thomas Rossi
################################################################################

use strict;
use warnings;

my $usageMsg = q(   Usage: fastaparse fastafile

          Extract each sequence from a fastafile into a single string.
          <do something to the sequence -- this one computes its length
          and adds it after the sequence name on the header>

          Output is the revised header and sequence data
          Output sent to standard output. );

#main
&checkUsage();              # comment this line if assigning file name above

my $seqFile = $ARGV[ 0 ];   # comment this line if assigning file name above
my $filename = "OUT-$seqFile";

open(OUTFILE, ">$filename");

open ( IN, $seqFile )  or die "Unable to open: ".$seqFile ;


# first line better be a sequence header
my $inLine = <IN>;

while ( $inLine )
{
   
   my @lineArr = split ('\|', $inLine);
   
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