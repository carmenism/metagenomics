#!/usr/bin/env python

import os
import os.path
import urllib
import zipfile
import dbDef
import sqlite3

taxdmpZip = 'taxdmp.zip'
nodesFilename = 'nodes.dmp'
namesFilename = 'names.dmp'

nodesDmpTaxid = 0
nodesDmpParentTaxid = 1
nodesDmpTaxRank = 2

namesDmpTaxid = 0
namesDmpName = 1
namesDmpNameClass = 3

def addToTaxonomyTable(cursor, taxID, taxRank, parentTaxID):
    sql = "INSERT INTO " + dbDef.tblTaxonomy.name + " (" + dbDef.tblTaxonomy_col_tax_id.name + ", " + dbDef.tblTaxonomy_col_tax_rank.name + ", " + dbDef.tblTaxonomy_col_parent_tax_id.name + ") VALUES('" + taxID + "', '" + taxRank + "', '" + parentTaxID + "')"
    
    cursor.execute(sql)
    
def updateName(cursor, taxID, taxName):
    taxName = taxName.replace("'", "''")
    sql = "UPDATE " + dbDef.tblTaxonomy.name + " SET " + dbDef.tblTaxonomy_col_tax_name.name + " = '" + taxName + "' WHERE " + dbDef.tblTaxonomy_col_tax_id.name + " = '" + taxID + "'"
    print sql;
    cursor.execute(sql)

#urllib.urlretrieve('ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdmp.zip', taxdmpZip)

zfile = zipfile.ZipFile(taxdmpZip)

zfile.extract(nodesFilename, "")
zfile.extract(namesFilename, "")

conn = sqlite3.connect("Metagenomics.db")
cursor = conn.cursor()

dbDef.dropTable(cursor, dbDef.tblTaxonomy)
dbDef.createTable(cursor, dbDef.tblTaxonomy)

fNode = open(nodesFilename, 'r')

for line in fNode.readlines():
    tokens = line.split("|")
    tokens = [t.strip() for t in tokens]
    
    taxid = tokens[nodesDmpTaxid]
    parentTaxid = tokens[nodesDmpParentTaxid]
    taxRank = tokens[nodesDmpTaxRank]
    
    addToTaxonomyTable(cursor, taxid, taxRank, parentTaxid)
    
fNode.close()

fName = open(namesFilename, 'r')

for line in fName.readlines():
    tokens = line.split("|")
    tokens = [t.strip() for t in tokens]
    
    taxid = tokens[namesDmpTaxid]
    name = tokens[namesDmpName]
    nameClass = tokens[namesDmpNameClass]
    
    if nameClass == 'scientific name':
        updateName(cursor, taxid, name)
    
fName.close()

conn.commit()
conn.close()