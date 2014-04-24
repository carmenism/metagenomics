#!/usr/bin/env python
################################################################################
#rankComparison.py
################################################################################
import buildTaxonomy
import sqlite3

def getCommonAncestor(speciesList):
    level = 0
    keepLooking = True
    
    while keepLooking:
        (firstTaxid, firstName, firstRank) = speciesList[0][level]
        print firstTaxid, firstName, firstRank
        
        for otherSpecies in speciesList[1:]:
            (otherTaxid, otherName, otherRank) = otherSpecies[level]
            
            if otherTaxid != firstTaxid:
                keepLooking = False
                level = level - 1
                
        level = level + 1
        
        if level == len(buildTaxonomy.abbrRanks):
            keepLooking = False
            level = level - 1
    
    return speciesList[0][level]

conn = sqlite3.connect("Metagenomics.db")
cursor = conn.cursor()

speciesList = []

print buildTaxonomy.getAbbrTaxonomyFromTaxid(cursor, "58777")
#print speciesA
#speciesB = buildTaxonomy.getAbbrTaxonomyFromTaxid(cursor, "109777")
#print speciesB
#speciesList.append(speciesA)
#speciesList.append(speciesB)

#print getCommonAncestor(speciesList)

conn.commit()
conn.close()