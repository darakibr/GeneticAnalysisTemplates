### This will create a Sample Sheet for Illumina Output data ###

import os
import re
import pandas as pd
import numpy as np
from datetime import date

today = date.today().strftime("%Y%m%d")

# Read in Illumina IDT labels to identify samples with corresponding index
idt = pd.read_csv("illumina_IDT.csv")

#Template header required
header = "[Header],,,,,,,,,\
          Investigator Name,INVNAME,,,,,,,,\
          Experiment Name,EXPERIMENT,,,,,,,,\
          Date,TODAYDATE,,,,,,,,\
          Workflow,GenerateFASTQ,,,,,,,,\
          Application,FASTQ Only,,,,,,,,\
          Instrument Type,INSTRUMENT,,,,,,,,\
          Assay,Nextera DNA Flex,,,,,,,,\
          Index Adapters,IDT-ILMN Nextera DNA UD Indexes (384 Indexes),,,,,,,,\
          Description,DESC,,,,,,,,\
          Chemistry,Amplicon,,,,,,,,\
          ,,,,,,,,,\
          [Reads],,,,,,,,,\
          READCYCLES,,,,,,,,,\
          READCYCLES,,,,,,,,,\
          ,,,,,,,,,\
          [Settings],,,,,,,,,\
          ReverseComplement,0,,,,,,,,\
          ,,,,,,,,,\
          [Data],,,,,,,,,"

def createSampleSheet():
  investigator_name = input("Investigator Name:\n")
  project = input("Name of project (avoid using spaces):\nEx. StaphoriaRun\n")
  today_date= date.today().strftime("%-d/%-m/%y")
  description = input("Description of run:\nEx. Staph_GBSmut_date\n")  
  runtype = input("Type N for a NextSeq run or M for a MiSeq run:\n")
  if runtype == "N":
    instrument_type = "NextSeq"
    read_cycles = 151
  elif == "M":
    instrument_type = "MiSeq"
    read_cycles = 301
  else:
    runtype = input("Invalid input, please use either 'N' for NextSeq or 'M' for MiSeq only.\n")

  with open('SampleSheet_'+project+today+'.csv', 'w') as file:
    tempheader = header
    tempheader = re.sub('INVNAME',investigator_name, tempheader)
    tempheader = re.sub('EXPERIMENT',project, tempheader)
    tempheader = re.sub('TODAYDATE',today_date, tempheader)
    tempheader = re.sub('INSTRUMENT',instrument_type, tempheader)
    tempheader = re.sub('DESC',description, tempheader)
    tempheader = re.sub('READCYCLES',read_cycles, tempheader)
    file.write(tempheader)

createSampleSheet()
