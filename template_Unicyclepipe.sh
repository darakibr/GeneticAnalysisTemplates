#!/bin/bash

### modify these variables ###
folder="ONT" #  >>> enter the name you want to give folder, will also dictate output names <<< #
REFERENCE="REFISOLATE" # >>> enter the reference isolate name (should match .fa file name) <<< #
threads="34"

#mkdir hybrid &&
cd hybrid &&

for X in BCJB1835 BCJB2983 BCJB3343 BCJB3344 BCJB3586 BCJB4361 ; do #For XXXX insert strain or accession numbers#
		cp ../fastq/"$X"_R1.fastq.gz .
		cp ../fastq/"$X"_R2.fastq.gz .
		
		#trim ONT reads to >5k and eliminate worst 5% of reads#
		filtlong --min_length 5000 --keep_percent 95 ../../GBS_ONT/TypeIV/demultiplex/"$X"_ONT.fastq.gz > "$X"_5k5perc.fastq
		
		#check read quality using raspberry
		raspberry "$X"_5k5perc.fastq > "$X"_readqc.txt
		#quick cleanup
		rm *.rlen
		
		# UNICYCLER
		unicycler -1 "$X"_R1.fastq.gz -2 "$X"_R2.fastq.gz -l "$X"_5k5perc.fastq -o "$X"_hybrid -t "$threads" 
		
		#cleanup#
		rm *.fastq.gz
		
done
