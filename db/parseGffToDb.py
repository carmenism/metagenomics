#!/usr/bin/env python
"""
===================
parseGffToDb module
===================

Authors
-------
Thomas Rossi (trn5@unh.edu)
Carmen St. Jean (crr8@unh.edu)
    
Date
----
May 6, 2014
    
Abstract
--------
This module parses the reference file (containing the genomes for our BWA
alignment) and inserts the data into the species and gene tables of the
metagenomics database.

Instructions
------------
To populate the species and gene tables, run this script on the command line
of a computer where Python is installed.  The name of the reference file should
be specified as a command line argument, e.g.:

    ./parseGffToDb.py referenceFile.rgff
    
If you have just added this file to your computer and this doesn't work,
then it may be necessary to change the permissions.  On Linux:

    chmod u+x parseGffToDb.py
    
It is also necessary to have dbDef.py in the same directory.
"""
import sqlite3
import string
import sys
import dbDef

# the meaning of the columns in the GFF reference file
gffColumnTaxId = 0
gffColumnRefId = 1
gffColumnStart = 2
gffColumnEnd = 3
gffColumnGeneId = 4
gffColumnProteinId = 5
gffColumnProduct = 6
gffColumnGoNumbers = 7

def isComment(line):
    """
    Returns true if the line of text is a comment line (i.e., begins with '#').
    
    Arguments:
        line -- The line of text to be tested.
    """
    return line.startswith("#")

def addToSpeciesTable(cursor, ncID, taxID):
    """
    Adds an entry to the species table.
    
    Arguments:
        cursor -- A cursor pointing to the metagenomics SQLite database.
        ncID -- The NCBI indentifier of the species.
        taxID -- The taxonomy identifier of the species.
    """
    sql = "INSERT INTO " + dbDef.tblSpecies.name + " (" + dbDef.tblSpecies_col_ncid.name + ", " + dbDef.tblSpecies_col_tax_id.name + ") VALUES('" + ncID + "', '" + taxID +"')"
    
    try:
        cursor.execute(sql)
    except sqlite3.IntegrityError:
        return False
    
    return True
    
def addToGeneTable(cursor, ncID, geneID, start, stop):
    """
    Adds an entry to the gene table.
    
    Arguments:
        cursor -- A cursor pointing to the metagenomics SQLite database.
        ncID -- The NCBI indentifier of the species the gene is from.
        geneID -- The gene ID.
        start -- The starting position of the gene in the species' genome.
        stop -- The end position of the gene in the species' genome.
    """
    sql = "INSERT INTO " + dbDef.tblGene.name + " (" + dbDef.tblGene_col_ncid.name + ", " + dbDef.tblGene_col_gene_id.name + ", " + dbDef.tblGene_col_start.name + ", " + dbDef.tblGene_col_stop.name + ") VALUES('" + ncID + "', '" + geneID +"', "+ start + ", " + stop + ")"
    
    try:
        cursor.execute(sql)
    except sqlite3.IntegrityError:
        return False
    
    return True

def writeToLog(logfile, message):
    """
    Writes the message to the log and standard output.
    
    Arguments:
        logfile -- The logfile object.
        message -- The message to be written.
    """
    print message
    logfile.write(message)

# check the command line argument for the reference filename
if (len(sys.argv) <= 1):
    print "Please specify a reference filename as a command line argument."
    exit(1)

referenceFilename = sys.argv[1]

# start a connection to the database
conn = sqlite3.connect("Metagenomics.db")
cursor = conn.cursor()

# drop the tables
dbDef.dropTable(cursor, dbDef.tblSpecies)
dbDef.dropTable(cursor, dbDef.tblGene)

# create the tables
dbDef.createTable(cursor, dbDef.tblSpecies)
dbDef.createTable(cursor, dbDef.tblGene)

# open the reference file
f = open(referenceFilename, "r") # eg "NC_017911.gff"

# open the log file to keep track of problems
logFile = open("dbCreationFile.log", "w")

# initialize some statistics stuff
lineNumber = 0
successGene = 0
successSpecies = 0
duplicateGene = 0
duplicateSpecies = 0
missingAttrGene = 0
missingAttrSpecies = 0
problemLines = 0

# read and parse each line of the reference file
for line in f.readlines():
    # make sure to only process non-comment lines
    if not isComment(line):
        lineNumber = lineNumber + 1
        
        try:
            # parse the tokens and extract the information
            tokens = line.split("\t")
            ncID = tokens[gffColumnRefId]
            taxID = tokens[gffColumnTaxId]
            start = tokens[gffColumnStart]
            stop = tokens[gffColumnEnd]
            geneID = tokens[gffColumnGeneId]
            
            if taxID is not None:
                # MAKE AN ENTRY IN SPECIES TABLE
                success = addToSpeciesTable(cursor, ncID, taxID)
                
                if success:
                    successSpecies = successSpecies + 1
                else:
                    writeToLog(logFile, "Species duplicate, line " + str(lineNumber) + ": " + line)
                    duplicateSpecies = duplicateSpecies + 1
                
            if geneID is not None:
                # MAKE AN ENTRY IN GENE TABLE
                success = addToGeneTable(cursor, ncID, geneID, start, stop)
                
                if success:
                    successGene = successGene + 1
                else:
                    writeToLog(logFile, "Gene duplicate, line " + str(lineNumber) + ": " + line)
                    duplicateGene = duplicateGene + 1
        except IndexError:
            # an error occured, so write it to the log file
            writeToLog(logFile, "Problem with line " + str(lineNumber) + ": " + line)
            problemLines = problemLines + 1

print "Non comment lines: " + str(lineNumber)
print "Problem lines: " + str(problemLines)
print "Success genes: " + str(successGene)
print "Success species: " + str(successSpecies)
print "Duplicate genes: " + str(duplicateGene)
print "Duplicate species: " + str(duplicateSpecies)
print "Genes missing attributes: " + str(missingAttrGene)
print "Species missing attributes: " + str(missingAttrSpecies)

f.close()
logFile.close()

conn.commit()
conn.close()