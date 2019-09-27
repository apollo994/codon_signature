#Codon Signature

Microorganism identification could be missleading or slow with traditional method (16S, phenotipical analysis).

This repository contains the scratch of a pipeline for alterntive classification using codon usage.

Here you will find the instraction to generate codon usage signature tables, starting from codon abbundance in CDS, to train a ML model.


## How to run the pipelines

Clone the repo cointinig the scripts and run it as follow:

```
git clone https://github.com/apollo994/codon_signature.git
bash codon_signature/codon_signature.sh RefSeq_table Taxon_IDs_list run_name
```

Where `RefSeq_table` is a table cointaining the following column (tab separated):
+ Taxid : the specific ID for the **Species** in RefSeq
+ Species : name of the species
+ Assembly : unique identifier of the deposited genome
+ AAA...TTT : 64 columns reppresenting the 64 codons and their absolute abbundance in the the CDS of the particular **Assembly**

`Taxon_IDs_list` is a .txt file that cointains one **Taxid** per line and reppresent the list of species you want for generate the final codon signature table (one for each Taxid)

`run_name` is the name used to name the folder cointainig the outputs
