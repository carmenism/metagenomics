import dbDef
import sqlite3

abbrRanks = [“domain”, “kingdom”, “phylum”, “class”, “order”, “family”, “genus”, “species”]

def getParentTaxidFromTaxid(cursor, taxid):
    sql = "SELECT " + dbDef.tblTaxonomy_col_parent_tax_id.name + " FROM " + dbDef.tblTaxonomy.name + " WHERE " + dbDef.tblTaxonomy_col_tax_id.name + " = '" + taxid + "';"
    
    try:
        cursor.execute(sql)
        
        data = cursor.fetchone()
        
        print data
        
        return data
    except sqlite3.Error:
        return None
        
def getRankFromTaxid(cursor, taxid):
    sql = "SELECT "+ dbDef.tblTaxonomy_col_rank.name + " FROM " + dbDef.tblTaxonomy.name + " WHERE " + dbDef.tblTaxonomy_col_tax_id.name + " = " + "'" + taxid + "';"
    
    try:
        cursor.execute(sql)
        
        data = cursor.fetchone()
        
        print data
        
        return data
    except sqlite3.Error:
        return None

def isPartOfAbbreviatedRank(rank):
    return rank in abbrRanks

def getAbbrTaxonomyFromTaxidRecursive(cursor, taxid, list):
    if taxid == 1: # this is root
        return

    rank = getRankFromTaxid(cursor, taxid)
    
    if isPartOfAbbreviated(rank):
        list.append((taxid, rank))

    parentTaxid = getParentTaxidFromTaxid(cursor, taxid)
        
    getAbbrTaxonomyFromTaxidRecursive(cursor, parentTaxid, list)

def getAbbrTaxonomyFromTaxid(cursor, taxid):
    list = []

    getAbbrTaxonomyFromTaxidRecursive(cursor, taxid, list)

    return list
