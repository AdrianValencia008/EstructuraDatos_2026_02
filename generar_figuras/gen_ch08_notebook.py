"""Genera ch08_teoria.ipynb con el contenido completo del capítulo 8."""
import json, pathlib

OUT = pathlib.Path(
    r'c:\Users\fator\Desktop\Proyectos1\Estructura_Datos_Repo'
    r'\notebooks\ch08_trees\ch08_teoria.ipynb'
)

def md(src, cid):
    return {"cell_type": "markdown", "id": cid, "metadata": {}, "source": src}

def code(src, cid):
    return {"cell_type": "code", "execution_count": None,
            "id": cid, "metadata": {}, "outputs": [], "source": src}

cells = []

# ── Título ────────────────────────────────────────────────────────────────────
cells.append(md(
    "# CH08 — Árboles\n\n"
    "Material del curso basado en Goodrich, Tamassia & Goldwasser — Capítulo 8.",
    "c8t00"
))

# ── 8.1 Árbol General ────────────────────────────────────────────────────────
cells.append(md(
    "## 8.1 Árbol General (*General Tree*)\n\n"
    "Un **árbol** es una estructura de datos no lineal que modela una relación "
    "jerárquica entre objetos. Formalmente es un conjunto de **nodos** con las "
    "siguientes propiedades:\n\n"
    "- Existe exactamente un nodo especial llamado **raíz** (*root*) que no tiene padre.\n"
    "- Cada nodo distinto de la raíz tiene exactamente **un padre**.\n"
    "- Los nodos que no tienen hijos se llaman **hojas** (*leaves*).\n"
    "- Los nodos con al menos un hijo son **nodos internos**.\n\n"
    "**Terminología clave:**\n\n"
    "| Término | Definición |\n"
    "|---|---|\n"
    "| **padre** (*parent*) | El nodo directamente encima de `v` en la jerarquía |\n"
    "| **hijo** (*child*) | Nodo directamente por debajo de `v` |\n"
    "| **hermanos** (*siblings*) | Nodos con el mismo padre |\n"
    "| **ancestros** | Padre, abuelo, ... hasta la raíz |\n"
    "| **descendientes** | Hijos, nietos, ... hasta las hojas |\n"
    "| **profundidad** (*depth*) de `v` | Número de aristas desde la raíz hasta `v` |\n"
    "| **altura** (*height*) del árbol | Profundidad máxima de cualquier hoja |\n\n"
    "**ADT Árbol — operaciones principales:**\n\n"
    "| Operación | Descripción | $O$ |\n"
    "|---|---|---|\n"
    "| `T.root()` | Retorna la posición de la raíz | $O(1)$ |\n"
    "| `T.parent(p)` | Posición del padre de `p` | $O(1)$ |\n"
    "| `T.children(p)` | Iterador de los hijos de `p` | $O(c_p)$ |\n"
    "| `T.num_children(p)` | Número de hijos de `p` | $O(1)$ |\n"
    "| `T.is_root(p)` | `True` si `p` es la raíz | $O(1)$ |\n"
    "| `T.is_leaf(p)` | `True` si `p` no tiene hijos | $O(1)$ |\n"
    "| `T.depth(p)` | Profundidad de `p` | $O(d_p)$ |\n"
    "| `T.height(p)` | Altura del subárbol en `p` | $O(n)$ |\n"
    "| `len(T)` | Número de nodos | $O(1)$ |",
    "c8t01"
))

cells.append(md(
    "![Árbol General — Terminología](../assets/ch08_general_tree.png)",
    "c8t01img"
))

cells.append(code(
    "import sys\n"
    "sys.path.append(r'C:\\Users\\fator\\Desktop\\Proyectos1\\Estructura_Datos_Repo')\n"
    "from goodrich.ch08.linked_binary_tree import LinkedBinaryTree",
    "c8t01imp"
))

