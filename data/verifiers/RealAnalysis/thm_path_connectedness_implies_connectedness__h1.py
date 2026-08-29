import sympy
from sympy import Interval, FiniteSet, ProductSet, Union, Intersection
from sympy.abc import x, y, z

def is_connected_set(S):
    if not isinstance(S, sympy.Set):
        return False
    if S == sympy.S.Reals:
        return True
    if S in (sympy.S.Rationals, sympy.S.Integers, sympy.S.Naturals, sympy.S.Naturals0):
        return False
    if getattr(S, 'is_empty', False) is True:
        return True
    if isinstance(S, sympy.Interval):
        return True
    if isinstance(S, sympy.FiniteSet):
        return len(S) <= 1
    if isinstance(S, sympy.ProductSet):
        return all(is_connected_set(arg) for arg in S.args)
    return False

def is_graph_connected(edges):
    if not edges:
        return True
    nodes = set()
    for e in edges:
        nodes.add(e[0])
        nodes.add(e[1])
    if not nodes:
        return True
    adj = {n: [] for n in nodes}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    start = next(iter(nodes))
    visited = set()
    queue = [start]
    while queue:
        curr = queue.pop(0)
        if curr not in visited:
            visited.add(curr)
            queue.extend(adj[curr])
    return len(visited) == len(nodes)

def check_path_connected(w):
    if hasattr(w, 'is_path_connected'):
        val = w.is_path_connected
        return val() if callable(val) else bool(val)
    if isinstance(w, (int, float, sympy.Number)):
        return True
    if isinstance(w, list) and all(isinstance(e, (tuple, list)) and len(e) == 2 for e in w):
        return is_graph_connected(w)
    return is_connected_set(w)

def check_connected(w):
    if hasattr(w, 'is_connected'):
        val = w.is_connected
        return val() if callable(val) else bool(val)
    if isinstance(w, (int, float, sympy.Number)):
        return True
    if isinstance(w, list) and all(isinstance(e, (tuple, list)) and len(e) == 2 for e in w):
        return is_graph_connected(w)
    return is_connected_set(w)

def conditions(witness):
    try:
        h1 = bool(check_path_connected(witness))
    except Exception:
        h1 = False
        
    try:
        q = bool(check_connected(witness))
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: X is path-connected",
    "¬Q: X is not a connected space"
]

N_HYP = 1
NEG_Q_INDEX = 1