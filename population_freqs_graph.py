import networkx as nx
import pickle
import pathlib
#convert haps list of 2 field to 1 field
def convert_to_low_res(hpf_file):
    dict_hap_freq = {}
    with open(hpf_file) as hpf_info:
        for line in hpf_info:
            hap, _, freq = line.strip().split(',')
            """hap = hap.split('~')
            for i in range(len(hap)):
                hap[i] = hap[i].split(':')[0]
            hap = ('~').join(hap)"""
            dict_hap_freq[hap] = dict_hap_freq.get(hap, 0) + float(freq)

    return dict_hap_freq


#crate edges between haplotypes and their allels
def create_graph(hpf_file, pop):
    graph = nx.Graph()
    with open(hpf_file) as hpf_info:
        for line in hpf_info:
            if 'hap' in line:
                continue
            hap, _, freq = line.strip().split(',')

            freq = str(freq) ###option to list of races
            graph.add_node(hap, freq=list(map(float, freq.split(";"))))
            alleles_list = hap.split('~')
            """new_allele_list = []
            for allele in alleles_list:
                new_allele_list.append(allele)
                if allele in dict_antigen_tranlation:
                    new_allele_list.append(dict_antigen_tranlation[allele])"""

            for allele in alleles_list:
                if not allele in graph.nodes():
                    graph.add_node(allele)
                graph.add_edge(allele, hap)

    pickle.dump(graph, open('pkl/graph_haps_freqs_' + pop+ '.pkl', "wb"))

def antigen_with_same_interpretation(file_ser_ser):
    dict_allele_antigen = {}
    with open(file_ser_ser) as info_file:
        for line in info_file:
            if not line.startswith('#'):
                line = line.strip().split(';')
                if len(line[1]) == 1:
                    line[1] = '0' + line[1]
                for i in range(2,len(line)):
                    if line[i] !='':
                        alleles = line[i].split('/')
                        for allele in alleles:
                            dict_allele_antigen[line[0] + '*' + allele] = line[0] + '*' + line[1]

    info_file.close()
    return dict_allele_antigen


# Create output directory if it doesn't exist
pathlib.Path('pkl').mkdir(parents=False, exist_ok=True)

pops_list = ['Kavkaz','Ashkenazi', 'Ethiopian', 'Sephardi', 'Others', 'Arab' , "General_IL",
    "AFB",
    "AINDI",
    "AISC",
    "ALANAM",
    "AMIND",
    "CARB",
    "CARHIS",
    "CARIBI",
    "HAWI",
    "FILII",
    "KORI",
    "JAPI",
    "MSWHIS",
    "MENAFC",
    "NAMER",
    "NCHI",
    "SCAHIS",
    "SCAMB",
    "SCSEAI",
    "VIET",
    "AFA",
    "API",
    "CAU",
    "HIS",
    "NAM"
]
#dict_hap_freq = convert_to_low_res('data/Israel_SR_res.csv')
#dict_antigen_tranlation = {}
#dict_antigen_tranlation = antigen_with_same_interpretation('data/rel_ser_ser.txt')
for pop in pops_list:
    create_graph('data/' + pop + '_hpf.csv', pop)
