#!/usr/bin/env python
# Filename: dbDef.py

import sqlite3

class ColumnDefinition:
    def __init__(self, col_name, col_type):
        self.name = col_name
        self.type = col_type
        
    def createString(self):
        return self.name + " " + self.type

class TableDefinition:
    def __init__(self, table_name, table_cols, table_primary_key = None):
        self.name = table_name
        self.cols = table_cols
        self.primary_key = table_primary_key
        
    def createString(self):
        colStr = ", ".join([col.createString() for col in self.cols])
        
        createStr = "CREATE TABLE " + self.name + " (" + colStr + " "
        
        if self.primary_key is not None:
            return createStr + ", " + self.primary_key + ")"
        
        return createStr + ")"
    
    def dropString(self):
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
    sql = table.dropString()

    cursor.execute(sql)
    
def createTable(cursor, table):
    sql = table.createString()

    print sql
    cursor.execute(sql)