cells.append(code(
    "# Construimos el árbol:\n"
    "#        1\n"
    "#       / \\\n"
    "#      2   3\n"
    "#     / \\   \\\n"
    "#    4   5   6\n\n"
    "T = LinkedBinaryTree()\n"
    "r = T._add_root(1)\n"
    "b = T._add_left(r, 2)\n"
    "c = T._add_right(r, 3)\n"
    "d = T._add_left(b, 4)\n"
    "e = T._add_right(b, 5)\n"
    "f = T._add_right(c, 6)\n\n"
    "print(f'Tamaño:          {len(T)} nodos')\n"
    "print(f'Raíz:            {T.root().element()}')\n"
    "print(f'Altura total:    {T.height(T.root())}')\n"
    "print(f'Profundidad(4):  {T.depth(d)}')\n"
    "print(f'Es hoja(4):      {T.is_leaf(d)}')\n"
    "print(f'Es hoja(2):      {T.is_leaf(b)}')",
    "c8t01ex"
))

# ── 8.2 Árbol Binario ────────────────────────────────────────────────────────
cells.append(md(
    "## 8.2 Árbol Binario (*Binary Tree*)\n\n"
    "Un **árbol binario** es un árbol ordenado en el que cada nodo tiene "
    "**a lo sumo 2 hijos**, denominados **hijo izquierdo** y **hijo derecho**. "
    "El hijo izquierdo siempre precede al derecho en el orden.\n\n"
    "**Propiedades de un árbol binario de altura $h$:**\n\n"
    "| Propiedad | Valor |\n"
    "|---|---|\n"
    "| Número máximo de nodos en nivel $k$ | $2^k$ |\n"
    "| Número máximo de nodos totales | $2^{h+1} - 1$ |\n"
    "| Número mínimo de hojas | $h + 1$ |\n"
    "| Relación hojas/nodos internos (árbol propio) | hojas $=$ internos $+ 1$ |\n\n"
    "**Árbol binario propio (*proper/full*):** cada nodo tiene 0 ó 2 hijos — nunca 1.\n\n"
    "**ADT Árbol Binario — operaciones adicionales a `Tree`:**\n\n"
    "| Operación | Descripción | $O$ |\n"
    "|---|---|---|\n"
    "| `T.left(p)` | Hijo izquierdo de `p` (`None` si no existe) | $O(1)$ |\n"
    "| `T.right(p)` | Hijo derecho de `p` (`None` si no existe) | $O(1)$ |\n"
    "| `T.sibling(p)` | Hermano de `p` (`None` si no existe) | $O(1)$ |\n"
    "| `T.inorder()` | Recorrido en inorden (izq → raíz → der) | $O(n)$ |",
    "c8t02"
))

cells.append(md(
    "![Árbol Binario — Estructura y terminología](../assets/ch08_binary_tree.png)",
    "c8t02img"
))

cells.append(code(
    "# Construir el árbol de la figura:\n"
    "#       A\n"
    "#      / \\\n"
    "#     B   C\n"
    "#    / \\ / \\\n"
    "#   D  E F  G\n\n"
    "T2 = LinkedBinaryTree()\n"
    "a = T2._add_root('A')\n"
    "b = T2._add_left(a, 'B')\n"
    "c = T2._add_right(a, 'C')\n"
    "d = T2._add_left(b, 'D')\n"
    "e = T2._add_right(b, 'E')\n"
    "f = T2._add_left(c, 'F')\n"
    "g = T2._add_right(c, 'G')\n\n"
    "print(f'Raíz:          {T2.root().element()}')\n"
    "print(f'Izq(A):        {T2.left(a).element()}')\n"
    "print(f'Der(A):        {T2.right(a).element()}')\n"
    "print(f'Izq(B):        {T2.left(b).element()}')\n"
    "print(f'Hermano(B):    {T2.sibling(b).element()}')\n"
    "print(f'Altura:        {T2.height(T2.root())}')\n"
    "print(f'Hojas:         {sum(1 for p in T2.positions() if T2.is_leaf(p))}')",
    "c8t02ex"
))

