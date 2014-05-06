#!/usr/bin/env python
import dbDef
import sqlite3

abbrRanks = ["superkingdom", "kingdom", "phylum", "class", "order", "family", "genus", "species"]

def getSingleFieldFromSql(cursor, sql):
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
    sql = "SELECT " + dbDef.tblTaxonomy_col_tax_name.name + " FROM " + dbDef.tblTaxonomy.name + " WHERE " + dbDef.tblTaxonomy_col_tax_id.name + " = '" + taxid + "';"
    
    return getSingleFieldFromSql(cursor, sql)
    

def getParentTaxidFromTaxid(cursor, taxid):
    sql = "SELECT " + dbDef.tblTaxonomy_col_parent_tax_id.name + " FROM " + dbDef.tblTaxonomy.name + " WHERE " + dbDef.tblTaxonomy_col_tax_id.name + " = '" + taxid + "';"

    return getSingleFieldFromSql(cursor, sql)
        
def getRankFromTaxid(cursor, taxid):
    sql = "SELECT "+ dbDef.tblTaxonomy_col_tax_rank.name + " FROM " + dbDef.tblTaxonomy.name + " WHERE " + dbDef.tblTaxonomy_col_tax_id.name + " = " + "'" + taxid + "';"
    
    return getSingleFieldFromSql(cursor, sql)

def isPartOfAbbreviatedRank(rank):
    return rank.lower() in abbrRanks

def getAbbrTaxonomyFromTaxidRecursive(cursor, taxid, taxList):
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