#IMPORT LIBRARIES
import os

#SET VARIABLES
cwd = os.getcwd()
folder = cwd+"Trycycler"
threads = 34
genomesize = '2200000'
isolatelist = ['BCJB1835','BCJB2983','BCJB3343','BCJB3344','BCJB3586','BCJB4361']

def changetemplate(template, threads, genomesize, isolatelist)
  #change variables in template to have actual values

def runbashfile(name)
  #bash command to run file

#RUN STEP 1 of Trycycler
# modify template .sh file and run

#View ouput trees
# format is .newik

#select 'bad' clusters
# rename 'bad' clusters with '.bad_<name>' so that Trycycler will ignore them in following steps

#RUN STEP 2 of Trycycler