# ── 8.3 Implementación LinkedBinaryTree ──────────────────────────────────────
cells.append(md(
    "## 8.3 Implementación: `LinkedBinaryTree`\n\n"
    "`LinkedBinaryTree` usa nodos enlazados donde cada nodo guarda cuatro "
    "referencias: padre, hijo izquierdo, hijo derecho y el elemento.\n\n"
    "```python\n"
    "class _Node:\n"
    "    __slots__ = '_element', '_parent', '_left', '_right'\n"
    "```\n\n"
    "**API interna** (uso del implementador — no la expone el ADT público):\n\n"
    "| Método | Descripción |\n"
    "|---|---|\n"
    "| `T._add_root(e)` | Agrega la raíz; lanza error si ya existe |\n"
    "| `T._add_left(p, e)` | Agrega hijo izquierdo a `p` |\n"
    "| `T._add_right(p, e)` | Agrega hijo derecho a `p` |\n"
    "| `T._replace(p, e)` | Reemplaza el elemento en `p`, retorna el anterior |\n"
    "| `T._delete(p)` | Elimina `p` (debe tener a lo sumo un hijo) |\n"
    "| `T._attach(p, t1, t2)` | Adjunta `t1` (izq) y `t2` (der) como subárboles de la hoja `p` |\n\n"
    "**Patrón `Position`:** la clase `Position` envuelve un nodo y solo expone "
    "`.element()`. Esto protege la estructura interna — el usuario del ADT nunca "
    "manipula los nodos directamente.",
    "c8t03"
))

cells.append(code(
    "# Árbol de expresión: (3 + 1) × (9 − 5)\n"
    "#          ×\n"
    "#         / \\\n"
    "#        +   −\n"
    "#       / \\ / \\\n"
    "#      3  1 9  5\n\n"
    "expr = LinkedBinaryTree()\n"
    "mul = expr._add_root('x')\n"
    "add = expr._add_left(mul, '+')\n"
    "sub = expr._add_right(mul, '-')\n"
    "expr._add_left(add, 3)\n"
    "expr._add_right(add, 1)\n"
    "expr._add_left(sub, 9)\n"
    "expr._add_right(sub, 5)\n\n"
    "print('Tamaño:', len(expr))\n"
    "print('Raíz:', expr.root().element())\n"
    "print('Operandos de +:', expr.left(add).element(), expr.right(add).element())\n"
    "print('Operandos de -:', expr.left(sub).element(), expr.right(sub).element())",
    "c8t03ex"
))

# ── 8.4 Recorridos ───────────────────────────────────────────────────────────
cells.append(md(
    "## 8.4 Recorridos (*Tree Traversals*)\n\n"
    "Un recorrido visita sistemáticamente **todos los nodos** del árbol exactamente "
    "una vez. El orden de visita define el tipo de recorrido.\n\n"
    "| Recorrido | Orden | Complejidad | Caso de uso típico |\n"
    "|---|---|---|---|\n"
    "| **Preorden** | Raíz → Izq → Der | $O(n)$ | Copiar árbol, TOC de documentos |\n"
    "| **Inorden** | Izq → Raíz → Der | $O(n)$ | Ordenar BST, expresión infija |\n"
    "| **Postorden** | Izq → Der → Raíz | $O(n)$ | Eliminar árbol, tamaño de directorios |\n"
    "| **Por niveles (BFS)** | Nivel 0 → Nivel 1 → ... | $O(n)$ | Buscar nodo más cercano |\n\n"
    "**Preorden:** el nodo se visita *antes* que sus descendientes — "
    "\"procesar primero la raíz\".\n\n"
    "**Postorden:** el nodo se visita *después* de sus descendientes — "
    "\"procesar cuando ya conocemos los resultados de los hijos\".\n\n"
    "**Inorden** (solo árboles binarios): la raíz queda *entre* sus dos "
    "subárboles — produce el orden ascendente en un BST.\n\n"
    "**Por niveles:** usa una **cola** interna; procesa todos los nodos de "
    "un nivel antes de pasar al siguiente.",
    "c8t04"
))

