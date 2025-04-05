import os
import re
import json
import networkx as nx
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO)

def extract_links(content):
    """Extract all [[filename]] links from markdown content"""
    pattern = r'\[\[(.*?)\]\]'
    return re.findall(pattern, content)


def build_content_graph(content_dir="src/content/docs"):
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
    print(graph)
    return graph, node_metadata


def depth_first_search(graph, start_node):
    stack = [start_node]

    while stack:
        node = stack.pop()
        logging.info(f"Visiting node: {node}")
        for neighbor in graph[node]:
            stack.append(neighbor)

    return


if __name__ == "__main__":
    # Build the graph using dictionary
    dict_graph, node_metadata = build_content_graph()

    # Print some statistics
    print(f"Graph contains {len(dict_graph)} nodes and {sum(len(edges) for edges in dict_graph.values())} edges")

    depth_first_search(dict_graph, "01-Sailing-deck")