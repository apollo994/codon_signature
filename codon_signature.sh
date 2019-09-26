#!/usr/bin/env bash
#Fabio Zanarello, JRC-ispra, 2019


refeseq_tab=$1
idx_list=$2
run_name=$3

result_folder="results_$run_name"

echo ""
echo "Creating results folder..."
mkdir $result_folder
echo "DONE"

while read id; do

echo ""
echo "Working on TAXID: $id"

echo "Extracting assemblies and computing relative frequencies..."
#python codon_signature/get_codon_freq.py --input $refseq_tab --id $id --output $result_folder"/"$id"_step1_res.tsv"
touch $result_folder"/"$id"_step1_res.tsv"
echo "DONE"

echo "Compiuting triplets couple ratio..."
#python codon_signature/get_couple.py --input $result_folder"/"$id"_step1_res.tsv" --output $result_folder"/"$id"_step2_res.tsv"
touch $result_folder"/"$id"_step2_res.tsv"
echo "DONE"

echo "Generating final 10k lines table..."
#python codon_signature/get_final_tab.py --input $result_folder"/"$id"_step2_res.tsv" --output $result_folder"/"$id"_final.tsv"
touch $result_folder"/"$id"_final.tsv"
echo "DONE"

echo "Cleaning temporary files.."
rm $result_folder"/"$id"_step1_res.tsv"
rm $result_folder"/"$id"_step2_res.tsv"
echo "DONE"


done <$idx_list

echo ""
echo "Check you results in $result_folder"/ folder""
echo ""
