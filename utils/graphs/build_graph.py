import os
import re
import json
import networkx as nx
import matplotlib.pyplot as plt


def extract_links(content):
    """Extract all [[filename]] links from markdown content"""
    pattern = r'\[\[(.*?)\]\]'
    return re.findall(pattern, content)


def build_content_graph(content_dir="src/content/docs"):
    """Build a graph representation of content files and their links"""
    graph = nx.DiGraph()

    # Walk through all markdown files
    for root, _, files in os.walk(content_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                node_id = os.path.splitext(file)[0]

                # Add node to graph
                graph.add_node(node_id, path=file_path)

                # Extract links from content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    links = extract_links(content)

                    # Add edges for each link
                    for link in links:
                        graph.add_edge(node_id, link)

    return graph


def visualize_graph(graph, output_path="public/graph.png"):
    """Create a visualization of the content graph"""
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', 
            node_size=1500, edge_color='gray', arrows=True)
    plt.savefig(output_path)

    # Also save as JSON for interactive visualization
    graph_data = {
        "nodes": [{"id": node, "path": graph.nodes[node].get("path", "")} 
                 for node in graph.nodes],
        "links": [{"source": u, "target": v} for u, v in graph.edges]
    }

    with open("public/graph.json", "w") as f:
        json.dump(graph_data, f)


def build_content_graph_with_dict(content_dir="src/content/docs"):
    """Build a graph representation of content files and their links using a dictionary"""
    # Main adjacency list - node_id -> list of outgoing links
    graph = {}
    # Store node metadata separately
    node_metadata = {}
    
    # Walk through all markdown files
    for root, _, files in os.walk(content_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                node_id = os.path.splitext(file)[0]
                
                # Initialize the adjacency list for this node
                if node_id not in graph:
                    graph[node_id] = []
                
                # Store node metadata
                node_metadata[node_id] = {"path": file_path}
                
                # Extract links from content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    links = extract_links(content)
                    
                    # Add edges for each link
                    for link in links:
                        # Add the link to this node's adjacency list
                        graph[node_id].append(link)
                        
                        # Ensure the target node exists in the graph
                        if link not in graph:
                            graph[link] = []
                            # Create metadata entry for link if it doesn't have a file yet
                            if link not in node_metadata:
                                node_metadata[link] = {"path": ""}
    
    return graph, node_metadata


def visualize_dict_graph(graph, node_metadata, output_path="public/graph.json"):
    """Save the dictionary-based graph as JSON for visualization"""
    # Convert to the format needed for visualization
    graph_data = {
        "nodes": [{"id": node, "path": node_metadata[node].get("path", "")} 
                 for node in graph.keys()],
        "links": [{"source": node, "target": target} 
                 for node in graph 
                 for target in graph[node]]
    }
    
    with open(output_path, "w") as f:
        json.dump(graph_data, f, indent=2)
    
    # If you still want to use NetworkX for visualization:
    nx_graph = nx.DiGraph()
    
    # Add nodes with attributes
    for node, metadata in node_metadata.items():
        nx_graph.add_node(node, **metadata)
    
    # Add edges
    for node, targets in graph.items():
        for target in targets:
            nx_graph.add_edge(node, target)
    
    # Create visualization
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(nx_graph)
    nx.draw(nx_graph, pos, with_labels=True, node_color='lightblue', 
            node_size=1500, edge_color='gray', arrows=True)
    plt.savefig(output_path.replace('.json', '.png'))
    
    return nx_graph


if __name__ == "__main__":
    # Build the graph using dictionary
    dict_graph, node_metadata = build_content_graph_with_dict()
    
    # Visualize and convert to NetworkX if needed
    nx_graph = visualize_dict_graph(dict_graph, node_metadata)
    
    # Print some statistics
    print(f"Graph contains {len(dict_graph)} nodes and {sum(len(edges) for edges in dict_graph.values())} edges")
