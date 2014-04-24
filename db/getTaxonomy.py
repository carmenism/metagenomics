import dbDef
import sqlite3

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