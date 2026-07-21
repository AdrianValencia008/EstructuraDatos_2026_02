# -*- coding: utf-8 -*-
"""Generador de figuras — CH10 Mapas, Tablas Hash y Skip Lists.

    python generar_figuras/generar_figuras_ch10.py
Vive en generar_figuras/ (en .gitignore, no se versiona).
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

IMG = Path('notebooks/assets')
IMG.mkdir(parents=True, exist_ok=True)

TITLE = '#1A237E'
TEAL_FC, TEAL_EC = '#80CBC4', '#00695C'
BLUE_FC, BLUE_EC = '#90CAF9', '#0D47A1'
ORANGE_FC, ORANGE_EC = '#FFCC80', '#E65100'
GREY_FC, GREY_EC = '#ECEFF1', '#607D8B'


def cell(ax, x, y, w, h, text, fc, ec, fs=11, tc=None, bold=True):
    ax.add_patch(patches.Rectangle((x, y), w, h, fc=fc, ec=ec, lw=1.8, zorder=2))
    if text != '':
        ax.text(x + w / 2, y + h / 2, text, ha='center', va='center',
                fontsize=fs, fontweight='bold' if bold else 'normal',
                color=tc or ec, zorder=3)


# ============ Figura 1: pipeline de la funcion hash ============
def fig_hash_function():
    fig, ax = plt.subplots(figsize=(13, 3.6))
    ax.axis('off'); ax.set_xlim(0, 13); ax.set_ylim(0, 3.4)
    ax.set_title('Función hash en dos etapas:  código hash  →  compresión  →  índice del bucket',
                 fontsize=13.5, fontweight='bold', color=TITLE, pad=10)

    y = 1.3; h = 0.95
    boxes = [
        (0.3, 2.2, "clave k\n'azul'", '#E1BEE7', '#6A1B9A'),
        (3.2, 2.6, 'código hash\nhash(k) = 8273…', '#BBDEFB', '#0D47A1'),
        (6.5, 3.0, 'compresión MAD\n((a·hc + b) mod p) mod N', '#FFE0B2', '#E65100'),
        (10.2, 2.4, 'índice\nh(k) = 6', '#C8E6C9', '#1B5E20'),
    ]
    centers = []
    for x, w, txt, fc, ec in boxes:
        ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.05',
                     fc=fc, ec=ec, lw=2, zorder=2))
        ax.text(x + w / 2, y + h / 2, txt, ha='center', va='center',
                fontsize=10.5, fontweight='bold', color=ec, zorder=3)
        centers.append((x, x + w))
    for i in range(len(boxes) - 1):
        ax.annotate('', xy=(centers[i + 1][0] - 0.05, y + h / 2),
                    xytext=(centers[i][1] + 0.05, y + h / 2),
                    arrowprops=dict(arrowstyle='-|>', color='#37474F', lw=2.2))

    ax.text(6.5, 0.45, 'el código hash depende solo de la clave;  la compresión la encaja en [0, N−1]',
            ha='center', fontsize=10, color='#546E7A', style='italic')

    plt.tight_layout()
    plt.savefig(IMG / 'ch10_hash_function.png', dpi=130, bbox_inches='tight')
    plt.close(fig)
    print('Guardado: ch10_hash_function.png')


# ============ Figura 2: encadenamiento separado ============
def fig_chaining():
    fig, ax = plt.subplots(figsize=(11, 5.6))
    ax.axis('off'); ax.set_xlim(-0.5, 11.5); ax.set_ylim(-0.5, 7.9)
    ax.set_title('Encadenamiento separado (ChainHashMap)',
                 fontsize=13.5, fontweight='bold', color=TITLE, pad=10)

    N = 6
    bw, bh = 1.3, 0.9
    bx = 0.5
    # contenido de cada bucket (lista de (k,v)); algunos con colision
    buckets = {
        0: [],
        1: [('sol', 9)],
        2: [('luna', 3), ('mar', 7)],   # colision
        3: [],
        4: [('rio', 5)],
        5: [('paz', 1), ('luz', 8)],    # colision
    }
    for j in range(N):
        by = (N - 1 - j) * (bh + 0.25) + 0.4
        cell(ax, bx, by, bw, bh, f'[{j}]', GREY_FC, GREY_EC)
        chain = buckets[j]
        if not chain:
            ax.text(bx + bw + 0.6, by + bh / 2, '∅', fontsize=14, color='#B71C1C',
                    ha='center', va='center', fontweight='bold')
            ax.annotate('', xy=(bx + bw + 0.35, by + bh / 2), xytext=(bx + bw, by + bh / 2),
                        arrowprops=dict(arrowstyle='->', color=GREY_EC, lw=1.5))
            continue
        prev = bx + bw
        cx = bx + bw + 0.6
        for (k, v) in chain:
            ax.annotate('', xy=(cx, by + bh / 2), xytext=(prev, by + bh / 2),
                        arrowprops=dict(arrowstyle='->', color=TEAL_EC, lw=1.7))
            cw = 1.9
            cell(ax, cx, by, cw, bh, f'{k}:{v}', TEAL_FC, TEAL_EC, fs=10.5)
            prev = cx + cw
            cx = prev + 0.5

    ax.text(0.5 + bw / 2, 7.55, 'bucket array', ha='center', fontsize=9.5, color='#37474F', style='italic')
    ax.text(7.5, -0.25, 'cada bucket guarda un UnsortedTableMap con las claves que colisionan',
            ha='center', fontsize=9.5, color='#546E7A', style='italic')

    plt.tight_layout()
    plt.savefig(IMG / 'ch10_hash_chaining.png', dpi=130, bbox_inches='tight')
    plt.close(fig)
    print('Guardado: ch10_hash_chaining.png')


# ============ Figura 3: sondeo lineal (open addressing) ============
def fig_probing():
    fig, ax = plt.subplots(figsize=(12, 3.4))
    ax.axis('off'); ax.set_xlim(-0.5, 12.5); ax.set_ylim(-1.8, 2.0)
    ax.set_title('Direccionamiento abierto — sondeo lineal (ProbeHashMap)',
                 fontsize=13.5, fontweight='bold', color=TITLE, pad=10)

    N = 11
    cw = 1.0; y = 0.4
    table = {1: 'sol', 2: 'mar', 3: 'rio', 4: 'luz', 7: 'paz', 8: '_AVAIL', 9: 'luna'}
    for j in range(N):
        x = 0.3 + j * cw
        val = table.get(j, '')
        if val == '_AVAIL':
            cell(ax, x, y, cw, 0.9, 'A', '#FFF59D', '#F9A825', fs=11)
        elif val:
            cell(ax, x, y, cw, 0.9, val, ORANGE_FC, ORANGE_EC, fs=9.5)
        else:
            cell(ax, x, y, cw, 0.9, '', '#FAFAFA', '#BDBDBD')
        ax.text(x + cw / 2, y - 0.28, f'[{j}]', ha='center', fontsize=8.5,
                color='#546E7A', fontweight='bold')

    # ilustrar colision: h('mar')=1 ocupado -> prueba 2
    ax.annotate('', xy=(0.3 + 2 * cw + cw / 2, y + 1.15),
                xytext=(0.3 + 1 * cw + cw / 2, y + 1.15),
                arrowprops=dict(arrowstyle='->', color=ORANGE_EC, lw=2,
                                connectionstyle='arc3,rad=-0.4'))
    ax.text(0.3 + 1.5 * cw, y + 1.55, "colisión en [1] → sondea [2]",
            ha='center', fontsize=9.5, color=ORANGE_EC, fontweight='bold')

    ax.text(6.0, -1.35,
            "todas las entradas viven en el propio arreglo (1 por celda);  "
            "A = _AVAIL marca un borrado",
            ha='center', fontsize=9.5, color='#546E7A', style='italic')

    plt.tight_layout()
    plt.savefig(IMG / 'ch10_hash_probing.png', dpi=130, bbox_inches='tight')
    plt.close(fig)
    print('Guardado: ch10_hash_probing.png')


# ============ Figura 4: skip list ============
def fig_skip_list():
    fig, ax = plt.subplots(figsize=(12, 4.8))
    ax.axis('off'); ax.set_xlim(-0.3, 12.3); ax.set_ylim(-0.6, 4.6)
    ax.set_title('Skip List — jerarquía de listas enlazadas ordenadas',
                 fontsize=13.5, fontweight='bold', color=TITLE, pad=10)

    keys = [12, 17, 20, 25, 31]
    kx = {12: 2.2, 17: 4.2, 20: 6.0, 25: 8.0, 31: 10.0}
    left, right = 0.6, 11.6
    # niveles: que claves aparecen en cada nivel (S0=todas)
    levels = {
        0: [12, 17, 20, 25, 31],
        1: [17, 25],
        2: [17],
        3: [],
    }
    nlev = 4
    ys = {lv: 0.5 + lv * 1.05 for lv in range(nlev)}

    def small(x, y, txt, fc, ec):
        ax.add_patch(patches.Rectangle((x - 0.42, y - 0.27), 0.84, 0.54, fc=fc, ec=ec, lw=1.6, zorder=3))
        ax.text(x, y, txt, ha='center', va='center', fontsize=10, fontweight='bold', color=ec, zorder=4)

    for lv in range(nlev):
        y = ys[lv]
        present = [left] + [kx[k] for k in levels[lv]] + [right]
        # linea horizontal del nivel (cadena de punteros)
        ax.plot([left, right], [y, y], color='#B0BEC5', lw=1.2, zorder=1, linestyle=(0, (4, 3)))
        # centinelas
        small(left, y, '−∞', '#CFD8DC', '#455A64')
        small(right, y, '+∞', '#CFD8DC', '#455A64')
        # nodos -> flechas entre nodos consecutivos
        xs = sorted(present)
        for a, b in zip(xs, xs[1:]):
            ax.annotate('', xy=(b - 0.45, y), xytext=(a + 0.45, y),
                        arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.6, zorder=2))
        for k in levels[lv]:
            small(kx[k], y, str(k), BLUE_FC, BLUE_EC)
        ax.text(-0.1, y, f'S{lv}', ha='right', va='center', fontsize=10,
                fontweight='bold', color='#37474F')

    # torre del 17 (aparece en todos los niveles) resaltada
    for lv in range(nlev):
        small(kx[17], ys[lv], '17', '#FFE082', '#F57F17')

    ax.text(6.0, -0.4,
            'cada clave sube al nivel superior con probabilidad 1/2  →  altura esperada O(log n)',
            ha='center', fontsize=10, color='#546E7A', style='italic')

    plt.tight_layout()
    plt.savefig(IMG / 'ch10_skip_list.png', dpi=130, bbox_inches='tight')
    plt.close(fig)
    print('Guardado: ch10_skip_list.png')


if __name__ == '__main__':
    fig_hash_function()
    fig_chaining()
    fig_probing()
    fig_skip_list()
    print('CH10: figuras generadas en', IMG)
