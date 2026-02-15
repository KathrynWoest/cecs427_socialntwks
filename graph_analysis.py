## NOTE: this file reuses a lot of code from Project 1

import sys
import fileio as fio
import components as comp
import visualization as vis
import homophily as hom
import balanced_graph as bal
import simulation as sim

# TODO: robustness_check k needs to be repeated several times, but i want to reuse the removal with simulate_failures. implement removal, then come back to properly show this on main


def main():
    # get arguments from command line and initialize BFS node list, the end of the argument list, and bools for which analyses were called
    args = sys.argv
    end = len(args)

    # if there are less than 2 arguments, then not possible to do anything. terminate program.
    if end < 2:
        raise Exception(f"Program was terminated because there is no file to upload a graph with.")
    
    # parse in graph from given .gml file
    user_graph = fio.parse_graph(args[1])

    # call the components function
    if "--components" in args:
        # check if the number of components is missing. if so, terminate program.
        if (args.index("--components") + 1 >= end) or ("--" in args[args.index("--components") + 1]):
            raise Exception("Program was terminated because it was missing the number of components for partitioning.")
        
        n = args[args.index("--components") + 1]
        # check if each component should be exported to a separate .gml file
        if "--split_output_dir" in args:
            comp.partition(user_graph, n, True)
        else:
            comp.partition(user_graph, n)
        
        # check if robustness check should occur
        if "--robustness_check" in args:
            # check if k is missing. if so, terminate program.
            if (args.index("--robustness_check") + 1 >= end) or ("--" in args[args.index("--robustness_check") + 1]):
                raise Exception("Program was terminated because it was missing the number of components for partitioning.")
            
            k = args[args.index("--robustness_check") + 1]

            reduced_graph = comp.removal(user_graph, k)
            comp.partition(reduced_graph, n)
    
    # call the visualization function
    if "--plot" in args:
        # check if vis output control is missing. if so, terminate program.
        if (args.index("--plot") + 1 >= end) or ("--" in args[args.index("--plot") + 1]):
                raise Exception("Program was terminated because it was missing the plot control argument.")
        
        control = args[args.index("--plot") + 1]
        if control not in ["C", "N", "P"]:
            raise Exception("Program was terminated because the plot control argument was not C, N, or P.")
        
        vis.plot(user_graph, control)

    # call the homophily function
    if "--verify_homophily" in args:
        hom.verify_hom(user_graph)

    # call the balanced graph function
    if "--verify_balanced_graph" in args:
        bal.verify_bal(user_graph)
    
    # call the output function
    if "--output" in args:
        # check if the output file name is missing. if so, terminate program.
        if (args.index("--output") + 1 >= end) or ("--" in args[args.index("--output") + 1]):
                raise Exception("Program was terminated because it was missing the output file name argument.")
        
        output_file = args[args.index("--output") + 1]

        fio.save_graph(user_graph, output_file)

    # call the simulate failures function
    if "--simulate_failures" in args:
        # check if k is missing. if so, terminate program.
        if (args.index("--simulate_failures") + 1 >= end) or ("--" in args[args.index("--simulate_failures") + 1]):
                raise Exception("Program was terminated because it was missing the number of removal edges argument.")
        
        k = args[args.index("--simulate_failures") + 1]
        reduced_graph = comp.removal(user_graph, k)
        comp.failures(user_graph, reduced_graph)
    
    # call the temporal simulation function
    if "--temporal_simulation" in args:
         # check if the simulation file is missing. if so, terminate program.
        if (args.index("--temporal_simulation") + 1 >= end) or ("--" in args[args.index("--temporal_simulation") + 1]):
                raise Exception("Program was terminated because it was missing the simulation file argument.")
        
        sim_file = args[args.index("--temporal_simulation") + 1]
        sim.animate(user_graph, sim_file)

main()