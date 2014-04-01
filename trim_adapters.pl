#!/usr/bin/perl -w
#
# For each adapter in the adapter file, make one-fourth and one-half fragments.
#
# Friday March 14, 2014
#
my $usageMsg = q( Usage: trim_adapters adapters_file  );

use warnings;
use strict;

&checkUsage();

my $adaptFile = $ARGV[ 0 ];

open ( IN, $adaptFile )  or die "Unable to open: $adaptFile";

# first line better be a sequence header
my $header = <IN>;
if ( substr( $header, 0, 1 ) ne '>' ) {
    print "********* ERROR ********* Expecting header, got:\n $header";
    print " is this a fasta file??? ";
    &checkUsage();
    exit;
}

my $outFileName = "$adaptFile.out";
my $OUTFILE;
open $OUTFILE, "> $outFileName" or die "Error opening $outFileName: $!";

while ( $header ) {
    my $adapter = ""; 
    my $inLine = <IN>;
    
    # read in all input lines of bases
    while ( $inLine && substr( $inLine, 0, 1 ) ne '>' ) {
        chomp( $inLine );     # remove line feed
        $adapter = $adapter . $inLine;
        $inLine = <IN>;
    }
    
    chomp( $header );
    
    my $length = length($adapter);
    my $half = int($length / 2);
    my $fourth = int($length / 4);
    
    my $half1 = substr($adapter, 0, $half);
    my $half2 = substr($adapter, $half);
    
    my $lengthHalf1 = length($half1);
    my $lengthHalf2 = length($half2);
    
    my $fourth1 = substr($half1, 0, $lengthHalf1 / 2);
    my $fourth2 = substr($half1, $lengthHalf1 / 2);
    
    my $fourth3 = substr($half2, 0, $lengthHalf2 / 2);
    my $fourth4 = substr($half2, $lengthHalf2 / 2);
    
    if ($fourth1 . $fourth2 . $fourth3 . $fourth4 ne $adapter) {
        print "************ ERROR dividing adapter into fourths\n";
    }
    
    if ($half1 . $half2 ne $adapter) {
        print "************ ERROR dividing adapter into halves\n";
    }
    
    print{$OUTFILE} "$header\n";
    print{$OUTFILE} "$adapter\n";
    
    print{$OUTFILE} "$header, Half 1 \n";
    print{$OUTFILE} "$half1\n";
    
    print{$OUTFILE} "$header, Half 2 \n";
    print{$OUTFILE} "$half2\n";
    
    print{$OUTFILE} "$header, Fourth 1\n";
    print{$OUTFILE} "$fourth1\n";
    
    print{$OUTFILE} "$header, Fourth 2\n";
    print{$OUTFILE} "$fourth2\n";
    
    print{$OUTFILE} "$header, Fourth 3\n";
    print{$OUTFILE} "$fourth3\n";
    
    print{$OUTFILE} "$header, Fourth 4\n";
    print{$OUTFILE} "$fourth4\n";
   
    $header = $inLine;    # last line read is either next header or null
}

close $OUTFILE;

sub checkUsage() {
    if ( @ARGV == 0 || $ARGV[0] eq "-h" ) {
        print STDERR "$usageMsg\n";
        exit;
    }
}