#!/bin/bash

### DEFINE INPUTS ###
docpath="/home/user/Documents/GBS_typeIV"
SEjar="/home/user/gen-soft/snpEff_latest_core/snpEff/snpEff.jar"
folder="ST459"
REF="NGBS061"
CHROM="CP007631"
# REQUIRES REF_ref_k14s8 and REF.fa file already in reference files folder

for X in SAMPLESLIST ; do
    #CHECK if .vcf file already exists
    if [ ! -f "$doc"/treefiles/vcfall/"$X".vcf ]
    then
        #CHECK if in our folder or CDC folder
        if [ ! -f "$doc"/fastq/"$X"_R1.fastq.gz ]
        then
            cp "$doc"/../CDC_GBS/fastq/"$X"_R1.fastq.gz "$X"_1.fastq.gz
            cp "$doc"/../CDC_GBS/fastq/"$X"_R2.fastq.gz "$X"_2.fastq.gz
        else
            cp "$doc"/fastq/"$X"_R1.fastq.gz "$X"_1.fastq.gz
            cp "$doc"/fastq/"$X"_R2.fastq.gz "$X"_2.fastq.gz
        fi
        # SMALT CODE to create .vcf file
        smalt map -f sam -n 20 -o "$X"_map.sam "$doc"/../GBS_reference_files/"$REF"_ref_k14s8 "$X"_1.fastq.gz "$X"_2.fastq.gz &&
        # Convert sam to bam file using SAMTOOLS and then sort
        samtools view -S -b -@ 20 "$X"_map.sam > "$X".bam &&
        samtools sort -@ 20 "X".bam > "$X"sort.bam &&
        # FREEBAYES call polys
        freebayes -f "$doc"/../GBS_reference_files/"$REF".fa -p 1 "X"sort.bam > "$X".vcf &&
        #cleanup
        rm "$X"_*.fastq.gz
        rm "$X"*.bam
        rm "$X"*.sam
        mv "$X".vcf "$doc"/treefiles/vcfall/ &&
        echo "Generated $X.vcf file and saved to $doc/treefiles/vcfall/"
    else
        cp "$doc"/treefiles/vcfall/"$X".vcf &&
        echo "File exists and copied from $doc/treefiles/vcfall/$X.vcf"
    fi
    # FILTER VCF with BCFTOOLS #
    bcftools view -i 'MIN(INFO/DP)>15 & QUAL>10' "$X".vcf -o "$X"_dp15q10.vcf &&
    bcftools view -i 'MIN(INFO/AO/INFO/DP)>0,75' "$X"_dp15q10.vcf -o "$X"_dp15q10f75.vcf &&
    vcftools --vcf "$X"_dp15q10f75.vcf --recode -out "$X" &&
    rm "$X"_dp15q10.vcf
    rm "$X"_dp15q10f75.vcf
    mv "$X".recode.vcf "$X"-"$folder".vcf &&
    bgzip "$X"-"$folder".vcf &&
    tabix -p vcf "$X"-"$folder".vcf.gz &&
    rm "$X".vcf
    mv *.vcf.gz ./"REF"-indexed/ &&
    mv *.tbi ./"REF"-indexed/ &&
    echo "DONE WITH $X"
done
### MERGE all vcf files to convert to dataframe ###
    bcftools merge --force-samples -O vcf -o "$folder"-merged.vcf ./"$REF"-indexed/*.vcf.gz &&
    sed -i "s/$CHROM.2/$CHROM/g" "$folder"-merged.vcf &&
    java -jar "$SEjar" -no-downstream -no-upstream -nolof "$CHROM" "$folder"-merged.vcf > "$folder"-jar.vcf &&
    bcftools annotate -x FORMAT "$folder"-jar.vcf > "$folder"-annotated.vcf &&
    sed "s/,/;/g" "$folder"-annotated.vcf > "$folder"-clean.vcf &&
    sed -i "s/INFO\tFORMAT/Allele|Annotation|Impact|Gene_name|Gene_id|Feature_type|Feature_id|Transcript_biotype\
    |Rank|HGVS.c|HGVS.p|cDNA_pos_length|CDS_pos_length|AA_pos_length|Distance|errors_warnings_info\tFORMAT/g" "$folder"-clean.vcf &&
    sed -i "s/|/\.\t/g" "$folder"-clean.vcf &&
    sed -i "s/\t\tGT/\tGT/g" "$folder"-clean.vcf &&
    sed "/^##/d" "$folder"-clean.vcf > "$folder".csv &&
    sed -i "s/\t\./,NULL/g" "$folder".csv && ### > t.csv ###
    sed -i "s/\t/,/g" "$folder".csv &&
    sed -i "s/,INFO.*PRIME,/,/g" "$folder".csv &&
    sed -i "s/,;.*GT/,/g" "$folder".csv &&
    sed -i "s/INFO.*,GT/GT/g" "$folder".csv &&
    sed -i "s/,WARNING/WARNING/g" "$folder".csv &&
    sed -i "s/&GT/,GT/g" "$folder".csv &&
    sed -i "s/,\./,/g" "$folder".csv &&
# DONE #
