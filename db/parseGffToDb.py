#!/usr/bin/env python

import sqlite3
import string
import sys
import dbDef

gffColumnTaxId = 0
gffColumnRefId = 1
gffColumnStart = 2
gffColumnEnd = 3
gffColumnGeneId = 4
gffColumnProteinId = 5
gffColumnProduct = 6
gffColumnGoNumbers = 7

def isComment(line):
    return line.startswith("#")

def isGene(feature):
    return feature == featureGene

def isGenome(feature):
    return feature == featureGenome

def extractGeneID(attributes):
    for attribute in attributes:
        if attrGeneId in attribute:
            return attribute[len(attrGeneId):]
        
    return None

def extractTaxID(attributes):
    for attribute in attributes:
        if attrTaxId in attribute:
            return attribute[len(attrTaxId):]
        
    return None

def addToSpeciesTable(cursor, ncID, taxID):
    sql = "INSERT INTO " + dbDef.tblSpecies.name + " (" + dbDef.tblSpecies_col_ncid.name + ", " + dbDef.tblSpecies_col_tax_id.name + ") VALUES('" + ncID + "', '" + taxID +"')"
    
    try:
        cursor.execute(sql)
    except sqlite3.IntegrityError:
        return False
    
    return True
    
def addToGeneTable(cursor, ncID, geneID, start, stop):
    sql = "INSERT INTO " + dbDef.tblGene.name + " (" + dbDef.tblGene_col_ncid.name + ", " + dbDef.tblGene_col_gene_id.name + ", " + dbDef.tblGene_col_start.name + ", " + dbDef.tblGene_col_stop.name + ") VALUES('" + ncID + "', '" + geneID +"', "+ start + ", " + stop + ")"
    
    try:
        cursor.execute(sql)
    except sqlite3.IntegrityError:
        return False
    
    return True

def writeToLog(logfile, message):
    print message
    logfile.write(message)

if (len(sys.argv) <= 1):
    print "Please specify a reference filename as a command line argument."
    exit(1)

referenceFilename = sys.argv[1]

print sqlite3.sqlite_version

conn = sqlite3.connect("Metagenomics.db")
cursor = conn.cursor()

dbDef.dropTable(cursor, dbDef.tblSpecies)
dbDef.dropTable(cursor, dbDef.tblGene)

dbDef.createTable(cursor, dbDef.tblSpecies)
dbDef.createTable(cursor, dbDef.tblGene)

f = open(referenceFilename, "r") # eg "NC_017911.gff"

logFile = open("dbCreationFile.log", "w")

lineNumber = 0
successGene = 0
successSpecies = 0
duplicateGene = 0
duplicateSpecies = 0
missingAttrGene = 0
missingAttrSpecies = 0
problemLines = 0

for line in f.readlines():
    if not isComment(line):
        lineNumber = lineNumber + 1
        
        try:
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