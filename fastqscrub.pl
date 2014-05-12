#!/usr/bin/perl -w
################################################################################
#fastqscrub.pl:
#THIS FILE WAS SCRAPPED EARLY IN PIPELINE DEVELOPMENT AND WAS NOT COMPLETED
#IT SERVES NO PURPOSE IN OUR PIPELINE, WAS NOT DEBUGGED, AND SHOULD NOT BE USED
#
#Created by: Thomas Rossi
################################################################################

use strict;
use warnings;

my $usageMsg = q(   Usage: fastqscrub fastafile

          Extract each sequence from a fastq file into a single string along
          with the quality scores into another string.
          
          Take the first 130 letters from both strings, for the rest,
          find the sequence in the sequence that based on the quality scores
          results in an average >20.  Until this is found, keep loping bases off
          of the end of the string (and the quality score).

          Output is the revised header, sequence data, and score data
          Output sent to two files, one with the revised sequence and one
          with the "leftovers". );

# first line better be a sequence header
my $header = <IN>;
if ( substr( $header, 0, 1 ) ne '>' )
{
   print "********* ERROR ********* Expecting header, got:\n $header";
   print " is this a fasta file??? ";
   &checkUsage();
   exit;
}

while ( $header )
{
   my $seq = ""; 
   my $inLine = <IN>;

   # read in all input lines of bases
   while ( $inLine && substr( $inLine, 0, 1 ) ne '>' )
   {
      chomp( $inLine );     # remove line feed
      $seq = $seq . $inLine;
      $inLine = <IN>;
   }
   # -----------------------------------------------------
   #   Replace the lines below with the sequence specific
   #  processing you want to do.
   #
        chomp($header);
        print $header;
        print &dnaToAminoAcid($seq);
        print "\n\n";
   #--------------------------------------------------------
   $header = $inLine;    # last line read is either next header or null
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