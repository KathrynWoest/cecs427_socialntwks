import networkx as nx
import itertools

def components(n, graph, output_components=False):
    # girvan_newman() returns an interator that yields a sequence of communities at each level
    communities_iterator = nx.community.girvan_newman(graph)

    # ensure n (number of components) is an integer
    try:
        n = int(n)
    except:
        print(f"{n} is not able to be converted into an integer, so removal of k edges is not possible. Simulating failures terminated.\n---")
        return

    # stop the iteration when number of communities exceeds n (yields tuples of sets)
    n_iterations = itertools.takewhile(lambda c: len(c) <= n, communities_iterator)

    # take the last result (the partition with n components, less than n if n exceeds maximum number of components for the graph)
    partition = None
    for communities in n_iterations:
        partition = communities

    if partition is None:
        print(f"Could not find a partition with <= {n} components.")
        return
    
    print(f"Graph partitioned into {len(partition)} components:")
    for i, comm in enumerate(partition):
        print(f"  Component {i+1}: {comm}")

        if output_components:
            subgraph = graph.subgraph(comm).copy()
            nx.write_gml(subgraph, f"component_{i+1}.gml")      # Export component to .gml
    
    return partition