cells.append(md(
    "![Recorridos de Árboles Binarios](../assets/ch08_traversals.png)",
    "c8t04img"
))

cells.append(code(
    "# Preorden: Raíz → Izq → Der\n"
    "print('Preorden:  ', end='')\n"
    "for p in T.preorder():\n"
    "    print(p.element(), end=' ')\n"
    "print()\n\n"
    "# Postorden: Izq → Der → Raíz\n"
    "print('Postorden: ', end='')\n"
    "for p in T.postorder():\n"
    "    print(p.element(), end=' ')\n"
    "print()",
    "c8t04pre"
))

cells.append(code(
    "# Inorden: Izq → Raíz → Der (solo árboles binarios)\n"
    "print('Inorden:   ', end='')\n"
    "for p in T.inorder():\n"
    "    print(p.element(), end=' ')\n"
    "print()\n\n"
    "# Por niveles (BFS)\n"
    "print('BFS:       ', end='')\n"
    "for p in T.breadthfirst():\n"
    "    print(p.element(), end=' ')\n"
    "print()",
    "c8t04bfs"
))

# ── 8.5 Árbol de Expresiones ─────────────────────────────────────────────────
cells.append(md(
    "## 8.5 Árbol de Expresiones (*Expression Tree*)\n\n"
    "Un **árbol de expresión** es un árbol binario propio donde:\n"
    "- Las **hojas** almacenan valores numéricos (operandos).\n"
    "- Los **nodos internos** almacenan operadores (`+`, `−`, `×`, `/`).\n\n"
    "**Recorridos y su significado:**\n\n"
    "| Recorrido | Resultado para `(3 + 1) × (9 − 5)` | Notación |\n"
    "|---|---|---|\n"
    "| Inorden + paréntesis | `(3 + 1) × (9 − 5)` | Infija |\n"
    "| Preorden | `× + 3 1 − 9 5` | Prefija (polaca) |\n"
    "| Postorden | `3 1 + 9 5 − ×` | Posfija (RPN) |\n\n"
    "**Evaluación recursiva** (recorrido postorden):\n\n"
    "```\n"
    "evaluar(nodo):\n"
    "  si es hoja → retornar nodo.valor\n"
    "  izq = evaluar(nodo.izquierdo)\n"
    "  der = evaluar(nodo.derecho)\n"
    "  retornar izq ⊕ der   # ⊕ es el operador del nodo\n"
    "```",
    "c8t05"
))

cells.append(code(
    "import operator\n\n"
    "OPS = {'+': operator.add, '-': operator.sub,\n"
    "       'x': operator.mul, '/': operator.truediv}\n\n"
    "def evaluar(T, p):\n"
    "    \"\"\"Evalúa recursivamente el árbol de expresión (recorrido postorden).\"\"\"\n"
    "    if T.is_leaf(p):\n"
    "        return p.element()\n"
    "    izq = evaluar(T, T.left(p))\n"
    "    der = evaluar(T, T.right(p))\n"
    "    return OPS[p.element()](izq, der)\n\n"
    "# Árbol: (3 + 1) × (9 - 5)\n"
    "resultado = evaluar(expr, expr.root())\n"
    "print(f'(3 + 1) x (9 - 5) = {resultado}')  # 16",
    "c8t05ex"
))

