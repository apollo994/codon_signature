#!/usr/bin/env python3
# Fabio Zanarello & Michele Maroni, JRC-ispra, 2019


import os
import sys
import argparse
from collections import defaultdict
import pandas as pd
import numpy as np
import collections


def main():
    """"""
    parser = argparse.ArgumentParser(description='My nice tool.')
    parser.add_argument('--input', metavar='INPUTFILE', default="/dev/stdin", help='The input file.')
    parser.add_argument('--id', metavar='ID',help='RefSeq tax ID',type=int)
    parser.add_argument('--output', metavar='OUTPUTFILE', default="/dev/stdout", help='The output file.')
    #Create a print_debug mode
    parser.add_argument('--verbose', metavar='VERBOSE', default=False, type=bool)
    args = parser.parse_args()

    #Dicrionary cointaing the genetic code (AA/correspondig triplets)
    genecode=dict()

    genecode["A"] = ["GCT","GCC","GCA","GCG"]
    genecode["L"] = ["TTA","TTG","CTT","CTC","CTA","CTG"]
    genecode["R"] = ["CGT","CGC","CGA","CGG","AGA","AGG"]
    genecode["K"] = ["AAA","AAG"]
    genecode["N"] = ["AAT","AAC"]
    genecode["M"] = ["ATG"]
    genecode["D"] = ["GAT","GAC"]
    genecode["F"] = ["TTT","TTC"]
    genecode["C"] = ["TGT","TGC"]
    genecode["P"] = ["CCT","CCC","CCA","CCG"]
    genecode["Q"] = ["CAA","CAG"]
    genecode["S"] = ["TCT","TCC","TCA","TCG","AGT","AGC"]
    genecode["E"] = ["GAA","GAG"]
    genecode["T"] = ["ACT","ACC","ACA","ACG"]
    genecode["G"] = ["GGT","GGC","GGA","GGG"]
    genecode["W"] = ["TGG"]
    genecode["H"] = ["CAT","CAC"]
    genecode["Y"] = ["TAT","TAC"]
    genecode["I"] = ["ATT","ATC","ATA"]
    genecode["V"] = ["GTT","GTC","GTA","GTG"]
    genecode["Z"] = ["TAA","TGA","TAG"]

    # Ideaa Fabio: invece di fare un ciclo for, carica il file in un dataframe, prendi tutte i nomi delle colonne e elimina quelle che non interessano"
        # Create a list of variable names to be kept
    to_keep=["Species","Assembly"]
    # Append to the 'to_keep' list the codon columns from the input table
    # that corresponds to each aminoacid in the genecode dictionary
    for AA in genecode:
        for trip in genecode[AA]:
            to_keep.append(trip)
    if args.verbose==True:
        print("Line to to_keep\n",to_keep)

    data=pd.read_csv(args.input, sep="\t", index_col=False, low_memory=False)
    data=data.set_index("Taxid")
    # Create a new dataframe RefSeq tax ID,Species,Assembly and all the codons from genecode dictionary as columns
    # that is has only the rows where RefSeq is equal to the input Tax Id
    one_id_data=(data.loc[args.id,to_keep])
    if args.verbose==True:
        print("DataFrame columns\n",one_id_data)


    # data.index.names = [None]
    ratio_all=pd.DataFrame(index=data.index)

    #table with all triplets frequencies

    for AA in genecode:
        sub_data=data.loc[:,genecode[AA]]
        if args.verbose==True:
            print("Subset of codon columns for ",AA,":\n",sub_data)
        ratio_subdata=sub_data.div(sub_data.sum(axis=1), axis=0)
        if args.verbose==True:
            print("Relative frequency of codon usage for",AA,":\n", ratio_subdata)
        ratio_all=pd.merge(ratio_all,ratio_subdata,on="Assembly")
    # to do explicitely declares which columns has to be rounded
    ratio_all=ratio_all.round(2)
    print (ratio_all)

    ratio_all.to_csv("ratio_all.tsv", sep="\t")

    # # max=len(ratio_all.index)
    # #
    # # for trip in ratio_all.columns:
    # #     trip_freq=list(ratio_all.loc[:,trip])
    # #     trip_freq=collections.Counter(trip_freq)
    # #     test=0
    # #     percent=0
    # #
    # #     while percent<0.9:
    # #         test=test+1
    # #         top=trip_freq.most_common(test)
    # #         percent=0
    # #         for freq in top:
    # #             percent=percent+(freq[1]/max)
    #
    #
    #     # print (trip_freq)
    #     # print (percent)
    #     # print (test)
    #     # print()
    #
    #
    #
    #
    # # print (ratio_all)
    # # print ()
    # # GCT_freq=list(ratio_all.loc[:,"GCT"])
    # # print (GCT_freq)
    # # print ()
    # # counter=collections.Counter(GCT_freq)
    # # print(counter)
    # # print(counter.values())
    # # print(counter.keys())
    # # print(counter.most_common(3))


if __name__ == "__main__":
    main()