# -*- coding: utf-8 -*-
"""Generador de figuras — CH09 Colas de Prioridad.

Ejecuta este script para regenerar las imagenes en notebooks/assets/.
    python generar_figuras/generar_figuras_ch09.py
Este archivo vive en generar_figuras/ (en .gitignore, no se versiona).
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

IMG = Path('notebooks/assets')
IMG.mkdir(parents=True, exist_ok=True)

BLUE_FC, BLUE_EC = '#90CAF9', '#0D47A1'
RED_FC, RED_EC = '#EF9A9A', '#B71C1C'
GREEN_FC, GREEN_EC = '#A5D6A7', '#1B5E20'
TITLE = '#1A237E'


def node(ax, x, y, val, r=0.40, fc=BLUE_FC, ec=BLUE_EC, fs=14):
    ax.add_patch(patches.Circle((x, y), r, fc=fc, ec=ec, lw=2, zorder=3))
    ax.text(x, y, str(val), ha='center', va='center',
            fontsize=fs, fontweight='bold', color=ec, zorder=4)


def link(ax, x1, y1, x2, y2, color=BLUE_EC, lw=1.8):
    ax.plot([x1, x2], [y1, y2], color=color, lw=lw, zorder=1)


# ---- posiciones del heap de ejemplo [4,5,6,15,9] ----
POS = {0: (3.0, 3.0), 1: (1.6, 1.9), 2: (4.4, 1.9), 3: (0.8, 0.8), 4: (2.4, 0.8)}
EDGES = [(0, 1), (0, 2), (1, 3), (1, 4)]
VALS = [4, 5, 6, 15, 9]


# ============ Figura 1: heap como arbol + arreglo ============
def fig_tree_array():
    fig, ax = plt.subplots(figsize=(12, 5.2))
    ax.axis('off'); ax.set_xlim(-0.5, 11.5); ax.set_ylim(-1.6, 3.8)
    ax.set_title('Montículo: árbol binario completo  ↔  arreglo (level-numbering)',
                 fontsize=14, fontweight='bold', color=TITLE, pad=10)

    for a, b in EDGES:
        link(ax, *POS[a], *POS[b])
    for i, (x, y) in POS.items():
        node(ax, x, y, VALS[i])
        ax.text(x + 0.46, y + 0.30, f'[{i}]', fontsize=9, color='#546E7A', fontweight='bold')

    # arreglo a la derecha
    ax0 = 6.2; ay = 1.6; cw = 0.95
    for i, v in enumerate(VALS):
        x = ax0 + i * cw
        ax.add_patch(patches.Rectangle((x, ay), cw, 0.85, fc=BLUE_FC, ec=BLUE_EC, lw=2, zorder=2))
        ax.text(x + cw / 2, ay + 0.42, str(v), ha='center', va='center',
                fontsize=13, fontweight='bold', color=BLUE_EC, zorder=3)
        ax.text(x + cw / 2, ay - 0.28, f'[{i}]', ha='center', fontsize=9, color='#546E7A', fontweight='bold')
    ax.text(ax0 + 2.5 * cw, ay + 1.25, 'self._data', ha='center', fontsize=11,
            style='italic', color='#37474F')

    # formulas de indices
    ax.text(3.0, -1.25,
            r'padre(j) = (j−1)//2      izq(j) = 2j+1      der(j) = 2j+2',
            ha='center', fontsize=12, color='#37474F',
            bbox=dict(boxstyle='round,pad=0.4', fc='#FFF8E1', ec='#FBC02D'))

    plt.tight_layout()
    plt.savefig(IMG / 'ch09_heap_tree_array.png', dpi=130, bbox_inches='tight')
    plt.close(fig)
    print('Guardado: ch09_heap_tree_array.png')


# ============ Figura 2: up-heap y down-heap ============
def fig_up_down():
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.0))

    # --- Up-heap (tras add) ---
    ax = axes[0]
    ax.axis('off'); ax.set_xlim(-0.5, 5.5); ax.set_ylim(-0.8, 3.8)
    ax.set_title('Up-heap (después de add)', fontsize=13, fontweight='bold', color=GREEN_EC, pad=8)
    for a, b in EDGES:
        link(ax, *POS[a], *POS[b])
    # nuevo nodo insertado como hijo izq de [2]=6 -> indice 5
    new_pos = (3.7, 0.8)
    link(ax, *POS[2], *new_pos, color=GREEN_EC)
    for i, (x, y) in POS.items():
        node(ax, x, y, VALS[i])
    node(ax, *new_pos, 2, fc=GREEN_FC, ec=GREEN_EC)
    ax.text(new_pos[0] + 0.46, new_pos[1] + 0.30, '[5]', fontsize=9, color='#546E7A', fontweight='bold')
    # flecha de subida nuevo->[2]->[0]
    ax.annotate('', xy=(POS[2][0] - 0.1, POS[2][1] - 0.35),
                xytext=(new_pos[0] - 0.1, new_pos[1] + 0.35),
                arrowprops=dict(arrowstyle='->', color=GREEN_EC, lw=2.2, connectionstyle='arc3,rad=0.2'))
    ax.annotate('', xy=(POS[0][0] + 0.1, POS[0][1] - 0.35),
                xytext=(POS[2][0] + 0.0, POS[2][1] + 0.35),
                arrowprops=dict(arrowstyle='->', color=GREEN_EC, lw=2.2, connectionstyle='arc3,rad=-0.2'))
    ax.text(2.5, -0.55, 'el nuevo sube mientras sea\nmenor que su padre  → O(log n)',
            ha='center', fontsize=10, color=GREEN_EC)

    # --- Down-heap (tras remove_min) ---
    ax = axes[1]
    ax.axis('off'); ax.set_xlim(-0.5, 5.5); ax.set_ylim(-0.8, 3.8)
    ax.set_title('Down-heap (después de remove_min)', fontsize=13, fontweight='bold', color=RED_EC, pad=8)
    down_vals = [15, 5, 6, 9]  # 15 puesto en la raiz, baja
    dpos = {0: POS[0], 1: POS[1], 2: POS[2], 3: POS[3], 4: POS[4]}
    for a, b in EDGES:
        link(ax, *dpos[a], *dpos[b])
    node(ax, *dpos[0], 15, fc=RED_FC, ec=RED_EC)
    node(ax, *dpos[1], 5)
    node(ax, *dpos[2], 6)
    node(ax, *dpos[3], 9)
    node(ax, *dpos[4], 15, fc='#E0E0E0', ec='#9E9E9E')
    ax.text(dpos[4][0], dpos[4][1] - 0.7, '(hueco)', ha='center', fontsize=8, color='#9E9E9E')
    # flecha de bajada [0]->[1]->[3]
    ax.annotate('', xy=(dpos[1][0] + 0.1, dpos[1][1] + 0.35),
                xytext=(dpos[0][0] - 0.1, dpos[0][1] - 0.35),
                arrowprops=dict(arrowstyle='->', color=RED_EC, lw=2.2, connectionstyle='arc3,rad=0.2'))
    ax.annotate('', xy=(dpos[3][0] + 0.1, dpos[3][1] + 0.35),
                xytext=(dpos[1][0] - 0.05, dpos[1][1] - 0.35),
                arrowprops=dict(arrowstyle='->', color=RED_EC, lw=2.2, connectionstyle='arc3,rad=0.2'))
    ax.text(2.5, -0.55, 'la raíz baja intercambiándose con el\nhijo de menor clave  → O(log n)',
            ha='center', fontsize=10, color=RED_EC)

    plt.tight_layout()
    plt.savefig(IMG / 'ch09_upheap_downheap.png', dpi=130, bbox_inches='tight')
    plt.close(fig)
    print('Guardado: ch09_upheap_downheap.png')


# ============ Figura 3: heap adaptable con locators ============
def fig_adaptable():
    fig, ax = plt.subplots(figsize=(12, 4.6))
    ax.axis('off'); ax.set_xlim(-0.5, 11.5); ax.set_ylim(-1.2, 3.4)
    ax.set_title('Cola de prioridad adaptable: cada Locator guarda el índice de su entrada',
                 fontsize=13.5, fontweight='bold', color=TITLE, pad=10)

    items = [('2', 'a'), ('5', 'b'), ('4', 'c'), ('9', 'd')]
    locs = ['loc_a', 'loc_b', 'loc_c', 'loc_d']
    x0, ay, cw = 0.8, 0.5, 2.3

    for i, (k, v) in enumerate(items):
        x = x0 + i * cw
        ax.add_patch(patches.Rectangle((x, ay), cw - 0.25, 0.9, fc=BLUE_FC, ec=BLUE_EC, lw=2, zorder=2))
        ax.text(x + (cw - 0.25) / 2, ay + 0.45, f'_Item({k},{v!r})', ha='center', va='center',
                fontsize=11, fontweight='bold', color=BLUE_EC, zorder=3)
        ax.text(x + (cw - 0.25) / 2, ay - 0.30, f'índice {i}', ha='center', fontsize=9,
                color='#546E7A', fontweight='bold')
        # locator arriba con flecha hacia la celda
        ly = 2.6
        ax.add_patch(patches.FancyBboxPatch((x + 0.35, ly), cw - 0.95, 0.55,
                     boxstyle='round,pad=0.05', fc='#FFE0B2', ec='#E65100', lw=1.8, zorder=2))
        ax.text(x + (cw - 0.25) / 2, ly + 0.27, locs[i], ha='center', va='center',
                fontsize=10, fontweight='bold', color='#E65100', zorder=3)
        ax.annotate('', xy=(x + (cw - 0.25) / 2, ay + 0.92),
                    xytext=(x + (cw - 0.25) / 2, ly - 0.02),
                    arrowprops=dict(arrowstyle='->', color='#E65100', lw=1.8))

    ax.text(5.0, -0.95,
            'update(loc, k, v) y remove(loc) acceden en O(1) por el índice; '
            'al hacer swap, _index se actualiza',
            ha='center', fontsize=10, color='#37474F', style='italic')

    plt.tight_layout()
    plt.savefig(IMG / 'ch09_adaptable_locators.png', dpi=130, bbox_inches='tight')
    plt.close(fig)
    print('Guardado: ch09_adaptable_locators.png')


if __name__ == '__main__':
    fig_tree_array()
    fig_up_down()
    fig_adaptable()
    print('CH09: figuras generadas en', IMG)
