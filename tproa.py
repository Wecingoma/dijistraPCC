import tkinter as tk
from tkinter import ttk, messagebox
from heapq import heappush, heappop
import networkx as nx
import matplotlib.pyplot as plt


class Edge:
    def __init__(self, to, capacity, cost, rev, original=False):
        self.to = to
        self.capacity = capacity
        self.cost = cost
        self.rev = rev
        self.original = original
        self.initial_capacity = capacity if original else 0


class MinCostFlow:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.original_edges = []

    def add_edge(self, u, v, capacity, cost):
        forward = Edge(v, capacity, cost, len(self.graph[v]), original=True)
        backward = Edge(u, 0, -cost, len(self.graph[u]), original=False)

        self.graph[u].append(forward)
        self.graph[v].append(backward)

        self.original_edges.append((u, len(self.graph[u]) - 1))

    def min_cost_flow(self, source, sink, max_flow):
        INF = float("inf")
        total_flow = 0
        total_cost = 0
        potential = [0] * self.n

        while total_flow < max_flow:
            dist = [INF] * self.n
            parent_node = [-1] * self.n
            parent_edge = [-1] * self.n

            dist[source] = 0
            pq = [(0, source)]

            while pq:
                d, u = heappop(pq)
                if d > dist[u]:
                    continue

                for i, e in enumerate(self.graph[u]):
                    if e.capacity <= 0:
                        continue

                    v = e.to
                    reduced_cost = e.cost + potential[u] - potential[v]

                    if dist[v] > dist[u] + reduced_cost:
                        dist[v] = dist[u] + reduced_cost
                        parent_node[v] = u
                        parent_edge[v] = i
                        heappush(pq, (dist[v], v))

            if dist[sink] == INF:
                break

            for i in range(self.n):
                if dist[i] < INF:
                    potential[i] += dist[i]

            add_flow = max_flow - total_flow
            v = sink
            while v != source:
                u = parent_node[v]
                e = self.graph[u][parent_edge[v]]
                add_flow = min(add_flow, e.capacity)
                v = u

            v = sink
            while v != source:
                u = parent_node[v]
                e = self.graph[u][parent_edge[v]]
                rev = self.graph[v][e.rev]

                e.capacity -= add_flow
                rev.capacity += add_flow
                total_cost += add_flow * e.cost

                v = u

            total_flow += add_flow

        return total_flow, total_cost

    def get_edge_flows(self):
        result = []
        for u, idx in self.original_edges:
            e = self.graph[u][idx]
            flow_used = e.initial_capacity - e.capacity
            result.append((u, e.to, e.initial_capacity, e.cost, flow_used))
        return result


class MinCostFlowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flot à coût minimum - Algorithme primal-duaL")
        self.root.geometry("1000x700")

        self.edges = []

        self.build_ui()

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="Problème du flot à coût minimum - Interface graphique",
            font=("Arial", 16, "bold"),
            pady=10
        )
        title.pack()

        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        left_frame = tk.Frame(main_frame)
        left_frame.pack(side="left", fill="y", padx=10)

        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=10)

        # Paramètres généraux
        params_frame = tk.LabelFrame(left_frame, text="Paramètres du réseau", padx=10, pady=10)
        params_frame.pack(fill="x", pady=5)

        tk.Label(params_frame, text="Nombre de sommets :").grid(row=0, column=0, sticky="w")
        self.entry_nodes = tk.Entry(params_frame)
        self.entry_nodes.grid(row=0, column=1, pady=3)

        tk.Label(params_frame, text="Source :").grid(row=1, column=0, sticky="w")
        self.entry_source = tk.Entry(params_frame)
        self.entry_source.grid(row=1, column=1, pady=3)

        tk.Label(params_frame, text="Puits :").grid(row=2, column=0, sticky="w")
        self.entry_sink = tk.Entry(params_frame)
        self.entry_sink.grid(row=2, column=1, pady=3)

        tk.Label(params_frame, text="Flot demandé :").grid(row=3, column=0, sticky="w")
        self.entry_flow = tk.Entry(params_frame)
        self.entry_flow.grid(row=3, column=1, pady=3)

        # Ajout d'arêtes
        edge_frame = tk.LabelFrame(left_frame, text="Ajouter une arête", padx=10, pady=10)
        edge_frame.pack(fill="x", pady=5)

        tk.Label(edge_frame, text="Départ :").grid(row=0, column=0, sticky="w")
        self.entry_u = tk.Entry(edge_frame, width=10)
        self.entry_u.grid(row=0, column=1, pady=3)

        tk.Label(edge_frame, text="Arrivée :").grid(row=1, column=0, sticky="w")
        self.entry_v = tk.Entry(edge_frame, width=10)
        self.entry_v.grid(row=1, column=1, pady=3)

        tk.Label(edge_frame, text="Capacité :").grid(row=2, column=0, sticky="w")
        self.entry_capacity = tk.Entry(edge_frame, width=10)
        self.entry_capacity.grid(row=2, column=1, pady=3)

        tk.Label(edge_frame, text="Coût :").grid(row=3, column=0, sticky="w")
        self.entry_cost = tk.Entry(edge_frame, width=10)
        self.entry_cost.grid(row=3, column=1, pady=3)

        tk.Button(edge_frame, text="Ajouter l'arête", command=self.add_edge).grid(
            row=4, column=0, columnspan=2, pady=8
        )

        tk.Button(edge_frame, text="Supprimer la sélection", command=self.remove_selected_edge).grid(
            row=5, column=0, columnspan=2, pady=4
        )

        tk.Button(edge_frame, text="Vider toutes les arêtes", command=self.clear_edges).grid(
            row=6, column=0, columnspan=2, pady=4
        )

        tk.Button(edge_frame, text="Charger un exemple", command=self.load_example).grid(
            row=7, column=0, columnspan=2, pady=4
        )

        tk.Button(edge_frame, text="Exécuter l'algorithme", command=self.run_algorithm).grid(
            row=8, column=0, columnspan=2, pady=10
        )

        tk.Button(edge_frame, text="Tracer le graphe courant", command=self.draw_current_graph).grid(
            row=9, column=0, columnspan=2, pady=4
        )

        # Liste des arêtes
        list_frame = tk.LabelFrame(right_frame, text="Arêtes du graphe", padx=10, pady=10)
        list_frame.pack(fill="both", expand=False, pady=5)

        columns = ("u", "v", "capacity", "cost")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        self.tree.heading("u", text="Départ")
        self.tree.heading("v", text="Arrivée")
        self.tree.heading("capacity", text="Capacité")
        self.tree.heading("cost", text="Coût")

        self.tree.column("u", width=80, anchor="center")
        self.tree.column("v", width=80, anchor="center")
        self.tree.column("capacity", width=100, anchor="center")
        self.tree.column("cost", width=100, anchor="center")

        self.tree.pack(fill="x")

        # Résultats
        result_frame = tk.LabelFrame(right_frame, text="Résultats", padx=10, pady=10)
        result_frame.pack(fill="both", expand=True, pady=5)

        self.result_text = tk.Text(result_frame, height=20, wrap="word")
        self.result_text.pack(fill="both", expand=True)

    def add_edge(self):
        try:
            u = int(self.entry_u.get())
            v = int(self.entry_v.get())
            capacity = int(self.entry_capacity.get())
            cost = int(self.entry_cost.get())

            if capacity < 0:
                raise ValueError("La capacité doit être positive.")
            if u < 0 or v < 0:
                raise ValueError("Les sommets doivent être positifs.")

            self.edges.append((u, v, capacity, cost))
            self.tree.insert("", "end", values=(u, v, capacity, cost))

            self.entry_u.delete(0, tk.END)
            self.entry_v.delete(0, tk.END)
            self.entry_capacity.delete(0, tk.END)
            self.entry_cost.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("Erreur", f"Entrées invalides : {e}")

    def remove_selected_edge(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Aucune arête sélectionnée.")
            return

        for item in selected:
            values = self.tree.item(item, "values")
            edge = tuple(map(int, values))
            if edge in self.edges:
                self.edges.remove(edge)
            self.tree.delete(item)

    def clear_edges(self):
        self.edges.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.result_text.delete("1.0", tk.END)

    def load_example(self):
        self.clear_edges()

        self.entry_nodes.delete(0, tk.END)
        self.entry_source.delete(0, tk.END)
        self.entry_sink.delete(0, tk.END)
        self.entry_flow.delete(0, tk.END)

        self.entry_nodes.insert(0, "4")
        self.entry_source.insert(0, "0")
        self.entry_sink.insert(0, "3")
        self.entry_flow.insert(0, "4")

        example_edges = [
            (0, 1, 3, 1),
            (0, 2, 2, 2),
            (1, 2, 2, 1),
            (1, 3, 2, 3),
            (2, 3, 4, 1),
        ]

        for edge in example_edges:
            self.edges.append(edge)
            self.tree.insert("", "end", values=edge)

    def validate_graph_inputs(self):
        try:
            n = int(self.entry_nodes.get())
            source = int(self.entry_source.get())
            sink = int(self.entry_sink.get())
            flow = int(self.entry_flow.get())

            if n <= 0:
                raise ValueError("Le nombre de sommets doit être > 0.")
            if source < 0 or source >= n:
                raise ValueError("La source est invalide.")
            if sink < 0 or sink >= n:
                raise ValueError("Le puits est invalide.")
            if flow < 0:
                raise ValueError("Le flot demandé doit être positif.")
            if source == sink:
                raise ValueError("La source et le puits doivent être différents.")

            for (u, v, capacity, cost) in self.edges:
                if u >= n or v >= n:
                    raise ValueError(f"L'arête ({u}->{v}) dépasse le nombre de sommets.")
                if capacity < 0:
                    raise ValueError(f"Capacité invalide sur l'arête ({u}->{v}).")

            return n, source, sink, flow

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
            return None

    def run_algorithm(self):
        validated = self.validate_graph_inputs()
        if validated is None:
            return

        n, source, sink, max_flow = validated

        if not self.edges:
            messagebox.showwarning("Attention", "Ajoute au moins une arête.")
            return

        mcf = MinCostFlow(n)
        for u, v, capacity, cost in self.edges:
            mcf.add_edge(u, v, capacity, cost)

        total_flow, total_cost = mcf.min_cost_flow(source, sink, max_flow)
        edge_flows = mcf.get_edge_flows()

        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, "=== RÉSULTATS ===\n")
        self.result_text.insert(tk.END, f"Flot demandé : {max_flow}\n")
        self.result_text.insert(tk.END, f"Flot envoyé  : {total_flow}\n")
        self.result_text.insert(tk.END, f"Coût total   : {total_cost}\n\n")

        if total_flow < max_flow:
            self.result_text.insert(
                tk.END,
                "Attention : le réseau ne permet pas d'envoyer tout le flot demandé.\n\n"
            )

        self.result_text.insert(tk.END, "=== DÉTAIL DES ARÊTES ===\n")
        for u, v, cap, cost, flow_used in edge_flows:
            self.result_text.insert(
                tk.END,
                f"{u} -> {v} | capacité={cap}, coût={cost}, flot utilisé={flow_used}\n"
            )

        self.draw_graph(edge_flows, title="Graphe après exécution")

    def draw_current_graph(self):
        validated = self.validate_graph_inputs()
        if validated is None:
            return

        n, _, _, _ = validated

        G = nx.DiGraph()
        G.add_nodes_from(range(n))

        for u, v, capacity, cost in self.edges:
            G.add_edge(u, v, capacity=capacity, cost=cost, flow=0)

        self._plot_graph(G, "Graphe courant")

    def draw_graph(self, edge_data, title="Graphe"):
        validated = self.validate_graph_inputs()
        if validated is None:
            return

        n, _, _, _ = validated

        G = nx.DiGraph()
        G.add_nodes_from(range(n))

        for u, v, cap, cost, flow in edge_data:
            G.add_edge(u, v, capacity=cap, cost=cost, flow=flow)

        self._plot_graph(G, title)

    def _plot_graph(self, G, title):
        plt.figure(figsize=(10, 6))

        try:
            pos = nx.spring_layout(G, seed=42)
        except Exception:
            pos = nx.circular_layout(G)

        edge_colors = []
        widths = []

        for _, _, data in G.edges(data=True):
            flow = data.get("flow", 0)
            if flow > 0:
                edge_colors.append("red")
                widths.append(2.5)
            else:
                edge_colors.append("gray")
                widths.append(1.5)

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_size=2200,
            node_color="lightblue",
            font_size=11,
            font_weight="bold",
            arrows=True,
            edge_color=edge_colors,
            width=widths
        )

        edge_labels = {}
        for u, v, data in G.edges(data=True):
            cap = data.get("capacity", 0)
            cost = data.get("cost", 0)
            flow = data.get("flow", 0)
            edge_labels[(u, v)] = f"cap={cap}\ncoût={cost}\nflot={flow}"

        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

        plt.title(title)
        plt.axis("off")
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = MinCostFlowApp(root)
    root.mainloop()