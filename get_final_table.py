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
        sorted_freqs = sorted(freqs.items(), key=operator.itemgetter(1, 0), reverse=True)        
        percentages = {}
        
        for freq in freqs:
            try:
                percentages[freqs[freq]].add(freq)
            except:
                percentages[freqs[freq]] = set([freq])
        #print(percentages)
        percentages_sorted = sorted(percentages.keys(), reverse=True)
        max_percent = percentages_sorted[0]
        #print(max_percent)
        maxima = percentages[percentages_sorted[0]]
        percentage = max_percent
        if len(maxima) == 1:
            maximum = percentages[percentages_sorted[0]].pop()
            distributions[column_name] = {maximum: percentage}
            #maximum already covers column
            if percentage >= limit:
                continue
            #limit not reached, range of values has to be extended around the maximum
            else:
                left = maximum - 0.01
                right = maximum + 0.01
                proceed = True
                while percentage < limit and proceed:
                    if left in freqs:
                        left_value = freqs[left]
                    else:
                        left_value = 0
                    if right in freqs:
                        right_value = freqs[right]
                    else:
                        right_value = 0
                    next_ptg = max(left_value, right_value)
                    print(next_ptg)
                    if next_ptg == 0:
                        print('out')
                        proceed = False
                    else:
                        if next_ptg == left_value:
                            left -= 0.01
                        elif next_ptg == right_value:
                            right += 0.01
                    percentage += next_ptg
                else:
                    continue
        print(column_name)    
        
            #print('Maximum')
            #print(maximum.pop() )
        #print(maxima)
        #sort the frequencies to easily find the maxima
        sorted_freqs = sorted(freqs.items(), key=operator.itemgetter(1, 0), reverse=True)
        #print(sorted_freqs)
        #set to check which values have already been considered
        touched_values = set()
        #the highest percentage value
        max_percent = sorted_freqs[0][1]
        #find the list of all maxima
        maxima = []        #print(max_percent)
        for tup in sorted_freqs:
            #print(tup)
            if tup[1] == max_percent:
                #print('Going to add {}'.format(tup))
                maxima.append(tup[0])
                touched_values.add(tup[0])
            #else:
                #means no more maxima possible, no need to loop over the rest
                #break

        #enter the values of the maxima for the column distribution        
        for mx in maxima:
            try:
                distributions[column_name][mx] = max_percent
            except:
                distributions[column_name] = {mx: max_percent}
        
#       #check if the maxima already cover more than the threshold because then
                #no need to continue
        percentage = len(maxima)*max_percent        
        if percentage >= limit:
            #print('enough!')
            continue
        
        #if the maxima do not cover the limit, extend the range of values        
        else:
            #dictionary to keep track of the extension around the maxima
            maxima_dict = {maxi: [maxi - 0.01, maxi + 0.01] for maxi in maxima}
            
            
            
            
            
            print(maxima_dict)
            def find_next_value(ptg):
                nbr_values = {}
                #go through neighbors of all maxima to find new best value
                for maxi in maxima:
                    left = maxima_dict[maxi][0]
                    right = maxima_dict[maxi][1]
                    if not left in touched_values and left in freqs:
                        #touched_values.add(left)
                        #maxima_dict[maxi][0] -= 0.01
                        try:
                            nbr_values[freqs[left]].append(left) 
                        except:
                            nbr_values[freqs[left]] = [left]
                    
                    if not right in touched_values and right in freqs:
                        #touched_values.add(right)
                        #maxima_dict[maxi][1] += 0.01
                        try:
                            nbr_values[freqs[right]].append(right) 
                        except:
                            nbr_values[freqs[right]] = [right]
                    #print(nbr_values)
                    if nbr_values:
                        next_max = sorted(nbr_values)[0]
                        next_value = nbr_values[next_max][0]
                        #print(next_max)
                        #print(next_value)
                        return (next_value, next_max)
                    else:
                        return False
            if percentage < limit:
                next_step = find_next_value(percentage)
                if next_step:
                    #print('move on')
                    percentage += next_step[1]
                #limit cannot be reached, stop extension
                else:
                    #distributions[column_name][next_step[0]] = freqs[next_step[0]]
                    continue
            distributions[column_name][next_step[0]] = freqs[next_step[0]]
            #print(distributions)
    return distributions            
        #rel_freqs = {values[0]: values[1]/total for values in sorted_abs_freqs}
        #print(rel_freqs)
        #print(column_name)
        #print(sorted_freqs)
        #index = 0
        #max_value = sorted_freqs[index]
        #percentage = max_value[1]
        #print(percentage)
        #print(max_value)
        #if percentage >= limit:
            #distributions[column_name] = {max_value[0]: max_value[1]}
        #else:
            #print(percentage)
            #while percentage < limit:
                #try:
                    #print('1')
                    #distributions[column_name][max_value[0]] = max_value[1]
                    #print('2')
                #except:
                    #distributions[column_name] = {max_value[0]: max_value[1]}
                #index += 1
                #max_value = sorted_freqs[index]
                #percentage += max_value[1]
                #print(percentage)
            #distributions[column_name][max_value[0]] = max_value[1]

            #distributions[max_value[0]] = 1.0
        #distributions[column_name] = sorted(abs_freqs)
        #freqs.clear()


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
    #parser.add_argument('--id', metavar='ID',help='RefSeq tax ID',type=int)
    parser.add_argument('-o', '--output', metavar='OUTPUTFILE', default="/dev/stdout", help='The output file.')
    args = parser.parse_args()

    threshold = 0.9
    nr_rows = 10

    inpath = args.input
    outpath = args.output

    table = parse_table(inpath)
    distributions = get_column_distribution(table, threshold)
    #print(distributions)
    #training_data = build_table(distributions, nr_rows)
    #print(training_data)
    #Write output
    #training_data.to_csv(outpath, sep='\t', index=False)
    #print(list(table.columns)[2:])
    #for column in table.columns[2:]:
    #    print(table[column])
    #print(table.columns[2:])

if __name__ == "__main__":
    main()