# ── Comparación ───────────────────────────────────────────────────────────────
cells.append(md(
    "## Comparación: Árbol vs Lista vs Arreglo\n\n"
    "| Operación | Arreglo | Lista enlazada | Árbol binario* |\n"
    "|---|---|---|---|\n"
    "| Acceso por índice | $O(1)$ | $O(n)$ | — |\n"
    "| Búsqueda | $O(n)$ | $O(n)$ | $O(\\log n)$\\* |\n"
    "| Inserción ordenada | $O(n)$ | $O(n)$ | $O(\\log n)$\\* |\n"
    "| Profundidad de un nodo | — | — | $O(h)$ |\n"
    "| Recorrido completo | $O(n)$ | $O(n)$ | $O(n)$ |\n"
    "| Memoria por elemento | Compacta | Nodo + 1–2 ptr | Nodo + 3 ptr |\n\n"
    "\\* Para árbol binario de búsqueda (BST) balanceado con $h = O(\\log n)$.\n\n"
    "**Cuándo usar árboles:**\n"
    "- Datos con estructura jerárquica natural (sistemas de archivos, XML/HTML).\n"
    "- Búsqueda, inserción y eliminación eficiente en datos ordenados (BST — Ch09).\n"
    "- Expresiones y parsing (compiladores, calculadoras).\n"
    "- Algoritmos de búsqueda en grafos (árboles de expansión — Ch14).",
    "c8cmp"
))

# ── Ejercicios ────────────────────────────────────────────────────────────────
cells.append(md(
    "---\n\n"
    "## Ejercicios\n\n"
    "Ejercicios seleccionados de Goodrich, Tamassia & Goldwasser — "
    "*Data Structures and Algorithms in Python*, Capítulo 8.\n"
    "Completa los métodos marcados con `raise NotImplementedError`.",
    "c8e00"
))

# ── Ejercicio 1 ───────────────────────────────────────────────────────────────
cells.append(md(
    "### Ejercicio 1 — Contar hojas *(R-8.1)*\n\n"
    "Implementa `contar_hojas(T)` que reciba un `LinkedBinaryTree` y retorne "
    "el número de **hojas** (nodos sin hijos). Usa un recorrido recursivo.\n\n"
    "**Pista:** un nodo es hoja si `T.is_leaf(p)` retorna `True`.",
    "c8e01"
))

cells.append(code(
    "def contar_hojas(T):\n"
    "    \"\"\"Retorna el número de hojas del árbol T.\"\"\"\n"
    "    raise NotImplementedError\n\n\n"
    "# --- Tests ---\n"
    "T_e = LinkedBinaryTree()\n"
    "r_e = T_e._add_root(1)\n"
    "b_e = T_e._add_left(r_e, 2)\n"
    "c_e = T_e._add_right(r_e, 3)\n"
    "T_e._add_left(b_e, 4)\n"
    "T_e._add_right(b_e, 5)\n"
    "T_e._add_right(c_e, 6)\n"
    "print(contar_hojas(T_e))        # 3  (nodos 4, 5, 6)\n\n"
    "T_sola = LinkedBinaryTree()\n"
    "T_sola._add_root(99)\n"
    "print(contar_hojas(T_sola))     # 1",
    "c8e01c"
))

# ── Ejercicio 2 ───────────────────────────────────────────────────────────────
cells.append(md(
    "### Ejercicio 2 — Altura de un subárbol *(R-8.3)*\n\n"
    "Implementa `altura_subarbol(T, p)` que calcule la altura del subárbol "
    "con raíz en la posición `p` **sin usar `T.height()`**. Debe funcionar "
    "recursivamente.\n\n"
    "**Recuerda:** la altura de una hoja es 0; la de un nodo interno es "
    "$1 + \\max(\\text{altura\\_izq}, \\text{altura\\_der})$.",
    "c8e02"
))

cells.append(code(
    "def altura_subarbol(T, p):\n"
    "    \"\"\"Calcula la altura del subárbol con raíz en p sin usar T.height().\"\"\"\n"
    "    raise NotImplementedError\n\n\n"
    "# --- Tests ---\n"
    "T_a = LinkedBinaryTree()\n"
    "r_a = T_a._add_root('A')\n"
    "b_a = T_a._add_left(r_a, 'B')\n"
    "c_a = T_a._add_right(r_a, 'C')\n"
    "d_a = T_a._add_left(b_a, 'D')\n"
    "print(altura_subarbol(T_a, r_a))   # 2\n"
    "print(altura_subarbol(T_a, b_a))   # 1\n"
    "print(altura_subarbol(T_a, d_a))   # 0  (es hoja)",
    "c8e02c"
))

