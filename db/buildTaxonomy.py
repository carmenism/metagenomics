#!/usr/bin/env python
"""
====================
buildTaxonomy module
====================

Authors
-------
Thomas Rossi (trn5@unh.edu)
Carmen St. Jean (crr8@unh.edu)
    
Date
----
May 6, 2014
    
Abstract
--------
This module allows for easy retrieval of the abbreviated taxonomy for a
taxonomy ID from the taxonomy database based on the NCBI taxonomy.
"""
import dbDef
import sqlite3

abbrRanks = ["superkingdom", "kingdom", "phylum", "class", "order", "family", "genus", "species"]

def getSingleFieldFromSql(cursor, sql):
    """
    Executes an SQLite expression and tries to return a single result as a string.
    
    Arguments:
        cursor -- A cursor pointing to the metagenomics SQLite database.
        sql -- An SQLite expression to execute.
    """
    try:
        cursor.execute(sql)
        
        cursorResult = cursor.fetchone()
        
        if cursorResult is None:
            return None
        
        data = str(cursorResult[0])
        
        return data
    except sqlite3.Error:
        return None

def getNameFromTaxid(cursor, taxid):
    """
    Returns the name which matches the given taxonomy ID.
    
    Arguments:
        cursor -- A cursor pointing to the metagenomics SQLite database.
        taxid -- The taxonomy ID for a species, genus, family, etc.
    """
    sql = "SELECT " + dbDef.tblTaxonomy_col_tax_name.name + " FROM " + dbDef.tblTaxonomy.name + " WHERE " + dbDef.tblTaxonomy_col_tax_id.name + " = '" + taxid + "';"
    
    return getSingleFieldFromSql(cursor, sql)

def getParentTaxidFromTaxid(cursor, taxid):
    """
    Returns the taxonomy ID of the parent of the given taxonomy ID.
    
    Arguments:
        cursor -- A cursor pointing to the metagenomics SQLite database.
        taxid -- The taxonomy ID for a species, genus, family, etc.
    """
    sql = "SELECT " + dbDef.tblTaxonomy_col_parent_tax_id.name + " FROM " + dbDef.tblTaxonomy.name + " WHERE " + dbDef.tblTaxonomy_col_tax_id.name + " = '" + taxid + "';"

    return getSingleFieldFromSql(cursor, sql)
        
def getRankFromTaxid(cursor, taxid):
    """
    Returns the rank for the given taxonomy ID.
    
    Arguments:
        cursor -- A cursor pointing to the metagenomics SQLite database.
        taxid -- The taxonomy ID for a species, genus, family, etc.
    """
    sql = "SELECT "+ dbDef.tblTaxonomy_col_tax_rank.name + " FROM " + dbDef.tblTaxonomy.name + " WHERE " + dbDef.tblTaxonomy_col_tax_id.name + " = " + "'" + taxid + "';"
    
    return getSingleFieldFromSql(cursor, sql)

def isPartOfAbbreviatedRank(rank):
    """
    Returns true if the specified rank is part of the abbreviated ranks.
    
    Arguments:
        rank -- A rank that describes a level of taxonomy (e.g., "species",
            "subfamily", "superorder")
    """
    return rank.lower() in abbrRanks

def getAbbrTaxonomyFromTaxidRecursive(cursor, taxid, taxList):
    """
    Gets the abbreviated taxonomy for a taxonomy ID.  This is a recursive
    helper function which should not be called directly.  Call the
    getAbbrTaxonomyFromTaxid method instead.
    
    Arguments:
        cursor -- A cursor pointing to the metagenomics SQLite database.
        taxid -- The taxonomy ID for a species, genus, family, etc.
        taxList -- A list where the abbreviated taxonomy is added.
    """
    if taxid == "1": # this is root
        return True

    rank = getRankFromTaxid(cursor, taxid)
    name = getNameFromTaxid(cursor, taxid)
    
    if rank is None:
        print "Not able to retrieve rank"
        return False
    
    if isPartOfAbbreviatedRank(rank):
        taxList.insert(0, (taxid, name, rank))

    parentTaxid = getParentTaxidFromTaxid(cursor, taxid)
        
    if parentTaxid is None:
        print "Not able to retrieve parent id"
        return False
        
    return getAbbrTaxonomyFromTaxidRecursive(cursor, parentTaxid, taxList)

def getAbbrTaxonomyFromTaxid(cursor, taxid):
    """
    Gets the abbreviated taxonomy for a taxonomy ID.  Returns the results as a
    list where each item is a tuple of (taxonomy ID, name, rank).  The items in
    the list are ordered from highest (i.e., kingdom) to lowest (i.e., species)
    rank.
    
    Arguments:
        cursor -- A cursor pointing to the metagenomics SQLite database.
        taxid -- The taxonomy ID for a species, genus, family, etc.
    """
    taxList = []

    if cursor is None:
        print "Cursor was not defined"
        return None

    completeAbbrTax = getAbbrTaxonomyFromTaxidRecursive(cursor, taxid, taxList)

    if completeAbbrTax:
        return taxList
    else:
        print "Incomplete taxonomy"
        return None

# Just a simple test to show the retrieval of a taxonomy

#conn = sqlite3.connect("Metagenomics.db")
#cursor = conn.cursor()
#taxid = "58777"

#print getParentTaxidFromTaxid(cursor, taxid)
#print getRankFromTaxid(cursor, taxid)
#print getNameFromTaxid(cursor, taxid)
#print getAbbrTaxonomyFromTaxid(cursor, taxid)

#conn.commit()
#conn.close()