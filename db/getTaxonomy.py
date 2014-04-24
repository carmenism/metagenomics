#!/usr/bin/env python
import dbDef
import sqlite3

abbrRanks = ["domain", "kingdom", "phylum", "class", "order", "family", "genus", "species"]

def getSingleFieldFromSql(cursor, sql):
    try:
        cursor.execute(sql)
        
        data = str(cursor.fetchone()[0])
        
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
        return False
    
    if isPartOfAbbreviatedRank(rank):
        taxList.insert(0, (taxid, name, rank))

    parentTaxid = getParentTaxidFromTaxid(cursor, taxid)
        
    if parentTaxid is None:
        return False
        
    return getAbbrTaxonomyFromTaxidRecursive(cursor, parentTaxid, taxList)

def getAbbrTaxonomyFromTaxid(cursor, taxid):
    taxList = []

    completeAbbrTax = getAbbrTaxonomyFromTaxidRecursive(cursor, taxid, taxList)

    if completeAbbrTax:
        return taxList
    else:
        return None

conn = sqlite3.connect("Metagenomics.db")
cursor = conn.cursor()
print getParentTaxidFromTaxid(cursor,"58777")
print getRankFromTaxid(cursor,"58777")
print getNameFromTaxid(cursor,"58777")
print getAbbrTaxonomyFromTaxid(cursor, "58777")
conn.commit()
conn.close()