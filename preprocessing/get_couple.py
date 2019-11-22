#!/usr/bin/env python
# Fabio Zanarello, JRC-ispra, 2019


import os
import sys
import argparse
from collections import defaultdict
import pandas as pd
import numpy as np
import collections


def main():
    parser = argparse.ArgumentParser(description='My nice tool.')
    parser.add_argument('--input', metavar='INPUTFILE', default="/dev/stdin", help='The input file.')
    #parser.add_argument('--id', metavar='ID',help='RefSeq tax ID',type=int)
    parser.add_argument('--output', metavar='OUTPUTFILE', default="/dev/stdout", help='The output file.')
    args = parser.parse_args()

    #code to print the dictionary couple

    # codons1=["AAA","AAC","AAG","AAT","ACA","ACC","ACG","ACT","AGA","AGC","AGG",
    # "AGT","ATA","ATC","ATG","ATT","CAA","CAC","CAG","CAT","CCA","CCC","CCG","CCT",
    # "CGA","CGC","CGG","CGT","CTA","CTC","CTG","CTT"]
    #
    # codons2=["GAA","GAC","GAG","GAT","GCA","GCC","GCG","GCT","GGA","GGC","GGG",
    # "GGT","GTA","GTC","GTG","GTT","TAA","TAC","TAG","TAT","TCA","TCC","TCG","TCT",
    # "TGA","TGC","TGG","TGT","TTA","TTC","TTG","TTT"]
    # codons2.reverse()
    #
    # for i in range(1,33):
    #     print("couple[\"C"+str(i)+"\"]=[\""+codons1[i-1]+"\",\""+codons2[i-1]+"\"]")

    #read rge triplets freq table from step1
    data=pd.read_csv(args.input, sep="\t", index_col="Assembly", low_memory=False)
    ass_id=data.index.tolist()


    #dictionary cointainig the complementary triplets
    couple = dict()


    couple["C1"]=["AAG","CTT"]
    couple["C2"]=["GTA","TAC"]
    couple["C3"]=["ACC","GGT"]
    couple["C4"]=["AAC","GTT"]
    couple["C5"]=["GGA","TCC"]
    couple["C6"]=["GCA","TGC"]
    couple["C7"]=["AGG","CCT"]
    couple["C8"]=["ATA","TAT"]
    couple["C9"]=["CCA","TGG"]
    couple["C10"]=["TAA","TTA"]
    couple["C11"]=["ATC","GAT"]
    couple["C12"]=["CCG","CGG"]
    couple["C13"]=["CTC","GAG"]
    couple["C14"]=["ACA","TGT"]
    couple["C15"]=["AGC","GCT"]
    couple["C16"]=["TCA","TGA"]
    couple["C17"]=["CAA","TTG"]
    couple["C18"]=["ACG","CGT"]
    couple["C19"]=["AGA","TCT"]
    couple["C20"]=["CGA","TCG"]
    couple["C21"]=["TAG","CTA"]
    couple["C22"]=["ATG","CAT"]
    couple["C23"]=["GAA","TTC"]
    couple["C24"]=["GCC","GGC"]
    couple["C25"]=["CCC","GGG"]
    couple["C26"]=["GAC","GTC"]
    couple["C27"]=["CAG","CTG"]
    couple["C28"]=["AAT","ATT"]
    couple["C29"]=["CAC","GTG"]
    couple["C30"]=["AAA","TTT"]
    couple["C31"]=["CGC","GCG"]
    couple["C32"]=["ACT","AGT"]

    #list of the triplets used to create an empty DataFrame
    new_col=list(couple.keys())
    data_couple=pd.DataFrame(columns=new_col)

    for element in couple:
        #only two triplets of interest
        temp_data=data[couple[element]]

        #seq name of the two triplets
        AA1=couple[element][0]
        AA2=couple[element][1]
        cup_values=[]
        #cycle on each row to eaxtract triplets fres
        for index, row in temp_data.iterrows():
            AA_values=[]
            AA_values.append(row[AA1])
            AA_values.append(row[AA2])

            #freq values with increasing order
            AA_values.sort()
            #ratio of the freq (alway smaller/bigger)
            cup_values.append(AA_values[0]/AA_values[1])

        #add the values to the couple column
        data_couple[element]=cup_values

    data_couple["Assembly"]=ass_id
    data_couple=data_couple.round(2)
    data_couple.to_csv(args.output, sep="\t",index=False, )


if __name__ == "__main__":
    main()
