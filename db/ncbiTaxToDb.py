#!/usr/bin/env python

import os
import os.path
import urllib
import zipfile
import dbDef

tblTaxonomy_col_tax_id = dbDef.ColumnDefinition("tax_id", "VARCHAR(14) PRIMARY KEY")
tblTaxonomy_col_tax_rank = dbDef.ColumnDefinition("tax_rank", "VARCHAR(40)")
tblTaxonomy_col_parent_tax_id = dbDef.ColumnDefinition("parent_tax_id", "VARCHAR(14)")
tblTaxonomy_cols = [tblTaxonomy_col_tax_id, tblTaxonomy_col_tax_rank, tblTaxonomy_col_parent_tax_id]
tblTaxonomy = dbDef.TableDefinition("tblTaxonomy", tblTaxonomy_cols)

taxdmpZip = 'taxdmp.zip'
nodesFilename = 'nodes.dmp'
namesFilename = 'names.dmp'

#urllib.urlretrieve('ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdmp.zip', taxdmpZip)

zfile = zipfile.ZipFile(taxdmpZip)

zfile.extract(nodesFilename, nodesFilename)
zfile.extract(namesFilename, namesFilename)

