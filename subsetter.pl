## Purpose: To subset the first (user-defined #) of entries from a very large FASTQ file
## For a metagenomics group project in the course MCBS 913: Applied Bioinformatics
## Group: Mark Anthony, Gloria Broders, Amanda Daly, Liz Landis, Simon Ogbamichael, and Carmen St. Jean
## Affiliation: University of New Hampshire
## Author: Amanda B. Daly
## Date: Feb 21, 2014

use strict;
use warnings;
my ($num, $infile, $outfile, $header, $seq, $id, $qual, @subset, $count);

print "Welcome to the FASTQ subsetter!\n";
print "How many entries would you like to grab?: ";
chomp ($num = <STDIN>);
print "Enter the name of the FASTQ file to be subsetted: ";
chomp ($infile = <STDIN>);
print "Choose a name for the ", $num, "-entry subset FASTQ output file: ";
chomp ($outfile = <STDIN>);

open(RAW, "<", $infile);

$count = 1;
while($count <= $num)       # Cycle through user-defined # of entries
{
	$header = <RAW>;        # Take first four lines from file
	$seq = <RAW>;
	$id = <RAW>;
	$qual = <RAW>;
	push (@subset, ($header, $seq, $id, $qual)); # Then them to an array to be printed later
	++$count;
}
close RAW;

open(OUT, ">", $outfile);
print OUT @subset;          # Print the subset to the output file
close OUT;

__END__