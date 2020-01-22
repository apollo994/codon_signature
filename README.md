# Codon Signature

Microorganism identification could be misleading or slow with traditional methods (16S, phenotypical analysis).

This repository contains the scratch of a pipeline for alternative classification using codon usage patterns.

Here you will find a pipeline to generate codon usage signature tables to train an ML model, starting from codon abundance in CDS.


## How to run the pipeline

Clone the repo containig the scripts and run it as follows:

```
git clone https://github.com/apollo994/codon_signature.git
bash codon_signature/preprocessing/codon_signature.sh RefSeq_table Taxon_IDs_list run_name
```

Where `RefSeq_table` is a table containing the following columns (tab-separated):
+ **Taxid** : the specific ID for the species in RefSeq
+ **Species** : scientific name of the species
+ **Assembly** : unique identifier of the deposited genome assembly
+ **AAA...TTT** : 64 columns representing codons and their absolute abundance in the CDS of the assembly

`Taxon_IDs_list` is a .txt file that contains one **Taxid** per line and represents the list of species you want to generate the final codon signature table for (one for each Taxid)

`run_name` is the name used to name the folder containing as many files as Taxids you asked for, each of them representing the codon signature of each species.