# ── Ejercicio 3 ───────────────────────────────────────────────────────────────
cells.append(md(
    "### Ejercicio 3 — Nodos en nivel $k$ *(R-8.6)*\n\n"
    "Implementa `nodos_en_nivel(T, k)` que retorne una **lista con los elementos** "
    "de todos los nodos que están a profundidad exactamente `k`. "
    "Puedes usar BFS o recursión.\n\n"
    "**Casos borde:** si `k` es mayor que la altura del árbol, retornar lista vacía.",
    "c8e03"
))

cells.append(code(
    "def nodos_en_nivel(T, k):\n"
    "    \"\"\"Retorna la lista de elementos de todos los nodos a profundidad k.\"\"\"\n"
    "    raise NotImplementedError\n\n\n"
    "# --- Tests ---\n"
    "T_n = LinkedBinaryTree()\n"
    "r_n = T_n._add_root('A')\n"
    "b_n = T_n._add_left(r_n, 'B')\n"
    "c_n = T_n._add_right(r_n, 'C')\n"
    "T_n._add_left(b_n, 'D')\n"
    "T_n._add_right(b_n, 'E')\n"
    "T_n._add_right(c_n, 'F')\n\n"
    "print(nodos_en_nivel(T_n, 0))   # ['A']\n"
    "print(nodos_en_nivel(T_n, 1))   # ['B', 'C']\n"
    "print(nodos_en_nivel(T_n, 2))   # ['D', 'E', 'F']\n"
    "print(nodos_en_nivel(T_n, 5))   # []",
    "c8e03c"
))

# ── Ejercicio 4 ───────────────────────────────────────────────────────────────
cells.append(md(
    "### Ejercicio 4 — ¿Es árbol binario completo? *(C-8.32)*\n\n"
    "Implementa `es_completo(T)` que retorne `True` si `T` es un "
    "**árbol binario completo**: todos los niveles están llenos excepto "
    "posiblemente el último, que se llena **de izquierda a derecha**.\n\n"
    "**Pista:** usa BFS. Un árbol es completo si, al recorrer por niveles, "
    "nunca aparece un nodo con hijo después de haber encontrado una posición "
    "vacía.",
    "c8e04"
))

cells.append(code(
    "def es_completo(T):\n"
    "    \"\"\"Retorna True si T es un árbol binario completo.\"\"\"\n"
    "    raise NotImplementedError\n\n\n"
    "# --- Tests ---\n"
    "# Árbol completo: 1 → {2,3} → {4,5,6}\n"
    "T_c = LinkedBinaryTree()\n"
    "r_c = T_c._add_root(1)\n"
    "b_c = T_c._add_left(r_c, 2)\n"
    "c_c = T_c._add_right(r_c, 3)\n"
    "T_c._add_left(b_c, 4)\n"
    "T_c._add_right(b_c, 5)\n"
    "T_c._add_left(c_c, 6)\n"
    "print(es_completo(T_c))    # True\n\n"
    "# Árbol NO completo: falta hijo der(B) pero existe hijo en C\n"
    "T_nc = LinkedBinaryTree()\n"
    "r_nc = T_nc._add_root(1)\n"
    "b_nc = T_nc._add_left(r_nc, 2)\n"
    "c_nc = T_nc._add_right(r_nc, 3)\n"
    "T_nc._add_left(b_nc, 4)\n"
    "T_nc._add_right(c_nc, 5)\n"
    "print(es_completo(T_nc))   # False",
    "c8e04c"
))

