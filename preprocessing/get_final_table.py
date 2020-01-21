#Author: Andreas Blaumeiser, Joint Research Centre F7 Unit, Ispra (Italy)
#Date: 2020-01-09

import argparse
import fractions
import numpy as np
import pandas as pd


def parse_table(inpath):
#Reads in the data from the input file.
#
#Parameters:
#inpath: path to the input file
#
#Output:
#data from the input file transformed into a Pandas dataframe
    
    data = pd.read_csv(
            inpath, sep='\t', index_col=False, low_memory=False
            )
    data = data.round(2)
    data.drop('Taxid', axis=1, inplace=True)
    data.set_index('Assembly', inplace=True)
    return data


def get_codon_distributions(data, code):
    
    codon_distributions = {}
    
    synonymous_codons = {
        'CYS': ['TGT', 'TGC'],
        'ASP': ['GAT', 'GAC'],
        'SER': ['TCT', 'TCG', 'TCA', 'TCC', 'AGC', 'AGT'],
        'GLN': ['CAA', 'CAG'],
        'MET': ['ATG'],
        'ASN': ['AAC', 'AAT'],
        'PRO': ['CCT', 'CCG', 'CCA', 'CCC'],
        'LYS': ['AAG', 'AAA'],
        'THR': ['ACC', 'ACA', 'ACG', 'ACT'],
        'PHE': ['TTT', 'TTC'],
        'ALA': ['GCA', 'GCC', 'GCG', 'GCT'],
        'GLY': ['GGT', 'GGG', 'GGA', 'GGC'],
        'ILE': ['ATC', 'ATA', 'ATT'],
        'LEU': ['TTA', 'TTG', 'CTC', 'CTT', 'CTG', 'CTA'],
        'HIS': ['CAT', 'CAC'],
        'ARG': ['CGA', 'CGC', 'CGG', 'CGT', 'AGG', 'AGA'],
        'TRP': ['TGG'],
        'VAL': ['GTA', 'GTC', 'GTG', 'GTT'],
        'GLU': ['GAG', 'GAA'],
        'TYR': ['TAT', 'TAC']
        }
    
    if code == 0:
        synonymous_codons['STOP'] = ['TAG', 'TGA', 'TAA']
    elif code == 1:
        synonymous_codons['STOP'] = ['TAA']
        synonymous_codons['SEC'] = ['TGA']
        synonymous_codons['PYL'] = ['TAG']
        
    #Calculate the threshold to filter underrepresented values
    nr_assemblies = len(data.index)
    limit = np.floor_divide(nr_assemblies, 100) + 1

    for amino_acid in synonymous_codons:
        #Extract the values for all codons that code for the amino acid
        codon_values = data[synonymous_codons[amino_acid]]
        #Count the absolute frequencies of all combinations of codon values
        frequencies = (
                codon_values.groupby(
                        synonymous_codons[amino_acid]).size().
                        reset_index(name='Frequency'
                                    )
                        )
        #Sort the codon sets according to their frequency
        sorted_freqs = frequencies.sort_values(by='Frequency', ascending=False)
        #Total number required to change absolute into realative frequencies
        old_total = sum(sorted_freqs['Frequency'])
        #Remove entries that occur less frequent than the limit
        sorted_freqs.drop(
                sorted_freqs[sorted_freqs.Frequency <= limit].index,
                inplace=True
                )
        #Transform the absolute values into relative ones
        sorted_freqs['Frequency'] = sorted_freqs['Frequency'].divide(old_total)
        new_total = sum(sorted_freqs['Frequency'].values)
        #Re-scale frequencies to sum up to 1 as it is a distribution
        sorted_freqs['Frequency'] = [
                fractions.Fraction(x/new_total).limit_denominator()
                for x in sorted_freqs['Frequency']
                ]
        sorted_freqs.reset_index(drop=True, inplace=True)
        codon_distributions[amino_acid] = sorted_freqs
    
    return codon_distributions


def build_table(distributions, nr):
#Creates a table of values for each pair of codons column picked randomly
#with a distribution according to all values in the column.
#
#Parameters:
#distributions: dictionary with the precalculated distributions for the columns
#nr: number of rows that the table should have
#
#Output:
#Pandas dataframe with the random values for each column
    
    sample_df = pd.DataFrame({'init': range(0,nr)})

    for amino_acid in distributions:
        codon_sample = (
                distributions[amino_acid]
                .sample(
                        n=nr, replace=True, 
                        weights=distributions[amino_acid]['Frequency']
                        )
                )
        codon_sample.drop('Frequency', axis=1, inplace=True)
        codon_sample.reset_index(drop=True, inplace=True)
        sample_df = sample_df.join(codon_sample)

    sample_df.drop('init', axis=1, inplace=True)
    return sample_df


def main():
    #Argument parsing
    parser = argparse.ArgumentParser(description='Codon usage sample tool.')
    parser.add_argument(
        '-i', '--input', metavar='INPUTFILE', default='/dev/stdin',
        help='The input file.'
    )
    parser.add_argument(
        '-o', '--output', metavar='OUTPUTFILE', default='/dev/stdout',
        help='The output file.'
    )
    parser.add_argument(
        '-r', '--rows', metavar='int', type=int, const=10000, default=10000,
        nargs='?', help='Number of rows for model training.'
    )
    parser.add_argument(
        '-c', '--code', metavar='int', type=int, const=0, default=0, nargs='?',
        help='Genetic code for twenty (0) or twenty-two (1) amino acids.'
    )

    args = parser.parse_args()
    
    #Definition of global parameters according to the command line arguments
    nr_rows = args.rows
    inpath = args.input
    outpath = args.output
    code = args.code

    #Read in data from input file
    table = parse_table(inpath)
    #Build the distributions for the columns
    distributions = get_codon_distributions(table, code)
    #Create the table with the random samples for each column
    training_data = build_table(distributions, nr_rows)
    #Write the table as .tsv to the output file
    training_data.to_csv(outpath, sep='\t', index=False)


if __name__ == '__main__':
    main()
