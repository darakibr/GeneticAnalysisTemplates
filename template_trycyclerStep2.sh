#!/bin/bash

### modify these variables ###
folder="GBS_ONT" #  >>> enter the name you want to give folder, will also dictate output names <<< #
REFERENCE="REFISOLATE" # >>> enter the reference isolate name (should match .fa file name) <<< #
threads="34"
current_time=$(date "+%y%m%d.%H%M")

### This is the second part of TRYCYCLER after generating good/bad clusters from long read data ###
cd Trycycler &&

for X in BCJB1835 ; do #  BCJB2983 BCJB3343 BCJB3344 BCJB3586 BCJB4361
		#trycycler cluster --assemblies "$X"_assemblies/*.fasta --reads "$X"_1k5perc.fastq --out_dir "$X"trycycler_out --threads "$threads"
		### Make sure to label all "BAD" clusters folder with '.bad_<cluster folder>' so it does not participate in the reconcile step. ###
		cd  "$X"trycycler_out &&
		for CLUSTER in */ ; do
				trycycler reconcile --reads ../"$X"_1k5perc.fastq --cluster_dir ./"$CLUSTER" --threads "$threads"
				trycycler msa --cluster_dir ./"$CLUSTER" --threads "$threads"
		done
		trycycler partition --reads ../"$X"_1k5perc.fastq --cluster_dirs ./cluster_* --threads "$threads"
		for CLUSTER in */ ; do
				trycycler consensus --cluster_dir ./"$CLUSTER"
		done
		cat ./cluster_*/7_final_consensus.fasta > ./"$X"consensus.fasta
		
		# Optional Polish for increased accuracy with Illumina short read #
		bwa index "$X"consensus.fasta
		bwa mem -t 16 -a "$X"consensus.fasta ../"$X"_R1.fastq.gz > "$X"_a1.sam
		bwa mem -t 16 -a "$X"consensus.fasta ../"$X"_R2.fastq.gz > "$X"_a2.sam
		polypolish ./"$X"trycycler_out/"$X"consensus.fasta "$X"_a1.sam "$X"_a2.sam > "$X"polish.fasta
		
		# Clean up
		#rm "$X"_a1.sam &&
		#rm "$X"_a2.sam &&
		#gzip *.fasta
		cd ..
		#rm "$X"_R1.fastq.gz &&
		#rm "$X"_R2.fastq.gz
		
done



