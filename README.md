# Genetic Analysis Templates
New template files to make adation to new bacterial stains easier.

To automatically run pipeline (MASTERPIPELINE.py), the goal is to have a folder per project. Once that is set up, invocation of the pipeline will require another folder with the reference files, and either the original Illumina output or the demultiplexed fastq files.

1. REF_bacterial species
  - folder containing MLST, AMR, reference genome, and other necessary databases or files.
2. Project folder
  - fastq
    - folder containing all fastq files, gzipped.
  - illumina_out
    - folder containing all raw Illumina output files

Setting up python program to require folder path, REF folder path, and isolates list as inputs.
