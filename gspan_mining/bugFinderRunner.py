import random
from bugFinder import run_ncg, run_cg, make_dict

graph_dataset_size = 340
file_name = "../graphdata/benchmark_tests/Chemical_340.txt"
supp = 2 #graph_dataset_size * 0.1
min_size_graph = 2
match = True
count = -1

while(match):
    # graphs_to_keep = [random.randint(0,graph_dataset_size-1) for _ in range(5)]
    # graphs_to_keep = [random.randint(0,graph_dataset_size-1) for _ in range(2)]
    graphs_to_keep = [90,188]
    ncg_results,ncg = run_ncg(file_name,supp,min_size_graph,graphs_to_keep)
    cg_results,cg = run_cg(file_name,supp,min_size_graph,graphs_to_keep)

    ncg_dict = make_dict(ncg_results)
    cg_dict = make_dict(cg_results)

    match = ncg_dict == cg_dict
    count+=1
    print("Count: {}\n Match: {}".format(count,match))

for gid in cg.graphs:
    cg.graphs[gid].plot()

#The two algs no longer have matching results
print("Dataset: ", graphs_to_keep)
print("ncg results: ", ncg_results)
print("cg results: ", cg_results)
print("ncg dict: ", ncg_dict)
print("cg dict: ", cg_dict)