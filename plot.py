import networkx as nx
import plotly.graph_objects as go

def plot(X, clustering_coeff, neighborhood_overlap, graph):
    G = nx.read_gml(graph)

    # Plot the edges
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    # Plot the nodes
    node_x = []
    node_y = []
    clustering_coeff = []   
    neighborhood_overlap = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

        # # Calculate clustering coefficient for each node
        # clustering_coeff.append(nx.clustering(G)) 

        # # Calculate neighborhood overlap for each node
        # neighborhood_overlap.append(G.degree[node])

    if X == "C":
    # Visualize clustering coefficient (node size = cc, color = degree)
        edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

        node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title=dict(
                text='Node Connections',
                side='right'
                ),
                xanchor='left',
            ),
            line_width=2))
        
        degree = []
        node_text = []
        for node, adjacencies in enumerate(G.adjacency()):
            degree.append(len(adjacencies[1]))
            node_text.append('degree: '+str(len(adjacencies[1])))

        node_trace.marker.color = degree    # node color = degree
        node_trace.marker.size = clustering_coeff     # node size = clustering coeff.
        node_trace.text = node_text

    elif X == "N":
    # Visualize neighborhood overlap (edge thickness = NO, color = sum of degrees at end points)
        edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

        node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title=dict(
                text='Node Connections',
                side='right'
                ),
                xanchor='left',
            ),
            line_width=2))
        
        degree = []
        node_text = []
        for node, adjacencies in enumerate(G.adjacency()):
            degree.append(len(adjacencies[1]))
            node_text.append('degree: '+str(len(adjacencies[1])))

        edge_trace.marker.color = degree    
        edge_trace.marker.size = neighborhood_overlap   
        node_trace.text = node_text

    elif X == "P":
    # Plot the attributes (node color, edge signs)
        edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

        node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title=dict(
                text='Node Connections',
                side='right'
                ),
                xanchor='left',
            ),
            line_width=2))
        
        edge_color = []
        node_color = []
        edge_text = []
        node_text = []

        # Setting node color
        for node in G.nodes():
            node_text.append(node.label)
            node_color.append("blue")
            
        
        # Labeling edge signs and setting their colors
        for edge in G.edges():
            edge_text.append('sign: '+ edge.sign)

            if edge.color == "r":
                edge_color = "red"
            elif edge.color == "g":
                edge_color = "green"


        edge_trace.marker.color = edge_color   
        edge_trace.text = edge_text
        node_trace.marker.color = node_color

    
    fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title=dict(
                        text="<br>Network Graph",
                        font=dict(
                            size=16
                        )
                    ),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    fig.show()

    return