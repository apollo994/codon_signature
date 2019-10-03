#!/usr/bin/env bash
#Fabio Zanarello, JRC-ispra, 2019


refseq_tab=$1
idx_list=$2
run_name=$3

python=python3.7

result_folder="results_$run_name"

echo ""
echo "Creating results folder..."
mkdir -p $result_folder
echo "DONE"

while read id; do

echo ""
echo "Working on TAXID: $id"
echo "Extracting assemblies and computing relative frequencies..."
$python codon_signature/get_codon_freq.py --input $refseq_tab --id $id --output $result_folder"/"$id"_step1_res.tsv"
#python codon_signature/get_codon_freq.py --input data/o576245-Refseq_species.tsv --output res_step_1.tsv --id 1428
#touch $result_folder"/"$id"_step1_res.tsv"
echo "DONE"

echo "Compiuting triplets couple ratio..."
$python codon_signature/get_couple.py --input $result_folder"/"$id"_step1_res.tsv" --output $result_folder"/"$id"_step2_res.tsv"
#python codon_signature/get_couple.py --input res_step_1.tsv --output res_step_2.tsv
#touch $result_folder"/"$id"_step2_res.tsv"
echo "DONE"

echo "Generating final 10k lines table..."
$python codon_signature/get_final_table.py --input $result_folder"/"$id"_step2_res.tsv" --output $result_folder"/"$id"_final.tsv"
#python codon_signature/get_final_table.py --input res_step_2.tsv --output res_final.tsv
#touch $result_folder"/"$id"_final.tsv"
echo "DONE"

echo "Cleaning temporary files.."
rm $result_folder"/"$id"_step1_res.tsv"
rm $result_folder"/"$id"_step2_res.tsv"
echo "DONE"


done <$idx_list

echo ""
echo "Check you results in $result_folder"/ folder""
echo ""


# echo "$refseq_tab"
# echo $1
# echo "$1"
# more "$refseq_tab"
