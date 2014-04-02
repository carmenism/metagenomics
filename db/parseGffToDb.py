#!/usr/bin/env python

import sqlite3
import string

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

tableSpecies = "Species"
tableGene = "Gene"

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
    sql = "INSERT INTO " + tableSpecies + " (NCID, TaxID) VALUES('" + ncID + "', '" + taxID +"')"
    
    cursor.execute(sql)
    
def addToGeneTable(cursor, ncID, geneID, start, stop):
    sql = "INSERT INTO " + tableGene + " (NCID, geneID, start, stop) VALUES('" + ncID + "', '" + geneID +"', "+ start + ", " + stop + ")"
    
    cursor.execute(sql)
    
conn = sqlite3.connect("something.db")
cursor = conn.cursor()

f = open("NC_017911.gff")

for line in f.readlines():
    if not isComment(line):
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
        elif isGene(feature):
            geneID = extractGeneID(attributes)
            
            if geneID is not None:
                # MAKE AN ENTRY IN GENE TABLE
                addToGeneTable(cursor, ncID, geneID, start, stop)

conn.commit()
conn.close()