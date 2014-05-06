#!/usr/bin/env python
################################################################################
#tabulateResults.py
################################################################################
import sys
import buildTaxonomy
import sqlite3
import csv

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
        return [self.taxid, self.name, self.rank, self.count, self.countChild]

    def toListAddGenus(self, genus):
        return [self.taxid, genus + " " + self.name, self.rank, self.count, self.countChild]

def createGenusSpeciesFile():
    genusSpeciesFile = filename + '_speciesGenus.csv'
    taxidsToDelete = []
    
    with open(genusSpeciesFile, 'wb') as genusSpeciesCsv:
        genusSpeciesCsvWriter = csv.writer(genusSpeciesCsv, delimiter=',', quotechar='"')
        
        for taxid, tally in organismCount.iteritems():
            if tally.rank == buildTaxonomy.abbrRanks[-1]: #if rank is species
                genusTax = getParentTaxidFromTaxid(cursor, taxid)
                
                genusName = organismCount[genusTax].name
                genusSpeciesCsvWriter.writeRow(tally.toListAddGenus(genusName))
                
                taxidsToDelete.append(taxid)
                
    for taxid in taxidsToDelete:
        del organismCount[taxid]
    
    return
 
def createTaxonomyFile():
    
    return
 
        
if len(sys.argv) == 1:
    print "This program requires a file to run"

for line in readFile.readlines():
    #get the tax id for the species
    readTaxID = '123'
    
    #locate in hash map and add one
    taxonomy = getAbbrTaxonomyFromTaxid(cursor, readTaxID)
    
    #for each level of taxonomy, add one to its count
    for level in taxonomy: # iterate over all but last item
        (taxid, name, rank) = level
        
        if taxid not in organismCount:
            organismCount[taxid] = Tally(name, rank, taxid)
        
        organismCount[taxid].increaseCount()

readFile.close()