### Create a BACTERIAL_reference_files folder
#Example is for Staphoria Aureus
import os
import re
cwd = os.getcwd()
if input("Do you wish to change the working directory where REF_folder will be created? [y,n]\nCurrent working directory is: "+str(cwd)) == 'y':
    cwd = input("Enter new path: ")
else:
    print("Using current directory: "+cwd)

class GBS:
    """A Group B Streptococcus (Strep/GBS) genetic sample information class"""
    bacteria = 'Streptococcus_agalactiae'
    abrv = 'GBS'
    def __init__(self, name):
        self.name = name
        self.files = []

class Staph:
    """A Staphylococcus aureus (Staph/SA) genetic sample information class"""
    bacteria = 'Staphylococcus_aureus'
    abrv = 'SA'
    def __init__(self, name):
        self.name = name
        self.files = []
    def addfile(self, filename):
        self.files.append(filename)

for isolate in isolatelist:
    isolate.addfile(isolate+'R1.fastq.gz')
    isolate.addfile(isolate+'R2.fastq.gz')

# create localDB folder
if not found
    create localDB folder
else
    do nothing

# create BACTERIAL.fa
if not found
    search ncbi
    download from ncbi
else
    do nothing

# create header_mlst.txt file
if not found
    open
else
    do nothing

# create BACTERIAL.txt file for MLST
if not found
    open
else
    do nothing
