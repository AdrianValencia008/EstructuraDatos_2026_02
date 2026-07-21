# -*- coding: utf-8 -*-
"""Generador de figuras — CH11 Árboles de Búsqueda (usa matplotlib + las clases reales de goodrich.ch11).

    python generar_figuras/generar_figuras_ch11.py
Vive en generar_figuras/ (en .gitignore, no se versiona).
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from goodrich.ch11.binary_search_tree import TreeMap
from goodrich.ch11.avl_tree import AVLTreeMap
from goodrich.ch11.red_black_tree import RedBlackTreeMap
from goodrich.ch11.splay_tree import SplayTreeMap

IMG = Path('notebooks/assets')
IMG.mkdir(parents=True, exist_ok=True)

TITLE = '#1A237E'
BASE_NODE = '#BBDEFB'
BASE_EDGE = '#90A4AE'
HL_NODE = '#FFE082'
RED_NODE = '#EF9A9A'
RED_EDGE_COLOR = '#B71C1C'
BLACK_NODE = '#455A64'


# --------------------------------------------------------------------------
# Utilidades para calcular posiciones (x,y) de un LinkedBinaryTree de goodrich
# x = orden in-order (garantiza que no se crucen ramas), y = -profundidad
# --------------------------------------------------------------------------
def layout(tree):
    """Retorna {id(nodo_interno): (posicion, x, y)}. Usamos p._node como clave
    estable porque Position no es hasheable (solo define __eq__)."""
    pos = {}
    counter = [0]

    def walk(p, depth):
        if p is None:
            return
        left = tree.left(p)
        right = tree.right(p)
        walk(left, depth + 1)
        x = counter[0]
        counter[0] += 1
        pos[p._node] = (p, x, -depth)
        walk(right, depth + 1)

    if len(tree) > 0:
        walk(tree.root(), 0)
    return pos


def draw_tree(ax, tree, title, node_color_fn=None, highlight=None, label_fn=None):
    pos = layout(tree)
    ax.set_title(title, fontsize=12.5, fontweight='bold', color=TITLE, pad=8)
    ax.axis('off')
    highlight_nodes = {p._node for p in (highlight or set())}

    # aristas
    for node_key, (p, x, y) in pos.items():
        parent = tree.parent(p)
        if parent is not None and parent._node in pos:
            _, x0, y0 = pos[parent._node]
            ax.plot([x0, x], [y0, y], color=BASE_EDGE, linewidth=1.8, zorder=1)

    # nodos
    for node_key, (p, x, y) in pos.items():
        color = node_color_fn(p) if node_color_fn else BASE_NODE
        is_hl = node_key in highlight_nodes
        edge = '#D50000' if is_hl else '#0D47A1'
        lw = 3 if is_hl else 1.6
        ax.scatter([x], [y], s=950, color=color, edgecolors=edge, linewidths=lw, zorder=2)
        label = label_fn(p) if label_fn else str(p.key())
        text_color = 'white' if color == BLACK_NODE else '#1A237E'
        ax.text(x, y, label, ha='center', va='center', fontsize=10.5,
                fontweight='bold', color=text_color, zorder=3)

    if pos:
        xs = [x for _, x, y in pos.values()]
        ys = [y for _, x, y in pos.values()]
        ax.set_xlim(min(xs) - 0.8, max(xs) + 0.8)
        ax.set_ylim(min(ys) - 0.8, max(ys) + 0.8)


# ============ Figura 1: BST degenerado vs AVL balanceado ============
def fig_bst_vs_avl():
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))

    bst = TreeMap()
    for k in range(1, 11):
        bst[k] = k
    draw_tree(axes[0], bst, f'BST — inserción ordenada 1..10\naltura = {bst.height(bst.root())} (degenerado)')

    avl = AVLTreeMap()
    for k in range(1, 11):
        avl[k] = k
    draw_tree(axes[1], avl, f'AVL — misma inserción 1..10\naltura = {avl.height(avl.root())} (balanceado)')

    plt.tight_layout()
    plt.savefig(IMG / 'ch11_bst_vs_avl.png', dpi=130, bbox_inches='tight')
    plt.close(fig)
    print('Guardado: ch11_bst_vs_avl.png')


# ============ Figura 2: reestructuración trinodal (rotación simple y doble) ============
def fig_trinode_restructure():
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.2))

    # Antes: desbalanceado a la izquierda-izquierda (rotación simple)
    before1 = TreeMap()
    for k in [30, 20, 10]:      # inserción ordenada descendente -> cadena izquierda
        before1[k] = k
    draw_tree(axes[0], before1, 'Antes — desbalance\n(caso zig-zig / LL)',
              highlight=[before1.root()])

    # Antes: desbalance zig-zag (izquierda-derecha)
    before2 = TreeMap()
    for k in [30, 10, 20]:
        before2[k] = k
    draw_tree(axes[1], before2, 'Antes — desbalance\n(caso zig-zag / LR)',
              highlight=[before2.root()])

    # Después de reestructurar (AVL logra el mismo resultado balanceado en ambos casos)
    after = AVLTreeMap()
    for k in [30, 20, 10]:
        after[k] = k
    draw_tree(axes[2], after, 'Después de la reestructuración\ntrinodal (subárbol balanceado)',
              highlight=[after.root()])

    plt.tight_layout()
    plt.savefig(IMG / 'ch11_trinode_restructure.png', dpi=130, bbox_inches='tight')
    plt.close(fig)
    print('Guardado: ch11_trinode_restructure.png')


# ============ Figura 3: árbol rojinegro con colores ============
def fig_red_black():
    fig, ax = plt.subplots(figsize=(9, 5.2))
    rbt = RedBlackTreeMap()
    for k in [44, 17, 88, 8, 32, 65, 97, 28, 54, 82]:
        rbt[k] = k

    def color_fn(p):
        return RED_NODE if rbt._is_red(p) else BLACK_NODE

    draw_tree(ax, rbt, 'Árbol rojinegro — cada nodo hereda el color de su\nresolución de inserción (raíz siempre negra)',
              node_color_fn=color_fn)

    # leyenda manual
    ax.scatter([], [], s=200, color=RED_NODE, edgecolors='#0D47A1', label='rojo')
    ax.scatter([], [], s=200, color=BLACK_NODE, edgecolors='#0D47A1', label='negro')
    ax.legend(loc='upper right', frameon=False, fontsize=10)

    plt.tight_layout()
    plt.savefig(IMG / 'ch11_red_black.png', dpi=130, bbox_inches='tight')
    plt.close(fig)
    print('Guardado: ch11_red_black.png')


# ============ Figura 4: splay tree antes / después de acceder a una clave ============
def fig_splay():
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))

    sp = SplayTreeMap()
    for k in [44, 17, 88, 8, 32, 65, 97, 28, 54, 82]:
        sp[k] = k
    draw_tree(axes[0], sp, 'Splay tree — tras insertar todas las claves\n(la raíz es la última clave insertada)',
              highlight=[sp.root()])

    accedida = sp.find_position(8)     # accede a la clave 8 y la splaya a la raiz
    draw_tree(axes[1], sp, 'Splay tree — tras acceder a la clave 8\n(8 sube a la raíz por splaying)',
              highlight=[sp.root()])

    plt.tight_layout()
    plt.savefig(IMG / 'ch11_splay.png', dpi=130, bbox_inches='tight')
    plt.close(fig)
    print('Guardado: ch11_splay.png')


if __name__ == '__main__':
    fig_bst_vs_avl()
    fig_trinode_restructure()
    fig_red_black()
    fig_splay()
    print('CH11: figuras generadas en', IMG)
