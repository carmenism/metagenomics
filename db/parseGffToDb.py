#!/usr/bin/env python

import sqlite3
import string
import sys
import dbDef

attrGene = "gbkey=Gene"
attrGenome = "gbkey=Src"
attrGeneId = "Dbxref=GeneID:"
attrTaxId = "Dbxref=taxon:"

featureGenome = "region"
featureGene = "gene"

gffColumnSeqname = 0
gffColumnSource = 1
gffColumnFeature = 2
gffColumnStart = 3
gffColumnEnd = 4
gffColumnScore = 5
gffColumnStrand = 6
gffColumnFrame = 7
gffColumnAttr = 8

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
    
    cursor.execute(sql)
    
def addToGeneTable(cursor, ncID, geneID, start, stop):
    sql = "INSERT INTO " + dbDef.tblGene.name + " (" + dbDef.tblGene_col_ncid.name + ", " + dbDef.tblGene_col_gene_id.name + ", " + dbDef.tblGene_col_start.name + ", " + dbDef.tblGene_col_stop.name + ") VALUES('" + ncID + "', '" + geneID +"', "+ start + ", " + stop + ")"
    
    cursor.execute(sql)

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

lineNumber = 1

for line in f.readlines():
    if not isComment(line):
        try:
            tokens = line.split("\t")
            ncID = tokens[gffColumnSeqname]
            feature = tokens[gffColumnFeature]
            start = tokens[gffColumnStart]
            stop = tokens[gffColumnEnd]
            attributes = tokens[gffColumnAttr].split(";")
            
            if isGenome(feature):
                taxID = extractTaxID(attributes)
                
                if taxID is not None:
                    # MAKE AN ENTRY IN SPECIES TABLE
                    addToSpeciesTable(cursor, ncID, taxID)
                else:
                    msg = "Species is missing taxid, line " + str(lineNumber) + ": " + line
                    logFile.write(msg + "\n");
                    print msg;
            elif isGene(feature):
                geneID = extractGeneID(attributes)
                
                if geneID is not None:
                    # MAKE AN ENTRY IN GENE TABLE
                    addToGeneTable(cursor, ncID, geneID, start, stop)
                else:
                    msg = "Gene is missing geneid, line " + str(lineNumber) + ": " + line
                    logFile.write(msg + "\n");
                    print msg;
        except Error:
            msg = "Problem with line " + str(lineNumber) + ": " + line
            logFile.write(msg + "\n");
            print msg;
    lineNumber = lineNumber + 1

f.close()
logFile.close()

conn.commit()
conn.close()