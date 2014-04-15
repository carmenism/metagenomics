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
    
def dropTable(cursor, table):
    sql = table.dropString()

    cursor.execute(sql)
    
def createTable(cursor, table):
    sql = table.createString()

    print sql
    cursor.execute(sql)