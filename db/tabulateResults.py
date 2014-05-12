#!/usr/bin/env python
"""
======================
tabulateResults module
======================

Authors
-------
Thomas Rossi (trn5@unh.edu)
Carmen St. Jean (crr8@unh.edu)
    
Date
----
May 6, 2014
    
Abstract
--------
This module parses the BWA alignment results SAM file.  For each read, it looks
up the taxonomy of the best matched species and increments the count at each
level of that taxonomy.  A summary of the counts at each taxonomic level is
then printed to eight files:

    * taxResults_superkingdom.csv
    * taxResults_kingdom.csv
    * taxResults_phylum.csv
    * taxResults_class.csv
    * taxResults_order.csv
    * taxResults_family.csv
    * taxResults_genus.csv
    * taxResults_species.csv

Instructions
------------
To run this file, you first need to make sure the taxonomy, species, and gene
databases have been populated.  Run parseGffToDb.py and ncbiToDb.py to populate
them.

Next, run this script on the command line of a computer where Python is
installed with a command line argument specifying the BWA output, e.g.:

    ./tabulateResults.py bwaOutput.sam
    
If you have just added this file to your computer and this doesn't work,
then it may be necessary to change the permissions.  On Linux:

    chmod u+x tabulateResults.py
    
It is also necessary to have dbDef.py and buildTaxonomy.py in the same
directory.
"""
import sys
import buildTaxonomy
import sqlite3
import csv
import dbDef

conn = sqlite3.connect("Metagenomics.db")
cursor = conn.cursor()

# initialize the hashmap of tallies
organismCount = {}

class Tally:
    """
    Represents the number of times a specific entry at a rank (kingdom,
    phylum, class, etc.) has an alignment with a read.
    """
    def __init__(self, name, rank, tax):
        """
        Initializes an entry with a count of zero.
        
        Arguments:
            name -- The name of the entry.
            rank -- The rank (kingdom, phylum, class, etc.).
            tax -- The taxonomy ID.
        """
        self.count = 0
        self.name = name
        self.rank = rank
        self.taxid = tax
        
    def increaseCount(self):
        """
        Increases the count for this entry by one.
        """
        self.count = self.count + 1
        
    def toList(self):
        """
        Converts and returns the data represented in this Tally object to a
        list.
        """
        return [self.taxid, self.name, self.rank, self.count]

def getTaxidFromNCID(cursor, ncid):
    """
    Returns the taxonomy ID corresponding to the given NCBI ID.
    
    Arguments:
        cursor -- A cursor object pointing to the metagenomics SQLite database.
        ncid -- The NCBI identifier for the species, genus, family, etc.
    """
    sql = "SELECT " + dbDef.tblSpecies_col_tax_id.name + " FROM " + dbDef.tblSpecies.name + " WHERE " + dbDef.tblSpecies_col_ncid.name + " = '" + ncid + "';"
    
    return buildTaxonomy.getSingleFieldFromSql(cursor, sql)

def createLevelFile(level):
    """
    Creates the summary file for the given taxonomic level.
    
    Arguments:
        level -- A taxonomic level (e.g., kingdom, phylum, class, etc.).
    """
    totalCount = 0
    
    # create a file name
    levelFile = 'taxResults_' + level + '.csv'
    
    # initialize a list of IDs to delete to make the next level's processing
    # go faster
    taxidsToDelete = []
    
    # create a list of headers for the file
    tmpList = ["Taxid","Name","Rank","Count"]
    
    # open the output file
    with open(levelFile, 'wb') as levelCsv:
        # initialize the CSV writer for the file
        levelCsvWriter = csv.writer(levelCsv, delimiter=',', quotechar='"')
        levelCsvWriter.writerow(tmpList) # write the header line
        
        # iterate over the entire hashmap of counts
        for taxid, tally in organismCount.iteritems():
            # only include the entry in the report if it belongs to this
            # taxonomy level
            if tally.rank == level:
                # add the count to the total count
                totalCount = totalCount + tally.count
                
                # write to the CSV
                levelCsvWriter.writerow(tally.toList())
                
                # add the tax ID to the list of IDs to be deleted
                taxidsToDelete.append(taxid)
    
        # write a line with a total
        tmpList = ["TOTAL","",level,totalCount]
        levelCsvWriter.writerow(tmpList)
    
    # delete the taxids that are no longer needed 
    for taxid in taxidsToDelete:
        del organismCount[taxid]
    
    return

# open the log file in case we need to record problems
logFile = open("tabulateResults.log", "w") 
   
# check for a command line argument
if len(sys.argv) == 1:
    print "This program requires a file to run"

filename = sys.argv[1]

readFile = open(filename, 'r')

# read each line ('read') in the BWA ouput file
for line in readFile.readlines():
    # tokenize the line
    tokens = line.split("\t")
    
    # extract the NCBI ID from the tokens
    ncid = tokens[1]
    
    # get the taxonomy ID for the species
    readTaxID = getTaxidFromNCID(cursor, ncid)
    
    # write to the log and continue if there is no taxonomy ID for that NCID
    if readTaxID is None:
        logFile.write("Problem with line: " + line)
        continue
    
    # get the abbreviated taxonomy for that taxonomy ID
    taxonomy = buildTaxonomy.getAbbrTaxonomyFromTaxid(cursor, readTaxID)
    
    # for each level of taxonomy, add one to its count
    for level in taxonomy: 
        (taxid, name, rank) = level
        
        # if there is no entry in the hashmap, add one
        if taxid not in organismCount:
            organismCount[taxid] = Tally(name, rank, taxid)
        
        # increment the count
        organismCount[taxid].increaseCount()

readFile.close()

# create the results file for each taxonomy level
for level in buildTaxonomy.abbrRanks:
    createLevelFile(level)

conn.commit()
conn.close()

logFile.close()