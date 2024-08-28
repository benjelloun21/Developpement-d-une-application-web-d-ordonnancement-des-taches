import networkx as nx
import matplotlib.pyplot as plt
from .models import task
from django.shortcuts import render

# Filtrage des prédécesseurs directs
Collection_Predecessors = []  # Collection_Predecessors supposed to contain all attributes by the end of table_filling

def get_tasks_from_db():
    tasks = {}
    for t in task.objects.all():
        attribute = t.Attribute
        duration = t.Duration
        all_predecessors = t.get_predecessors_list()  # all_predecessors  mean DIRECT and NOTDIRECT predecessors
        predecessors = []  # predecessors mean DIRECT_PREDECESSORS

        for pred in all_predecessors:
            if pred not in Collection_Predecessors:
                predecessors.append(pred)
            else:
                Collection_Predecessors.append(pred)

        tasks[attribute] = {'duration': duration, 'predecessors': predecessors}
    return tasks

def create_graph():
    tasks = get_tasks_from_db()
    G = nx.DiGraph()
    for attribute, details in tasks.items():
        G.add_node(attribute, duration=details['duration'])
        for pred in details['predecessors']:
            G.add_edge(pred, attribute)

    # Add the "FIN" node
    G.add_node("FIN", duration=0)
    
    # Add edges from tasks with no successors to "FIN"
    for attribute in list(G.nodes):
        if G.out_degree(attribute) == 0 and attribute != "FIN":
            G.add_edge(attribute, "FIN", duration=G.nodes[attribute]['duration'])
    
    return G

def calculate_earliest_start():
    G = create_graph()
    earliest_start = {task: 0 for task in G.nodes}  # Initialize all tasks with earliest start time of 0
    for task in nx.topological_sort(G):
        if task in G.nodes and G.in_edges(task):
            earliest_start[task] = max(
                earliest_start[pred] + G.nodes[pred].get('duration', 0)
                for pred in G.predecessors(task)
            )
    return earliest_start

def calculate_latest_start(earliest_start):
    G = create_graph()
    latest_start = {}
    for task in reversed(list(nx.topological_sort(G))):
        if G.out_edges(task):
            latest_start[task] = min(latest_start[succ] - G.nodes[task].get('duration', 0) for succ in G.successors(task))
        else:
            latest_start[task] = earliest_start[task]
    return latest_start

def identify_critical_path(earliest_start, latest_start):
    return [task for task in earliest_start if earliest_start[task] == latest_start[task]]

def calculate_total_float(earliest_start, latest_start):
    total_float = {}
    for task in earliest_start:
        if task != "FIN":
            total_float[task] = latest_start[task] - earliest_start[task]
    return total_float

def calculate_free_float(earliest_start):
    G = create_graph()
    free_float = {}
    for task in earliest_start:
        if task != "FIN":
            successors = list(G.successors(task))
            if successors:
                free_float[task] = min(earliest_start[succ] - earliest_start[task] - G.nodes[task].get('duration', 0) for succ in successors)
            else:
                free_float[task] = float('inf')
    return free_float

def critical_path_view(request):
    earliest_start = calculate_earliest_start()
    latest_start = calculate_latest_start(earliest_start)
    total_float = calculate_total_float(earliest_start, latest_start)
    free_float = calculate_free_float(earliest_start)

    items = task.objects.all()

    context = {
        'items': items,
        'earliest_start': earliest_start,
        'latest_start': latest_start,
        'total_float': total_float,
        'free_float': free_float
    }
    return render(request, 'critical_path.html', context)

def visualize_graph(earliest_start, latest_start, critical_path):
    # Compute the levels of nodes
    G = create_graph()
    levels = {}
    for node in nx.topological_sort(G):
        if G.in_degree(node) == 0:
            levels[node] = 0
        else:
            levels[node] = max(levels[pred] + 1 for pred in G.predecessors(node))
    
    # Generate positions for nodes
    pos = {}
    level_counts = {}
    for node, level in levels.items():
        if level not in level_counts:
            level_counts[level] = 0
        pos[node] = (level, -level_counts[level])  # Arrange nodes in vertical levels
        level_counts[level] += 1
    
    # Draw the graph
    node_labels = {node: f"{node}\nES: {earliest_start[node]}\nLS: {latest_start[node]}" for node in G.nodes}
    edge_labels = {(u, v): f"{G.nodes[u].get('duration', 0)}" for u, v in G.edges}
    
    plt.figure(figsize=(12, 8))
    
    # Draw edges
    nx.draw(G, pos, with_labels=True, labels=node_labels, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold', node_shape='s')
    
    # Draw edge labels first to ensure they are not covered by the red edges
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    
    # Highlight critical path
    critical_edges = [(u, v) for u, v in zip(critical_path, critical_path[1:])]
    nx.draw_networkx_edges(G, pos, edgelist=critical_edges, edge_color='red', width=2)
    
    # Highlight critical path nodes with different color outline
    nx.draw_networkx_nodes(G, pos, nodelist=critical_path, node_color='lightblue', edgecolors='red', node_size=3000, node_shape='s', linewidths=2)
    
    plt.show()

def main():
    G = create_graph()
    earliest_start = calculate_earliest_start()
    latest_start = calculate_latest_start(earliest_start)
    critical_path = identify_critical_path(earliest_start, latest_start)
    total_float = calculate_total_float(earliest_start, latest_start)
    free_float = calculate_free_float(earliest_start)
    
    print("\nEarliest Start Times:", earliest_start)
    print("Latest Start Times:", latest_start)
    print("Critical Path (excluding 'FIN'):", critical_path)
    print("Total Floats (excluding 'FIN'):", total_float)
    print("Free Floats (excluding 'FIN'):", free_float)
    
    visualize_graph(earliest_start, latest_start, critical_path)

if __name__ == "__main__":
    main()