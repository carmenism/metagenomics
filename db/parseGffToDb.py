#!/usr/bin/env python

import sqlite3
import string
import sys

class ColumnDefinition:
    def __init__(self, col_name, col_type):
        self.name = col_name
        self.type = col_type
        
    def createString(self):
        return self.name + " " + self.type

class TableDefinition:
    def __init__(self, table_name, table_cols, table_primary_key = None):
        self.name = table_name
        self.cols = table_cols
        self.primary_key = table_primary_key
        
    def createString(self):
        colStr = ", ".join([col.createString() for col in self.cols])
        
        createStr = "CREATE TABLE " + self.name + " (" + colStr + " "
        
        if self.primary_key is not None:
            return createStr + ", " + self.primary_key + ")"
        
        return createStr + ")"
    
    def dropString(self):
        return "DROP TABLE IF EXISTS " + self.name

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

tblSpecies_col_ncid = ColumnDefinition("ncid", "VARCHAR(20) PRIMARY KEY")
tblSpecies_col_tax_id = ColumnDefinition("tax_id", "VARCHAR(14)")
tblSpecies_col_tax_rank = ColumnDefinition("tax_rank", "VARCHAR(40)")
tblSpecies_col_parent_tax_id = ColumnDefinition("parent_tax_id", "VARCHAR(14)")
tblSpecies_cols = [tblSpecies_col_ncid, tblSpecies_col_tax_id, tblSpecies_col_tax_rank, tblSpecies_col_parent_tax_id]
tblSpecies = TableDefinition("tblSpecies", tblSpecies_cols)

tblGene_col_ncid = ColumnDefinition("ncid", "VARCHAR(20)")
tblGene_col_gene_id = ColumnDefinition("gene_id", "VARCHAR(14)")
tblGene_col_start = ColumnDefinition("start", "INT")
tblGene_col_stop = ColumnDefinition("stop", "INT")
tblGene_col_function = ColumnDefinition("function", "VARCHAR(2500)")
tblGene_col_cog_id = ColumnDefinition("cog_id", "VARCHAR(20)")
tblGene_cols = [tblGene_col_ncid, tblGene_col_gene_id, tblGene_col_start, tblGene_col_stop, tblGene_col_function, tblGene_col_cog_id]
tblGene = TableDefinition("tblGene", tblGene_cols, "PRIMARY KEY(" + tblGene_col_ncid.name + ", " + tblGene_col_gene_id.name + ")")

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
    sql = "INSERT INTO " + tblSpecies.name + " (" + tblSpecies_col_ncid.name + ", " + tblSpecies_col_tax_id.name + ") VALUES('" + ncID + "', '" + taxID +"')"
    
    cursor.execute(sql)
    
def addToGeneTable(cursor, ncID, geneID, start, stop):
    sql = "INSERT INTO " + tblGene.name + " (" + tblGene_col_ncid.name + ", " + tblGene_col_gene_id.name + ", " + tblGene_col_start.name + ", " + tblGene_col_stop.name + ") VALUES('" + ncID + "', '" + geneID +"', "+ start + ", " + stop + ")"
    
    cursor.execute(sql)
    
def dropTable(cursor, table):
    sql = table.dropString()

    cursor.execute(sql)
    
def createTable(cursor, table):
    sql = table.createString()

    print sql
    cursor.execute(sql)

if (len(sys.argv) >= 1):
    print "Please specify a reference filename as a command line argument."
    exit(1)

referenceFilename = sys.argv[1]

print sqlite3.sqlite_version

conn = sqlite3.connect("Metagenomics.db")
cursor = conn.cursor()

dropTable(cursor, tblSpecies)
dropTable(cursor, tblGene)

createTable(cursor, tblSpecies)
createTable(cursor, tblGene)

f = open(referenceFilename) # eg "NC_017911.gff"

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