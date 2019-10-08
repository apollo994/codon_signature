#Andreas

import os
import sys
import argparse
from collections import defaultdict
import pandas as pd
import numpy as np
import collections
import operator
from functools import reduce
import math
import numpy
import fractions

def parse_table(inpath):
    data = pd.read_csv(inpath, sep='\t', index_col=False, low_memory=False)
    return data

def get_column_distribution(data, limit):
    distributions = {}
    for column_name in data.columns:
        #print(column_name)
        freqs = {}
        column_values = data[column_name].values
        for value in column_values:
            try:
                freqs[value] += 1
            except:
                freqs[value] = 1
        #Transform absolute freqs into relative freqs
        total = reduce(lambda x,y: x+y, freqs.values())
        freqs = {freq: freqs[freq]/total for freq in freqs}
        #print(freqs)
        sorted_freqs = sorted(freqs.items(), key=operator.itemgetter(1, 0), reverse=True)
        #set to check which values have already been considered
        touched_values = set()
        #the highest percentage value
        max_percent = sorted_freqs[0][1]
        #find the list of all maxima
        maxima = []
        for tup in sorted_freqs:
            #print(tup)
            if tup[1] == max_percent:
                #print('Going to add {}'.format(tup))
                maxima.append(tup[0])
                touched_values.add(tup[0])
            else:
                #means no more maxima possible, no need to loop over the rest
                break

        #enter the values of the maxima for the column distribution
        #print(maxima)
        for mx in maxima:
            try:
                distributions[column_name][mx] = max_percent
            except:
                distributions[column_name] = {mx: max_percent}

        #check if the maxima already cover more than the threshold because then
        #no need to continue
        percentage = len(maxima)*max_percent
        if percentage >= limit:
            #print('enough!')
            continue

        #if the maxima do not cover the limit, extend the range of values
        else:
            #dictionary to keep track of the extension around the maxima
            maxima_dict = {maxi: {0: maxi - 0.01, 1: maxi + 0.01} for maxi in maxima}
            #print('before')
            #print(maxima_dict)
            def find_next_value(ptg):
                nbr_values = []
                #go through neighbors of all maxima to find new best value
                for maxi in maxima:
                    left = maxima_dict[maxi][0]
                    right = maxima_dict[maxi][1]
                    #print(left, right)
                    if not left in touched_values and left in freqs:
                        nbr_values.append(((maxi, 0), freqs[left]))
                    if not right in touched_values and right in freqs:
                        #touched_values.add(right)
                        #maxima_dict[maxi][1] += 0.01
                        nbr_values.append(((maxi, 1), freqs[right]))
                    #print('NBR')
                    #print(nbr_values)
                if nbr_values:
                    next_step = (sorted(nbr_values, key=operator.itemgetter(1), reverse=True))[0]
                    #print('next')
                    #print(next_step)                        #next_max = sorted(nbr_values)[0]
                    next_value = maxima_dict[next_step[0][0]][next_step[0][1]]
                    next_max = next_step[1]
                    #print(next_max)
                    #print(next_value)
                    #update list of touched values
                    touched_values.add(next_value)
                    #print(touched_values)
                    #update maxima_dict
                    curr_max = next_step[0][0]
                    nbr = next_step[0][1]
                    if nbr == 0:
                        new_left = round(maxima_dict[curr_max][0] - 0.01, 2)
                        maxima_dict[curr_max][0] = new_left
                    elif nbr == 1:
                        new_right = round(maxima_dict[curr_max][1] + 0.01, 2)
                        maxima_dict[curr_max][1] = new_right
                    #print('after')
                    #print(maxima_dict)
                    return (next_value, next_max)
                else:
                    return False
            while percentage < limit:
                #print(percentage)
                next_step = find_next_value(percentage)
                #print(next_step)
                if next_step:
                    distributions[column_name][next_step[0]] = next_step[1]
                    #print(distributions)
                    #old_percentage = percentage
                    #print('move on')
                    percentage = math.fsum([percentage, next_step[1]])
                    #percentage = round(percentage, 2)
                    #if percentage == old_percentage:
                        #print('STOP')
                        #break
                #limit cannot be reached because reached only zeros, stop extension
                else:
                    #distributions[column_name][next_step[0]] = freqs[next_step[0]]
                    break
            #distributions[column_name][next_step[0]] = freqs[next_step[0]]
            #print(distributions)
    return distributions

def build_table(distributions, nr):
    sample_dict = {}
    #re-scaling to 1 (since it is supposed to be a distribution)
    #Should be moved to get_column_distribution function
    for column in distributions:
        keys = list(distributions[column].keys())
        values = list(distributions[column].values())
        percent = reduce(lambda x,y: x+y, values)
        #norm_values = [round(value/percent, 2) for value in values]

        norm_values = [fractions.Fraction(value/percent).limit_denominator() for value in values]
        if reduce(lambda x,y: x+y, norm_values) != 1:
            print('numerical issue with {}'.format(column))
            #print(norm_values)
        else:
            sample = numpy.random.choice(keys, p=list(norm_values), size=nr)
            sample_dict[column] = sample

    sample_df = pd.DataFrame(sample_dict)
    #print(sample_df)
    return sample_df

def main():

    parser = argparse.ArgumentParser(description='My nice tool.')
    parser.add_argument('-i', '--input', metavar='INPUTFILE', default="/dev/stdin", help='The input file.')
    parser.add_argument('-o', '--output', metavar='OUTPUTFILE', default="/dev/stdout", help='The output file.')
    parser.add_argument('-r', '--rows', metavar='int', type=int, help='Number of rows for model training.', nargs='?', const=10000, default=10000)
    parser.add_argument('-t', '--threshold', metavar='float', type=float, help='Threshold for value inclusion.', nargs='?', const=0.9, default=0.9)
    args = parser.parse_args()

    threshold = args.threshold
    nr_rows = args.rows
    inpath = args.input
    outpath = args.output

    table = parse_table(inpath)
    distributions = get_column_distribution(table, threshold)
    #print(distributions)
    # for column in distributions:
    #     pct = reduce(lambda x,y: x+y, distributions[column].values())
    #     #print(column)
    #     print(column, round(pct, 2))
    #     print(distributions[column].keys())
    #print(distributions)
    training_data = build_table(distributions, nr_rows)
    #print(training_data)
    #Write output
    training_data.to_csv(outpath, sep='\t', index=False)

if __name__ == "__main__":
    main()
