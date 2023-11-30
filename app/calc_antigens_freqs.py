import pickle
import os
import timeit


def parse_input(threshold):
    path = 'static/input'
    loci_list = ['A', 'B', 'C', 'DQB1', 'DRB1']
    os.makedirs(path, exist_ok=True)
    folder = os.fsencode(path)

    dict_donors = {}
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith(('.csv')):
            with open(path + '/' + filename) as input_file:
                for line in input_file.readlines():
                    if "Antigen" in line:
                        continue
                    sample_id, antigen, assignment, strength = line.strip().split(',')[:4]
                    #sample_id, antigen, assignment = line.strip().split(',')[:3]
                    if sample_id not in dict_donors:
                        dict_donors[sample_id] = []
                    #if assignment == 'Positive':
                    if float(strength) >= threshold:
                        if antigen.split('*')[0] in loci_list:
                            dict_donors[sample_id].append(antigen)

    return dict_donors


def find_haps_with_antigens(graph, antigens_list):
    dict_haps_with_antigens = {}
    dict_haps_with_antigens_class1 = {}
    dict_haps_with_antigens_class2 = {}

    for antigen in antigens_list:
        if antigen in graph.nodes():
            class_antigen = 1 if antigen.split('*')[0] in ['A', 'B', 'C'] else 2
            hap_with_antigen = graph.adj[antigen]
            for hap in hap_with_antigen:

                freqs = graph.nodes[hap]['freq']
                dict_haps_with_antigens[hap] = freqs[0]
                if class_antigen == 1:
                    dict_haps_with_antigens_class1[hap] = freqs[0]
                else:
                    dict_haps_with_antigens_class2[hap] = freqs[0]

    return sum(dict_haps_with_antigens.values()), sum(dict_haps_with_antigens_class1.values()), \
           sum(dict_haps_with_antigens_class2.values()), len(dict_haps_with_antigens_class1), \
           len(dict_haps_with_antigens_class2)


def call_calc_antigens(pop='General_IL', string_input=None, Assume_HWE=False, threshold = 4000):
    # get fom the user
    if not Assume_HWE:
        graph = pickle.load(open('pkl/graph_muugs_freqs_' + pop + '.pkl', "rb"))
    else:
        graph = pickle.load(open('pkl/graph_haps_freqs_' + pop + '.pkl', "rb"))
    # antigens_file = 'Input/antigens.txt'
    os.makedirs('static/output/', exist_ok=True)
    file_res = open('static/output/probs_without_antigens_haps.csv', 'w+')
    if string_input:
        dict_donors = {}
        string_input = string_input.strip().split(';')
        dict_donors[string_input[0]] = string_input[1].split(',')
    else:
        dict_donors = parse_input(threshold)
    # with open(antigens_file) as file_input:
    # for line in file_input:
    file_res.write("Sample id,Class 1+2,Class 1,Class 2\n")
    for sample_id, antigens_list in dict_donors.items():

        # id, antigens_list = line.strip().split(',')
        # freq_missing = find_haps_with_antigens(graph, antigens_list.split(';'))
        freq_positive_all, freq_positive_class1, freq_positive_class2, num_from_class1, num_from_class2 = \
            find_haps_with_antigens(graph, antigens_list)
        if Assume_HWE:
            freq_positive_all = 1 - (1 - freq_positive_all) ** 2
            freq_positive_class1 = 1 - (1 - freq_positive_class1) ** 2
            freq_positive_class2 = 1 - (1 - freq_positive_class2) ** 2
        freq_positive_all, freq_positive_class1, freq_positive_class2 = \
            int(round(freq_positive_all, 2) * 100), int(round(freq_positive_class1, 2) * 100), int(
                round(freq_positive_class2, 2) * 100)
        file_res.write("{id},{freq_all}%,{freq_class1}%,{freq_class2}%\n".format
                       (id=sample_id, freq_all=freq_positive_all, freq_class1=freq_positive_class1,
                        freq_class2=freq_positive_class2))

    file_res.close()



call_calc_antigens(Assume_HWE=True)
