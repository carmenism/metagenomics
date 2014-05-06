#!/usr/bin/env python
################################################################################
#tabulateResults.py
################################################################################
import sys
import buildTaxonomy
import sqlite3
import csv
import dbDef

conn = sqlite3.connect("Metagenomics.db")
cursor = conn.cursor()

organismCount = {}

filename = sys.argv[1]

readFile = open(filename, 'r')

class Tally:
    def __init__(self, name, rank, tax):
        self.count = 0
        self.name = name
        self.rank = rank
        self.taxid = tax
        
    def increaseCount(self):
        self.count = self.count + 1
        
    def toList(self):
        return [self.taxid, self.name, self.rank, self.count]

    def toListAddGenus(self, genus):
        return [self.taxid, genus + " " + self.name, self.rank, self.count]

def getTaxidFromNCID(cursor, ncid):
    sql = "SELECT " + dbDef.tblSpecies_col_tax_id.name + " FROM " + dbDef.tblSpecies.name + " WHERE " + dbDef.tblSpecies_col_ncid.name + " = '" + ncid + "';"
    
    return buildTaxonomy.getSingleFieldFromSql(cursor, sql)

def createLevelFile(level):
    totalCount = 0
    
    levelFile = 'taxResults_' + level + '.csv'
    taxidsToDelete = []
    
    tmpList = ["Taxid","Name","Rank","Count"]
    
    with open(levelFile, 'wb') as levelCsv:
        levelCsvWriter = csv.writer(levelCsv, delimiter=',', quotechar='"')
        levelCsvWriter.writerow(tmpList)
        
        for taxid, tally in organismCount.iteritems():
            if tally.rank == level:
                totalCount = totalCount + tally.count
                levelCsvWriter.writerow(tally.toList())
                
                taxidsToDelete.append(taxid)
    
        tmpList = ["TOTAL","",level,totalCount]
        levelCsvWriter.writerow(tmpList)
                
    #for taxid in taxidsToDelete:
    #    del organismCount[taxid]
    
    return
 
   
if len(sys.argv) == 1:
    print "This program requires a file to run"

for line in readFile.readlines():
    #get the tax id for the species
    tokens = line.split("\t")
    ncid = tokens[1]
    readTaxID = getTaxidFromNCID(cursor, ncid)
    
    #locate in hash map and add one
    taxonomy = buildTaxonomy.getAbbrTaxonomyFromTaxid(cursor, readTaxID)
    
    #for each level of taxonomy, add one to its count
    for level in taxonomy: # iterate over all but last item
        (taxid, name, rank) = level
        
        if readTaxID == '991903':
            print taxid + " " + name + " " + rank + " "

        if taxid not in organismCount:
            organismCount[taxid] = Tally(name, rank, taxid)
        
        organismCount[taxid].increaseCount()

readFile.close()

for level in buildTaxonomy.abbrRanks:
    createLevelFile(level)

conn.commit()
conn.close()