import itertools
import random
# from gspan import gSpan
# from closegraph import closeGraph

def convert_results_format(results):
    results_as_tuples = []
    for result in results:
        support, description, num_vertices = result[0], result[1], result[2]
        results_as_tuples.append((support, description, num_vertices))

    return results_as_tuples

def get_multiple_results(gs, max_subgraphs):
    results = []
    for bin in max_subgraphs:
        for dfscode_and_projection in bin:
            dfs_code = dfscode_and_projection[0]
            projection = dfscode_and_projection[1]
            counter = itertools.count()
            g = dfs_code.to_graph(gid=next(counter), is_undirected=True)

            support = str(gs._get_support(projection))
            description = g.display()
            num_vert = str(dfs_code.get_num_vertices())
            result = (support, description, num_vert)
            results.append(result)
    return results

def reduce_graph_dataset(graphs, graphs_to_keep):
    """
    graphs_to_keep must only have graphids that are valid
    """
    if graphs_to_keep is None:
        return graphs
    else:
        reduced_dataset = dict()
        for graphId in graphs_to_keep:
            reduced_dataset[graphId] = graphs[graphId]

        return reduced_dataset

def run_cg(file_name, supp, min_size_graph, graphs_to_keep):
    from closegraph import closeGraph
    cg = closeGraph(
        database_file_name=file_name,
        min_support=supp,
        min_num_vertices=min_size_graph,
        graphs_to_keep=graphs_to_keep
    )
    cg.run()
    results = cg._report_df.to_numpy().astype(str)
    results = convert_results_format(results)
    return results, cg

def run_ncg(file_name, supp, min_size_graph, graphs_to_keep):
    from gspan import gSpan
    gs = gSpan(
        database_file_name=file_name,
        min_support=supp,
        min_num_vertices=min_size_graph,
        graphs_to_keep=graphs_to_keep
    )
    gs.run()
    max_subgraphs = gs._max_subgraphs
    if max_subgraphs is None:
        results = []
    else:
        results = get_multiple_results(gs, max_subgraphs)
    return results,gs

def make_dict(results):
    res_dict = dict()
    for res in results:
        num_vert = res[2]
        if num_vert in res_dict:
            res_dict[num_vert] = res_dict[num_vert] + 1
        else:
            res_dict[num_vert] = 1
    return res_dict