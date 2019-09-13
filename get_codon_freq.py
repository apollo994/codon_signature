#!/usr/bin/env python3
# Fabio Zanarello, JRC-ispra, 2019


import os
import sys
import argparse
from collections import defaultdict
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description='My nice tool.')
    parser.add_argument('--input', metavar='INPUTFILE', default="/dev/stdin", help='The input file.')
    parser.add_argument('--output', metavar='OUTPUTFILE', default="/dev/stdout", help='The output file.')
    args = parser.parse_args()

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

    #print (genecode)

    data=pd.read_csv(args.input, sep="\t")

    #sub_data=data.loc[:,["Assembly"]+genecode["A"]]
    #sub_data.set_index("Assembly")
    sub_data=data.loc[:,genecode["A"]]
    
    ratio_subdata=sub_data.div(sub_data.sum(axis=1), axis=0))

    print (data)
    print()
    print (sub_data)



# #    for index, row in data.iterrows():
# #        print(row["TTT"])
#     testsum = data["GCT"] + data["GCC"]
#     #print(testsum)
#     buff=pd.DataFrame()
#
#
#     for codon in genecode["A"]:
#         buff.append((codon,list(data[codon].values)))
#
#     print (buff)
#
#     for i in [j[1] for j in buff]:
#         print (i)
#
#     #print(x[1] for x in buff)
#
#     #print (summ_buff)
#
#     #    print (codon)
#     #    for value in data[codon]:
#     #        print (value)
#         #print(data.loc(codon))
#
#
#     #print (data.columns)
#
#
#     #print (data)






if __name__ == "__main__":
    main()
