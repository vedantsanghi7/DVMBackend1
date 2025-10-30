import matplotlib.pyplot as plt
import networkx as nx

class MetroVisualizer:
    def __init__(self, metro_system):
        self.metro = metro_system
        self.graph = nx.Graph()
        self.colors = {'R': 'red', 'B': 'blue', 'O': 'orange', 'Y': 'yellow', 'G': 'green'}
        self.line_names = {'R': 'Red', 'B': 'Blue', 'O': 'Orange', 'Y': 'Yellow', 'G': 'Green'}
    
    def create_graph(self):
        for station_id, station in self.metro.stations.items():
            self.graph.add_node(station_id, name=station.name, lines=list(station.lines))
        
        for station_id, neighbors in self.metro.graph.items():
            for neighbor, line in neighbors:
                if station_id < neighbor:
                    self.graph.add_edge(station_id, neighbor, line=line, color=self.colors.get(line, 'black'))
    
    def visualize(self):
        self.create_graph()
        
        plt.figure(figsize=(16, 12))
        pos = nx.spring_layout(self.graph, k=2, iterations=100)
        
        drawn_edges = set()
        for line_id, line in self.metro.lines.items():
            line_edges = []
            for u, v, data in self.graph.edges(data=True):
                edge_key = tuple(sorted([u, v]))
                if data['line'] == line_id and edge_key not in drawn_edges:
                    line_edges.append((u, v))
                    drawn_edges.add(edge_key)
            
            if line_edges:
                nx.draw_networkx_edges(self.graph, pos, edgelist=line_edges, 
                                     edge_color=self.colors.get(line_id, 'black'),
                                     width=4, alpha=0.7, label=self.line_names.get(line_id, line_id))
        
        node_colors = []
        for node in self.graph.nodes():
            station = self.metro.stations[node]
            if len(station.lines) > 1:
                node_colors.append('purple')
            else:
                node_colors.append('lightblue')
        
        nx.draw_networkx_nodes(self.graph, pos, node_color=node_colors, 
                             node_size=800, alpha=0.9, edgecolors='black', linewidths=1)
        
        labels = {}
        for node in self.graph.nodes():
            station = self.metro.stations[node]
            if len(station.lines) > 1:
                labels[node] = f"{node}\n{station.name}\n(Transfer)"
            else:
                labels[node] = f"{node}\n{station.name}"
        
        nx.draw_networkx_labels(self.graph, pos, labels=labels, font_size=6, font_weight='bold')
        
        plt.title("Metro System Map\n(Purple nodes are transfer stations)", size=16, pad=20)
        plt.legend(loc='upper left', bbox_to_anchor=(0, 1), frameon=True)
        
        plt.figtext(0.02, 0.02, 
                   f"Total Stations: {len(self.metro.stations)}\n"
                   f"Total Lines: {len(self.metro.lines)}\n"
                   f"Transfer Stations: {sum(1 for s in self.metro.stations.values() if len(s.lines) > 1)}",
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
        
        plt.axis('off')
        plt.tight_layout()
        plt.show()