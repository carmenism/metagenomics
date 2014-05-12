#!/usr/bin/env python
"""
=========
runfastqc
=========

Authors
-------
Carmen St. Jean (crr8@unh.edu)
    
Date
----
April 1, 2014

Abstract
--------
Runs fastqc for all of the files in the specified directory.

Instructions
------------
On a computer which has python, call:

    python runfastqc.py /path/to/fastq/files/
"""
import sys
import glob
import os
import subprocess

directory = str(sys.argv[1])

for subdir in os.walk(directory):
    os.chdir(subdir[0])
    
    for fileName in glob.glob("*.fastq.gz"):
        if (not "adnq" in fileName):
            command = "fastqc " + fileName + " "
            print "Running fastqc on " + fileName
            subprocess.call(command.split())