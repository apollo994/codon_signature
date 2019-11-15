# Codon Signature

Microorganism identification could be missleading or slow with traditional method (16S, phenotipical analysis).

This repository contains the scratch of a pipeline for alterntive classification using codon usage.

Here you will find a pipeline to generate codon usage signature tables to train a ML model, starting from codon abbundance in CDS.


## How to run the pipelines

Clone the repo cointinig the scripts and run it as follow:

```
git clone https://github.com/apollo994/codon_signature.git
bash codon_signature/preprocessing/codon_signature.sh RefSeq_table Taxon_IDs_list run_name
```

Where `RefSeq_table` is a table cointaining the following column (tab separated):
+ **Taxid** : the specific ID for the Species in RefSeq
+ **Species** : name of the species
+ **Assembly** : unique identifier of the deposited genome
+ **AAA...TTT** : 64 columns reppresenting codons and their absolute abbundance in the CDS of the Assembly

`Taxon_IDs_list` is a .txt file that cointains one **Taxid** per line and reppresent the list of species you want for generate the final codon signature table (one for each Taxid)

`run_name` is the name used to name the folder cointainig as many file as many Taxid you askd for, each of them reppresenting the codon signature of each species.
