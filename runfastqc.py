#!/usr/bin/env python

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
            #subprocess.call(command.split())