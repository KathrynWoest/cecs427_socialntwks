import networkx as nx
import random
import copy

def robustness_check(graph, k, simulations=100):
    G_original = graph

    # Store original clusters
    original_components = list(nx.connected_components(G_original))

    component_counts = []
    max_sizes = []
    min_sizes = []
    cluster_persistence_results = []

    edges = list(G_original.edges())

    # ensure k is an integer
    try:
        k = int(k)
    except:
        print(f"{k} is not able to be converted into an integer, so removal of k edges is not possible. Simulating failures terminated.\n---")
        return

    for _ in range(simulations):

        # Copy graph so original remains unchanged
        G = G_original.copy()

        # Remove k random edges
        removed_edges = random.sample(edges, min(k, len(edges)))
        G.remove_edges_from(removed_edges)

        # Compute new components
        new_components = list(nx.connected_components(G))

        component_counts.append(len(new_components))

        sizes = [len(c) for c in new_components]
        max_sizes.append(max(sizes))
        min_sizes.append(min(sizes))

        # Check cluster persistence
        persists = clusters_persist(original_components, new_components)
        cluster_persistence_results.append(persists)

    # Final statistics
    results = {
        "average_num_components": sum(component_counts) / simulations,
        "max_component_size": max(max_sizes),
        "min_component_size": min(min_sizes),
        "cluster_persistence_rate": sum(cluster_persistence_results) / simulations
    }

    print("ROBUSTNESS_CHECK")
    for result in results:
        print(f"{result}: {results[result]}")
    print('---')
    return results


def clusters_persist(original_components, new_components):
    for original in original_components:
        found = False
        for new in new_components:
            if original.issubset(new):
                found = True
                break
        if not found:
            return False
    return True