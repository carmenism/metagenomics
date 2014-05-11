#!/usr/bin/env python
"""
==================
ncbiTaxToDb module
==================

Authors
-------
Thomas Rossi (trn5@unh.edu)
Carmen St. Jean (crr8@unh.edu)
    
Date
----
April 24, 2014
    
Abstract
--------
This module downloads and parses the NCBI taxonomy file to insert the data
into the taxonomy table of the metagenomics database.

Instructions
------------
To populate the taxonomy database, run this file on the command line of a
computer where Python is installed:

    ./ncbiTaxToDb.py
    
If you have just added this file to your computer and this doesn't work,
then it may be necessary to change the permissions.  On Linux:

    chmod u+x ncbiTaxToDb.py
    
It is also necessary to have the dbDef.py file in the same directory.
"""
import os
import os.path
import urllib
import zipfile
import dbDef
import sqlite3

taxdmpZip = 'taxdmp.zip' # the name of the zip file downloaded from NCBI
nodesFilename = 'nodes.dmp' # the file in the zip with the parent information
namesFilename = 'names.dmp' # the file in the zip with the name information

# the meaning of the columns in nodes.dmp
nodesDmpTaxid = 0
nodesDmpParentTaxid = 1
nodesDmpTaxRank = 2

# the meaning of the columns in names.dmp
namesDmpTaxid = 0
namesDmpName = 1
namesDmpNameClass = 3

def addToTaxonomyTable(cursor, taxID, taxRank, parentTaxID):
    """
    Adds an entry in the taxonomy table with the specified information.
    
    Arguments:
        cursor -- An sqlite cursor pointing to the metagenomics database.
        taxID -- The taxonomy ID of a species, genus, family, etc.
        taxRank -- A taxonomy rank such as species, genus, family, etc.
        parentTaxID -- The taxonomy ID of the "parent" node.
    """
    sql = "INSERT INTO " + dbDef.tblTaxonomy.name + " (" + dbDef.tblTaxonomy_col_tax_id.name + ", " + dbDef.tblTaxonomy_col_tax_rank.name + ", " + dbDef.tblTaxonomy_col_parent_tax_id.name + ") VALUES('" + taxID + "', '" + taxRank + "', '" + parentTaxID + "')"
    
    cursor.execute(sql)
    
def updateName(cursor, taxID, taxName):
    """
    Updates the name of the existing taxonomy entry with the specified taxonomy
    ID.
    
    Arguments:
        cursor -- An sqlite cursor pointing to the metagenomics database.
        taxID -- The taxonomy ID of a species, genus, family, etc.
        taxName -- The name of the taxonomy level.
    """
    taxName = taxName.replace("'", "''")
    sql = "UPDATE " + dbDef.tblTaxonomy.name + " SET " + dbDef.tblTaxonomy_col_tax_name.name + " = '" + taxName + "' WHERE " + dbDef.tblTaxonomy_col_tax_id.name + " = '" + taxID + "'"
    print sql;
    cursor.execute(sql)

# download the taxonomy information from the NCBI FTP server
urllib.urlretrieve('ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdmp.zip', taxdmpZip)

# open the zip archive
zfile = zipfile.ZipFile(taxdmpZip)
zfile.extract(nodesFilename, "")
zfile.extract(namesFilename, "")

# create a connection to the database
conn = sqlite3.connect("Metagenomics.db")
cursor = conn.cursor()

# drop and recreate the taxonomy table
dbDef.dropTable(cursor, dbDef.tblTaxonomy)
dbDef.createTable(cursor, dbDef.tblTaxonomy)

# open the nodes.dmp file
fNode = open(nodesFilename, 'r')

# parse each line of nodes.dmp
for line in fNode.readlines():
    # tokenize the line from the file
    tokens = line.split("|")
    tokens = [t.strip() for t in tokens]
    
    # extract the information from the tokens
    taxid = tokens[nodesDmpTaxid]
    parentTaxid = tokens[nodesDmpParentTaxid]
    taxRank = tokens[nodesDmpTaxRank]
    
    addToTaxonomyTable(cursor, taxid, taxRank, parentTaxid)
    
fNode.close()

# open the names.dmp file 
fName = open(namesFilename, 'r')

# parse each line of the names.dmp file
for line in fName.readlines():
    # tokenize the line from the file
    tokens = line.split("|")
    tokens = [t.strip() for t in tokens]
    
    # extract the information from the tokens
    taxid = tokens[namesDmpTaxid]
    name = tokens[namesDmpName]
    nameClass = tokens[namesDmpNameClass]
    
    # only add the name if it is a scientific name
    if nameClass == 'scientific name':
        updateName(cursor, taxid, name)
    
fName.close()

conn.commit()
conn.close()