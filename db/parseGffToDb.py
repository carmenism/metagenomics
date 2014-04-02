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

tblSpecies = "tblSpecies"
tblSpecies_ncid = "ncid"
tblSpecies_tax_id = "tax_id"
tblSpecies_taxonomy = "taxonomy"

tblGene = "tblGene"
tblGene_ncid = "ncid"
tblGene_gene_id = "gene_id"
tblGene_start = "start"
tblGene_stop = "stop"
tblGene_function = "function"

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
    sql = "INSERT INTO " + tblSpecies + " (" + tblSpecies_ncid + ", " + tblSpecies_tax_id + ") VALUES('" + ncID + "', '" + taxID +"')"
    
    cursor.execute(sql)
    
def addToGeneTable(cursor, ncID, geneID, start, stop):
    sql = "INSERT INTO " + tblGene + " (" + tblGene_ncid + ", " + tblGene_gene_id + ", " + tblGene_start + ", " + tblGene_stop + ") VALUES('" + ncID + "', '" + geneID +"', "+ start + ", " + stop + ")"
    
    cursor.execute(sql)
    
def dropTable(cursor, tableName):
    sql = "DROP TABLE IF EXISTS " + tableName

    cursor.execute(sql)
    
def createSpeciesTable(cursor):
    sql = "CREATE TABLE " + tblSpecies + " (" + tblSpecies_ncid + " VARCHAR(20) PRIMARY KEY, " + tblSpecies_tax_id + " VARCHAR(14), " + tblSpecies_taxonomy + " VARCHAR(2500) ) WITHOUT ROWID "

    print sql
    cursor.execute(sql)
    
def createGeneTable(cursor):
    sql = "CREATE TABLE " + tblGene + " (" + tblGene_ncid + " VARCHAR(20), " + tblGene_gene_id + " VARCHAR(14), " + tblGene_start + " INT, " + tblGene_stop + " INT, " + tblGene_function + " VARCHAR(2500), PRIMARY KEY(" + tblGene_ncid + ", " + tblGene_gene_id + ") ) WITHOUT ROWID "

    print sql
    cursor.execute(sql)

print sqlite3.sqlite_version

conn = sqlite3.connect("Metagenomics.db")
cursor = conn.cursor()

dropTable(cursor, tblSpecies)
dropTable(cursor, tblGene)

createSpeciesTable(cursor)
createGeneTable(cursor)

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