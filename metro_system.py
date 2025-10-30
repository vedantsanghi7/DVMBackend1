import csv
import networkx as nx
from station import Station
from line import Line
from ticket import Ticket

class MetroSystem:
    def __init__(self):
        self.graph = nx.Graph()
        self.stations = {}
        self.lines = {}
        self.tickets = []

    def load_data(self):
        with open('stations.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                station = Station(row['id'], row['name'])
                self.stations[row['id']] = station
                self.graph.add_node(row['id'], name=row['name'])

        with open('lines.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.lines[row['id']] = Line(row['id'], row['name'])

        with open('edges.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.graph.add_edge(row['from'], row['to'], line=row['line'])

    def list_stations(self):
        print("\nList of Metro Stations:\n")
        for st in self.stations.values():
            print(f"{st.id} - {st.name}")
        print()

    def shortest_path(self, src, dest):
        import networkx as nx
        try:
            return nx.shortest_path(self.graph, src, dest)
        except nx.NetworkXNoPath:
            return None

    def calculate_price(self, path):
        return (len(path) - 1) * 5 if path else 0  # ₹5 per hop

    def purchase_ticket(self, src, dest):
        path = self.shortest_path(src, dest)
        if not path:
            print("No path found.")
            return

        price = self.calculate_price(path)
        ticket = Ticket(src, dest, price, path)
        self.tickets.append(ticket)

        print(f"\nTicket purchased successfully! ID: {ticket.id}")
        print(f"From: {self.stations[src].name}  →  To: {self.stations[dest].name}")
        print(f"Stations crossed: {len(path)-1}")
        print(f"Total Price: ₹{price}")
        print("\nRoute Instructions:")
        for i in range(len(path) - 1):
            edge_data = self.graph.get_edge_data(path[i], path[i+1])
            line_name = self.lines[edge_data['line']].name
            print(f"  {self.stations[path[i]].name} → {self.stations[path[i+1]].name} ({line_name} Line)")
        print()

    def view_tickets(self):
        if not self.tickets:
            print("No tickets purchased yet.")
            return
        print("\nPurchased Tickets:\n")
        for t in self.tickets:
            print(f"ID: {t.id} | From: {self.stations[t.src].name} → {self.stations[t.dest].name} | Price: ₹{t.price}")

    def visualize(self):
        import matplotlib.pyplot as plt
        import matplotlib.lines as mlines

        line_colors = {
            "R": "red",
            "B": "blue",
            "O": "orange",
            "Y": "gold",
            "G": "green"
        }

        pos = nx.spring_layout(self.graph, seed=42)
        plt.figure(figsize=(10, 8))

        for line_id, color in line_colors.items():
            edges = [(u, v) for u, v, d in self.graph.edges(data=True) if d["line"] == line_id]
            nx.draw_networkx_edges(
                self.graph, pos,
                edgelist=edges,
                width=2.5,
                edge_color=color,
                alpha=0.8
            )

        nx.draw_networkx_nodes(self.graph, pos, node_size=550, node_color='lightgray')
        nx.draw_networkx_labels(self.graph, pos,
                                labels={n: self.stations[n].name for n in self.graph.nodes()},
                                font_size=7)

        legend_handles = [
            mlines.Line2D([], [], color=color, marker='_', markersize=15, label=self.lines[line_id].name)
            for line_id, color in line_colors.items()
        ]
        plt.legend(handles=legend_handles, title="Metro Lines", loc="upper left")

        plt.title("Washington Metro Map (Simplified)", fontsize=12, fontweight='bold')
        plt.axis("off")
        plt.tight_layout()
        plt.show()

