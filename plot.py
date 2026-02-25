import networkx as nx
import plotly.graph_objects as go
from cluster import clustering_coefficient
from neighborhood import neighborhood_overlap
import os
import webbrowser

def plot(mode, graph, clustering_coeff=None, n_overlap=None):
    """
    Plots and visualizes the given graph in one of three modes: `C` (clustering coefficient), `N` (neighborhood overlap),
    or `P` (graph attributes).
    
    Parameters:
        - mode (str): the letter that specifies the plotting mode
        - graph (NetworkX graph): the graph to be visualized
        - clustering_coeff (int): the clustering coefficient for a specified node
        - n_overlap (int): the neighborhood overlap between two specified nodes

    Outputs:
        - html file: visualized graph in HTML format
    """
    
    G = graph

    # Get node positions
    pos = nx.get_node_attributes(G, 'pos')

    if not pos:
        pos = nx.spring_layout(G, seed=42)

    node_x = [pos[n][0] for n in G.nodes()]
    node_y = [pos[n][1] for n in G.nodes()]

    # Set default visual settings
    node_size = [10] * G.number_of_nodes()
    node_color = ["blue"] * G.number_of_nodes()
    node_text = []

    edge_traces = []

    if mode == "C":
    # Visualize clustering coefficient (node size = cc, color = degree)
        if clustering_coeff is None:
            raise ValueError("Clustering coefficient data required for mode 'C'.")

        degree = dict(G.degree())

        cc_values = {}
        for n in G.nodes():
            cc = clustering_coefficient(G, n, True) or 0.0
            cc_values[n] = cc
            node_size.append(cc * 40 + 10)

        node_color = [
            degree[n]
            for n in G.nodes()
        ]

        node_text = [
            f"Node: {n}<br>Degree: {degree[n]}<br>CC: {cc_values[n]:.3f}"
            for n in G.nodes()
        ]

        # Uniform edges
        edge_x, edge_y = [], []
        for u, v in G.edges():
            edge_x += [pos[u][0], pos[v][0], None]
            edge_y += [pos[u][1], pos[v][1], None]

        edge_traces.append(
            go.Scatter(
                x=edge_x,
                y=edge_y,
                mode="lines",
                line=dict(width=1, color="gray"),
                hoverinfo="none"
            )
        )

    elif mode == "N":
    # Visualize neighborhood overlap (edge thickness = NO, color = sum of degrees at end points)
        if n_overlap is None:
            raise ValueError("Neighborhood overlap data required for mode 'N'.")

        degree = dict(G.degree())

        for u, v in G.edges():
            overlap = neighborhood_overlap(G, u, v, True) or 0.0
            width = overlap * 10 + 1
            degree_sum = degree[u] + degree[v]

            # Add each edge one by one
            edge_traces.append(
                go.Scatter(
                    x=[pos[u][0], pos[v][0]],
                    y=[pos[u][1], pos[v][1]],
                    mode="lines",
                    line=dict(width=width, color=f"rgba(0,0,255,{overlap})"),
                    hoverinfo="text",
                    text=f"Overlap: {overlap:.3f}<br>Degree Sum: {degree_sum}"
                )
            )

        node_text = [
            f"Node: {n}<br>Degree: {degree[n]}"
            for n in G.nodes()
        ]

    elif mode == "P":
    # Plot the attributes (node color, edge signs)
        for u, v in G.edges():
            sign = G.edges[u, v].get("sign", "unknown")

            if sign == "+":
                color = "green"
            elif sign == "-":
                color = "red"
            else:
                color = "gray"

            # Add each edge one by one
            edge_traces.append(
                go.Scatter(
                    x=[pos[u][0], pos[v][0]],
                    y=[pos[u][1], pos[v][1]],
                    mode="lines",
                    line=dict(width=2, color=color),
                    hoverinfo="text",
                    text=f"Sign: {sign}"
                )
            )

        node_color = [
            G.nodes[n].get("color", "blue")
            for n in G.nodes()
        ]

        node_color = ["red" if color == "r" else "green" if color == "g" else color for color in node_color]

        node_text = [
            f"Node: {n}<br>Color: {G.nodes[n].get('color', 'blue')}"
            for n in G.nodes()
        ]

    else:
        raise ValueError("Mode must be one of: C, N, P")

    # Plot nodes
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        text=node_text,
        marker=dict(
            size=node_size,
            color=node_color,
            colorscale="YlGnBu" if mode == "C" else None,
            showscale=(mode == "C"),
            line_width=2
        )
    )

    # Generate graph
    fig = go.Figure(
        data=edge_traces + [node_trace],
        layout=go.Layout(
            title="Network Graph",
            showlegend=False,
            hovermode="closest",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        )
    )

    file_path = os.path.abspath("graph.html")
    fig.write_html("file_path", auto_open=False)
    webbrowser.open("file://" + file_path)