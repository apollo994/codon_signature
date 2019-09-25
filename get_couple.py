#!/usr/bin/env python3
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

    #code to print the couple

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


    data=pd.read_csv(args.input, sep="\t", index_col=False, low_memory=False)

    couple = dict()

    couple["C1"]=["AAA","TTT"]
    couple["C2"]=["AAC","TTG"]
    couple["C3"]=["AAG","TTC"]
    couple["C4"]=["AAT","TTA"]
    couple["C5"]=["ACA","TGT"]
    couple["C6"]=["ACC","TGG"]
    couple["C7"]=["ACG","TGC"]
    couple["C8"]=["ACT","TGA"]
    couple["C9"]=["AGA","TCT"]
    couple["C10"]=["AGC","TCG"]
    couple["C11"]=["AGG","TCC"]
    couple["C12"]=["AGT","TCA"]
    couple["C13"]=["ATA","TAT"]
    couple["C14"]=["ATC","TAG"]
    couple["C15"]=["ATG","TAC"]
    couple["C16"]=["ATT","TAA"]
    couple["C17"]=["CAA","GTT"]
    couple["C18"]=["CAC","GTG"]
    couple["C19"]=["CAG","GTC"]
    couple["C20"]=["CAT","GTA"]
    couple["C21"]=["CCA","GGT"]
    couple["C22"]=["CCC","GGG"]
    couple["C23"]=["CCG","GGC"]
    couple["C24"]=["CCT","GGA"]
    couple["C25"]=["CGA","GCT"]
    couple["C26"]=["CGC","GCG"]
    couple["C27"]=["CGG","GCC"]
    couple["C28"]=["CGT","GCA"]
    couple["C29"]=["CTA","GAT"]
    couple["C30"]=["CTC","GAG"]
    couple["C31"]=["CTG","GAC"]
    couple["C32"]=["CTT","GAA"]

    new_col=list(couple.keys())

    for element in couple:
        temp_data=data.iloc[:,couple[element]]
    #     print (couple[element])
    # #print (temp_data)
    #print (data.loc[:,["AAA","TTT"]])


if __name__ == "__main__":
    main()