# ── Ejercicio 5 ───────────────────────────────────────────────────────────────
cells.append(md(
    "### Ejercicio 5 — Preorden iterativo *(C-8.38)*\n\n"
    "Implementa `preorden_iterativo(T)` que retorne la lista de elementos "
    "en **preorden** usando una **pila explícita** — sin usar recursión ni "
    "`T.preorder()`.\n\n"
    "**Pista:** inicializa la pila con la raíz. En cada paso: desapila, "
    "agrega al resultado, apila primero el hijo **derecho** y luego el "
    "**izquierdo** (para que izquierdo salga primero).",
    "c8e05"
))

cells.append(code(
    "def preorden_iterativo(T):\n"
    "    \"\"\"Preorden con pila explícita; retorna lista de elementos.\"\"\"\n"
    "    raise NotImplementedError\n\n\n"
    "# --- Tests ---\n"
    "# Árbol T (definido al inicio del notebook):\n"
    "#    1\n"
    "#   / \\\n"
    "#  2   3\n"
    "# / \\   \\\n"
    "#4   5   6\n"
    "print(preorden_iterativo(T))   # [1, 2, 4, 5, 3, 6]\n\n"
    "# Árbol de un solo nodo\n"
    "T_uno = LinkedBinaryTree()\n"
    "T_uno._add_root(42)\n"
    "print(preorden_iterativo(T_uno))  # [42]",
    "c8e05c"
))

# ── Ejercicio 6 ───────────────────────────────────────────────────────────────
cells.append(md(
    "### Ejercicio 6 — ¿Son árboles espejo? *(C-8.40)*\n\n"
    "Implementa `son_espejo(T1, T2)` que retorne `True` si `T2` es la "
    "imagen espejo de `T1` (es decir, `T2` es `T1` reflejado horizontalmente).\n\n"
    "**Dos árboles son espejos si:**\n"
    "- Sus raíces tienen el mismo elemento.\n"
    "- El hijo izquierdo de `T1` es espejo del hijo **derecho** de `T2`, y viceversa.\n\n"
    "**Casos borde:** dos árboles vacíos son espejos; un árbol vacío y uno no "
    "vacío no lo son.",
    "c8e06"
))

cells.append(code(
    "def son_espejo(T1, T2):\n"
    "    \"\"\"Retorna True si T2 es la imagen espejo de T1.\"\"\"\n"
    "    raise NotImplementedError\n\n\n"
    "# --- Tests ---\n"
    "# T_orig:     1          T_mirror:    1\n"
    "#            / \\                      / \\\n"
    "#           2   3                    3   2\n"
    "#          /     \\                  /     \\\n"
    "#         4       5                5       4\n"
    "T_orig = LinkedBinaryTree()\n"
    "ro = T_orig._add_root(1)\n"
    "bo = T_orig._add_left(ro, 2)\n"
    "co = T_orig._add_right(ro, 3)\n"
    "T_orig._add_left(bo, 4)\n"
    "T_orig._add_right(co, 5)\n\n"
    "T_mirror = LinkedBinaryTree()\n"
    "rm = T_mirror._add_root(1)\n"
    "bm = T_mirror._add_left(rm, 3)\n"
    "cm = T_mirror._add_right(rm, 2)\n"
    "T_mirror._add_left(bm, 5)\n"
    "T_mirror._add_right(cm, 4)\n\n"
    "print(son_espejo(T_orig, T_mirror))  # True\n"
    "print(son_espejo(T_orig, T_orig))    # False  (no es su propio espejo)",
    "c8e06c"
))

# ─────────────────────────────────────────────────────────────────────────────
# Serializar y guardar
# ─────────────────────────────────────────────────────────────────────────────
notebook = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.11.0"
        }
    },
    "cells": cells
}

with open(OUT, 'w', encoding='utf-8') as fh:
    json.dump(notebook, fh, ensure_ascii=False, indent=1)

print(f'Guardado: {OUT}')
print(f'Celdas totales: {len(cells)}')
