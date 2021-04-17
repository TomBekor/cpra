import pickle
import os
import timeit

def parse_input():
    path = 'input'
    loci_list = ['A', 'B', 'C', 'DQB1', 'DRB1']
    folder = os.fsencode(path)

    dict_donors = {}
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith(('.csv')):
            list_donor = []
            with open(path + '/' + filename) as input_file:
                for line in input_file:
                    sample_id, antigen, assignment = line.strip().split(',')[:3]
                    if assignment == 'Positive':
                        if antigen.split('*')[0] in loci_list:
                            list_donor.append(antigen)
            if list_donor:
                dict_donors[sample_id] = dict_donors.get(sample_id, []) + list_donor

    return dict_donors


def find_haps_with_antigens(graph, antigens_list):
    dict_haps_with_antigens = {}
    count = 0
    for antigen in antigens_list:
        if antigen in graph.nodes():
            hap_with_antigen = graph.adj[antigen]
            for hap in hap_with_antigen:
                if not hap in dict_haps_with_antigens:
                    freqs = graph.node[hap]['freq']
                    dict_haps_with_antigens[hap] = freqs
                    count += freqs[0]

    return 1 - count

def call_calc_antigens(pop = 'General_IL', string_input = None):
    #get fom the user
    graph = pickle.load(open('pkl/graph_haps_freqs_'+ pop + '.pkl', "rb"))
    #antigens_file = 'Input/antigens.txt'
    file_res = open('output/probs_without_antigens.csv', 'w')
    if string_input:
        dict_donors = {}
        string_input = string_input.strip().split(';')
        dict_donors[string_input[0]] = string_input[1].split(',')
    else:
        dict_donors = parse_input()
    #with open(antigens_file) as file_input:
        #for line in file_input:
    file_res.write("Sample id,Frequency of haplotypes without positive antigens\n")
    for sample_id, antigens_list in dict_donors.items():

            #id, antigens_list = line.strip().split(',')
            #freq_missing = find_haps_with_antigens(graph, antigens_list.split(';'))
            freq_missing = find_haps_with_antigens(graph, antigens_list)
            freq_missing = round(freq_missing, 3)
            file_res.write("{id},{freq_missing}\n".format( id=sample_id,freq_missing=freq_missing))


    file_res.close()


# call_calc_antigens()
