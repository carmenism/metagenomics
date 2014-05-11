#!/usr/bin/env python
"""
============
dbDef module
============

Authors
-------
Thomas Rossi (trn5@unh.edu)
Carmen St. Jean (crr8@unh.edu)
    
Date
----
April 15, 2014
    
Abstract
--------
This module defines table names and column names for the metagenomics database
based on the reference file and the NCBI taxonomy.  
"""
import sqlite3

class ColumnDefinition:
    """
    This class represents a definition for a column in an SQL table.  Stores
    the name and type of the column.  
    """
    def __init__(self, colName, colType):
        """
        Creates a new column definition object.
        
        Arguments:
            colName -- The name of the column.
            colType -- The data type of the column.
        """
        self.name = colName
        self.type = colType
        
    def createString(self):
        """
        Creates a string for the column definition to be used in a CREATE
        TABLE SQLite statement.
        """
        return self.name + " " + self.type

class TableDefinition:
    """
    This class represents a definition for a table in an SQL database.  Stores
    the name of the table and a list of column definition objects.
    """
    def __init__(self, tableName, tableCols, tablePrimaryKey = None):
        """
        Creates a new table definition object.
        
        Arguments:
            tableName -- The name of the table.
            tableCols -- A list of ColumnDefinition objects.
            tablePrimaryKey -- An optional parameter for specifying the columns
                which form the primary key.  If the primary key should be a
                single column, then do not use this parameter and add "PRIMARY
                KEY" to the name of the ColumnDefinition object.
        """
        self.name = tableName
        self.cols = tableCols
        self.primary_key = tablePrimaryKey
        
    def createString(self):
        """
        Builds a string that is an SQLite CREATE TABLE statement for this
        table.
        """
        colStr = ", ".join([col.createString() for col in self.cols])
        
        createStr = "CREATE TABLE " + self.name + " (" + colStr + " "
        
        if self.primary_key is not None:
            return createStr + ", " + self.primary_key + ")"
        
        return createStr + ")"
    
    def dropString(self):
        """
        Builds a string that is an SQLite DROP TABLE statement for this table.
        """
        return "DROP TABLE IF EXISTS " + self.name
    
tblSpecies_col_ncid = ColumnDefinition("ncid", "VARCHAR(20) PRIMARY KEY")
tblSpecies_col_tax_id = ColumnDefinition("tax_id", "VARCHAR(14)")
tblSpecies_col_taxonomy = ColumnDefinition("taxonomy", "VARCHAR(2500)")
tblSpecies_cols = [tblSpecies_col_ncid, tblSpecies_col_tax_id, tblSpecies_col_taxonomy]
tblSpecies = TableDefinition("tblSpecies", tblSpecies_cols)

tblGene_col_ncid = ColumnDefinition("ncid", "VARCHAR(20)")
tblGene_col_gene_id = ColumnDefinition("gene_id", "VARCHAR(14)")
tblGene_col_start = ColumnDefinition("start", "INT")
tblGene_col_stop = ColumnDefinition("stop", "INT")
tblGene_col_function = ColumnDefinition("function", "VARCHAR(2500)")
tblGene_col_cog_id = ColumnDefinition("cog_id", "VARCHAR(20)")
tblGene_cols = [tblGene_col_ncid, tblGene_col_gene_id, tblGene_col_start, tblGene_col_stop, tblGene_col_function, tblGene_col_cog_id]
tblGene = TableDefinition("tblGene", tblGene_cols, "PRIMARY KEY(" + tblGene_col_ncid.name + ", " + tblGene_col_gene_id.name + ")")

tblTaxonomy_col_tax_id = ColumnDefinition("tax_id", "VARCHAR(14) PRIMARY KEY")
tblTaxonomy_col_tax_rank = ColumnDefinition("tax_rank", "VARCHAR(40)")
tblTaxonomy_col_parent_tax_id = ColumnDefinition("parent_tax_id", "VARCHAR(14)")
tblTaxonomy_col_tax_name = ColumnDefinition("tax_name", "VARCHAR(200)")
tblTaxonomy_cols = [tblTaxonomy_col_tax_id, tblTaxonomy_col_tax_name, tblTaxonomy_col_tax_rank, tblTaxonomy_col_parent_tax_id]
tblTaxonomy = TableDefinition("tblTaxonomy", tblTaxonomy_cols)

def dropTable(cursor, table):
    """
    Drops the specified table from the SQLite database.
    
    Arguments:
        cursor -- A cursor pointing to the metagenomics SQLite database.
        table -- A TableDefinition object.
    """
    sql = table.dropString()

    cursor.execute(sql)
    
def createTable(cursor, table):
    """
    Creates the specified table from the SQLite database.
    
    Arguments:
        cursor -- A cursor pointing to the metagenomics SQLite database.
        table -- A TableDefinition object.
    """
    sql = table.createString()

    print sql
    cursor.execute(sql)