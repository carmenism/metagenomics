#!/usr/bin/env python
"""
=====================
rankComparison module
=====================

Authors
-------
Thomas Rossi (trn5@unh.edu)
Carmen St. Jean (crr8@unh.edu)
    
Date
----
April 28, 2014
    
Abstract
--------
This module finds the lowest common ancestor between a list of species.  This
code did not end up in our final pipeline.

Instructions
------------
To run this file, you first need to make sure the taxonomy table is populated
by running ncbiToDb.py on a computer which has python installed.

Next, run this script on the command line of a computer where Python is
installed with a command line argument specifying the BWA output, e.g.:

    ./rankComparison.py 
    
If you have just added this file to your computer and this doesn't work,
then it may be necessary to change the permissions.  On Linux:

    chmod u+x rankComparison.py
    
It is also necessary to have buildTaxonomy.py in the same directory.
"""
import buildTaxonomy
import sqlite3

def getCommonAncestor(speciesList):
    """
    Returns the lowest common ancestor between the specified species.
    
    Arguments:
        speciesList -- A list of species taxonomies.
    """
    level = 0
    keepLooking = True
    
    while keepLooking:
        (firstTaxid, firstName, firstRank) = speciesList[0][level]
        print firstTaxid, firstName, firstRank
        
        for otherSpecies in speciesList[1:]:
            (otherTaxid, otherName, otherRank) = otherSpecies[level]
            
            if otherTaxid != firstTaxid:
                return speciesList[0][level - 1]
                
        level = level + 1
        
        if level == len(buildTaxonomy.abbrRanks):
            keepLooking = False
            level = level - 1
    
    return speciesList[0][level]

conn = sqlite3.connect("Metagenomics.db")
cursor = conn.cursor()

speciesList = []

print buildTaxonomy.isPartOfAbbreviatedRank("genus")

speciesA =  buildTaxonomy.getAbbrTaxonomyFromTaxid(cursor, "58777")
print speciesA
speciesB = buildTaxonomy.getAbbrTaxonomyFromTaxid(cursor, "109777")
print speciesB

speciesList.append(speciesA)
speciesList.append(speciesB)

print getCommonAncestor(speciesList)

conn.commit()
conn.close()