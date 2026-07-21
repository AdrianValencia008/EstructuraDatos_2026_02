# -*- coding: utf-8 -*-
"""Generador de figuras — CH14 Algoritmos en Grafos (usa networkx).

    python generar_figuras/generar_figuras_ch14.py
Vive en generar_figuras/ (en .gitignore, no se versiona).
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
from pathlib import Path

IMG = Path('notebooks/assets')
IMG.mkdir(parents=True, exist_ok=True)

TITLE = '#1A237E'
BASE_NODE = '#BBDEFB'
BASE_EDGE = '#90A4AE'
HL = '#E53935'          # resaltado (highlight)
HL_NODE = '#FFE082'

# Grafo ponderado de ejemplo (el mismo que usa el notebook de teoria)
WEIGHTED = [('A', 'B', 4), ('A', 'C', 2), ('B', 'C', 1), ('B', 'D', 5),
            ('C', 'D', 8), ('C', 'E', 10), ('D', 'E', 2), ('D', 'F', 6), ('E', 'F', 3)]
POS = {'A': (0, 1), 'B': (1, 2), 'C': (1, 0), 'D': (2.4, 1), 'E': (3.8, 0), 'F': (5, 1)}


def base_graph():
    G = nx.Graph()
    for u, v, w in WEIGHTED:
        G.add_edge(u, v, weight=w)
    return G


def draw(ax, G, title, hl_edges=None, node_labels=None, directed=False, hl_color=HL):
    hl_edges = set(tuple(sorted(e)) for e in (hl_edges or []))
    ax.set_title(title, fontsize=13, fontweight='bold', color=TITLE, pad=8)
    ax.axis('off')
    ecolors, ewidths = [], []
    for u, v in G.edges():
        if tuple(sorted((u, v))) in hl_edges:
            ecolors.append(hl_color); ewidths.append(3.4)
        else:
            ecolors.append(BASE_EDGE); ewidths.append(1.6)
    ncolors = [HL_NODE if (node_labels and n in node_labels) else BASE_NODE for n in G.nodes()]
    edge_kwargs = dict(edge_color=ecolors, width=ewidths, node_size=1100)
    if directed:
        edge_kwargs.update(arrows=True, arrowsize=18, connectionstyle='arc3')
    nx.draw_networkx_edges(G, POS, ax=ax, **edge_kwargs)
    nx.draw_networkx_nodes(G, POS, ax=ax, node_color=ncolors, edgecolors='#0D47A1',
                           linewidths=2, node_size=1100)
    lbls = {n: (f'{n}\n{node_labels[n]}' if (node_labels and n in node_labels) else n)
            for n in G.nodes()}
    nx.draw_networkx_labels(G, POS, lbls, ax=ax, font_size=11, font_weight='bold', font_color='#0D47A1')
    if nx.get_edge_attributes(G, 'weight'):
        elabels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, POS, elabels, ax=ax, font_size=10,
                                     font_color='#37474F',
                                     bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.85))


# ============ Figura 1: dirigido vs no dirigido ============
def fig_intro():
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.6))

    Gu = nx.Graph()
    Gu.add_edges_from([('A', 'B'), ('A', 'C'), ('B', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'E')])
    posu = {'A': (0, 1), 'B': (1, 1.8), 'C': (1, 0.2), 'D': (2.2, 1.5), 'E': (2.2, 0.5)}

    Gd = nx.DiGraph()
    Gd.add_edges_from([('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'), ('D', 'E')])

    for ax, G, pos, title, directed in [
        (axes[0], Gu, posu, 'Grafo no dirigido', False),
        (axes[1], Gd, posu, 'Grafo dirigido (digrafo)', True)]:
        ax.set_title(title, fontsize=13, fontweight='bold', color=TITLE, pad=8)
        ax.axis('off')
        ekw = dict(edge_color=BASE_EDGE, width=2.0, node_size=1100)
        if directed:
            ekw.update(arrows=True, arrowsize=20, connectionstyle='arc3,rad=0.02')
        nx.draw_networkx_edges(G, pos, ax=ax, **ekw)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=BASE_NODE,
                               edgecolors='#0D47A1', linewidths=2, node_size=1100)
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=12, font_weight='bold', font_color='#0D47A1')

    plt.tight_layout()
    plt.savefig(IMG / 'ch14_grafo_intro.png', dpi=130, bbox_inches='tight')
    plt.close(fig)
    print('Guardado: ch14_grafo_intro.png')


# ============ Figura 2: DFS vs BFS ============
def fig_dfs_bfs():
    fig, axes = plt.subplots(1, 2, figsize=(14, 4.8))
    G = base_graph()
    # quitar pesos para esta figura (recorridos no los usan)
    Gp = nx.Graph(); Gp.add_edges_from([(u, v) for u, v, w in WEIGHTED])

    dfs_edges = list(nx.dfs_edges(Gp, source='A'))
    bfs_edges = list(nx.bfs_edges(Gp, source='A'))

    draw(axes[0], Gp, 'DFS desde A (aristas de árbol)', hl_edges=dfs_edges,
         node_labels={'A': '★'})
    draw(axes[1], Gp, 'BFS desde A (aristas de árbol)', hl_edges=bfs_edges,
         node_labels={'A': '★'}, hl_color='#2E7D32')

    plt.tight_layout()
    plt.savefig(IMG / 'ch14_dfs_bfs.png', dpi=130, bbox_inches='tight')
    plt.close(fig)
    print('Guardado: ch14_dfs_bfs.png')


# ============ Figura 3: Dijkstra ============
def fig_dijkstra():
    fig, ax = plt.subplots(figsize=(8.5, 5.0))
    G = base_graph()
    dist = nx.single_source_dijkstra_path_length(G, 'A')
    paths = nx.single_source_dijkstra_path(G, 'A')
    spt = set()
    for v, p in paths.items():
        for a, b in zip(p, p[1:]):
            spt.add(tuple(sorted((a, b))))
    labels = {n: f'd={dist[n]}' for n in G.nodes()}
    draw(ax, G, 'Dijkstra desde A — árbol de caminos más cortos (d = distancia)',
         hl_edges=spt, node_labels=labels)
    plt.tight_layout()
    plt.savefig(IMG / 'ch14_dijkstra.png', dpi=130, bbox_inches='tight')
    plt.close(fig)
    print('Guardado: ch14_dijkstra.png')


# ============ Figura 4: MST ============
def fig_mst():
    fig, ax = plt.subplots(figsize=(8.5, 5.0))
    G = base_graph()
    T = nx.minimum_spanning_tree(G)
    mst_edges = list(T.edges())
    total = sum(d['weight'] for _, _, d in T.edges(data=True))
    draw(ax, G, f'Árbol de Expansión Mínima (peso total = {total})',
         hl_edges=mst_edges, hl_color='#6A1B9A')
    plt.tight_layout()
    plt.savefig(IMG / 'ch14_mst.png', dpi=130, bbox_inches='tight')
    plt.close(fig)
    print('Guardado: ch14_mst.png')


# ============ Figura 5: orden topologico ============
def fig_topological():
    fig, ax = plt.subplots(figsize=(11, 3.4))
    G = nx.DiGraph()
    G.add_edges_from([('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'), ('C', 'E'), ('D', 'F'), ('E', 'F')])
    order = list(nx.topological_sort(G))
    pos = {n: (i * 1.6, 0) for i, n in enumerate(order)}
    ax.set_title('Orden topológico de un DAG:  ' + '  →  '.join(order),
                 fontsize=13, fontweight='bold', color=TITLE, pad=10)
    ax.axis('off')
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=BASE_EDGE, width=2.0, arrows=True,
                           arrowsize=20, node_size=1100, connectionstyle='arc3,rad=-0.25')
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=BASE_NODE, edgecolors='#0D47A1',
                           linewidths=2, node_size=1100)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=12, font_weight='bold', font_color='#0D47A1')
    for i, n in enumerate(order):
        ax.text(i * 1.6, -0.55, f'#{i + 1}', ha='center', fontsize=10, color='#546E7A', fontweight='bold')
    ax.set_ylim(-0.9, 0.9)
    plt.tight_layout()
    plt.savefig(IMG / 'ch14_topological.png', dpi=130, bbox_inches='tight')
    plt.close(fig)
    print('Guardado: ch14_topological.png')


if __name__ == '__main__':
    fig_intro()
    fig_dfs_bfs()
    fig_dijkstra()
    fig_mst()
    fig_topological()
    print('CH14: figuras generadas en', IMG)
