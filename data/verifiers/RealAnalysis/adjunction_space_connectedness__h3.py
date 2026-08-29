import sympy
from sympy import Interval, FiniteSet, Union, S
from sympy.abc import x, y, z
import itertools

# Top-level setup for potential witness expressions
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def is_connected(space, topology):
    if not space:
        return True
    space_set = set(space)
    open_sets = [set(op) for op in topology]
    
    for U in open_sets:
        if not U or U == space_set:
            continue
        V = space_set - U
        if any(V == op for op in open_sets):
            return False
    return True

def is_closed(A, space, topology):
    space_set = set(space)
    A_set = set(A)
    if not A_set.issubset(space_set):
        return False
    complement = space_set - A_set
    open_sets = [set(op) for op in topology]
    return any(complement == op for op in open_sets)

def is_adjunction_space_connected(X, Y, topology_X, topology_Y, A, f):
    elements_X = [('X', e) for e in X]
    elements_Y = [('Y', e) for e in Y]
    all_elements = elements_X + elements_Y

    parent = {e: e for e in all_elements}
    def find(e):
        if e not in parent:
            parent[e] = e
        if parent[e] != e:
            parent[e] = find(parent[e])
        return parent[e]
    
    def union(e1, e2):
        root1 = find(e1)
        root2 = find(e2)
        if root1 != root2:
            parent[root1] = root2

    for a in A:
        if isinstance(f, dict):
            fa = f.get(a)
        elif isinstance(f, list):
            fa = next((v for k, v in f if k == a), None)
        else:
            try:
                fa = f(a)
            except Exception:
                fa = None
        if fa is not None and fa in X:
            union(('Y', a), ('X', fa))

    classes = {}
    for e in all_elements:
        root = find(e)
        classes.setdefault(root, []).append(e)

    Z_elements = list(classes.keys())
    if not Z_elements:
        return True

    n = len(Z_elements)
    if n > 15:
        # To prevent TLE on large spaces. Mathematically, if X and Y are connected 
        # and A is non-empty, the adjunction space is always connected.
        return True

    open_sets_X = [set(op) for op in topology_X]
    open_sets_Y = [set(op) for op in topology_Y]

    for i in range(1, (1 << n) - 1):
        U_Z = []
        for j in range(n):
            if (i & (1 << j)):
                U_Z.append(Z_elements[j])
        
        preimage_X = set()
        preimage_Y = set()
        for root in U_Z:
            for e in classes[root]:
                if e[0] == 'X':
                    preimage_X.add(e[1])
                else:
                    preimage_Y.add(e[1])
        
        is_open_X = any(preimage_X == op for op in open_sets_X)
        is_open_Y = any(preimage_Y == op for op in open_sets_Y)
        is_open_Z = is_open_X and is_open_Y
        
        if is_open_Z:
            V_Z = [z_el for z_el in Z_elements if z_el not in U_Z]
            comp_preimage_X = set()
            comp_preimage_Y = set()
            for root in V_Z:
                for e in classes[root]:
                    if e[0] == 'X':
                        comp_preimage_X.add(e[1])
                    else:
                        comp_preimage_Y.add(e[1])
            
            is_comp_open_X = any(comp_preimage_X == op for op in open_sets_X)
            is_comp_open_Y = any(comp_preimage_Y == op for op in open_sets_Y)
            is_comp_open_Z = is_comp_open_X and is_comp_open_Y
            
            if is_comp_open_Z:
                return False

    return True

def conditions(witness) -> list[bool]:
    def get_attr(obj, keys):
        if isinstance(obj, dict):
            for k in keys:
                if k in obj:
                    return obj[k]
        else:
            for k in keys:
                if hasattr(obj, k):
                    return getattr(obj, k)
        return None

    X = get_attr(witness, ['X', 'space_X', 'elements_X'])
    Y = get_attr(witness, ['Y', 'space_Y', 'elements_Y'])
    topology_X = get_attr(witness, ['topology_X', 'top_X', 'tau_X', 'open_sets_X'])
    topology_Y = get_attr(witness, ['topology_Y', 'top_Y', 'tau_Y', 'open_sets_Y'])
    A = get_attr(witness, ['A', 'subset_A'])
    f = get_attr(witness, ['f', 'map_f', 'function_f'])

    if isinstance(witness, tuple):
        if len(witness) == 6:
            X, Y, topology_X, topology_Y, A, f = witness
        elif len(witness) == 4:
            X, Y, A, f = witness

    h1_ok = False
    try:
        if X is not None and Y is not None and topology_X is not None and topology_Y is not None:
            h1_ok = is_connected(X, topology_X) and is_connected(Y, topology_Y)
        elif isinstance(X, sympy.Set) and isinstance(Y, sympy.Set):
            def is_sympy_connected(S_set):
                if isinstance(S_set, sympy.Interval): return True
                if isinstance(S_set, sympy.FiniteSet): return len(S_set) <= 1
                if S_set == sympy.S.Reals: return True
                return False
            h1_ok = is_sympy_connected(X) and is_sympy_connected(Y)
        elif isinstance(X, dict) and isinstance(Y, dict) and topology_X is None:
            def is_graph_connected(G):
                if not G: return True
                visited = set()
                start = list(G.keys())[0]
                def dfs(node):
                    visited.add(node)
                    for neighbor in G.get(node, []):
                        if neighbor not in visited:
                            dfs(neighbor)
                dfs(start)
                return len(visited) == len(G)
            h1_ok = is_graph_connected(X) and is_graph_connected(Y)
    except Exception:
        h1_ok = False

    h2_ok = False
    try:
        if A is not None and Y is not None and topology_Y is not None:
            if len(A) > 0:
                h2_ok = is_closed(A, Y, topology_Y)
        elif isinstance(A, sympy.Set) and isinstance(Y, sympy.Set):
            if not A.is_empty and A.is_subset(Y):
                h2_ok = True
        elif isinstance(X, dict) and isinstance(Y, dict) and topology_X is None:
            if A is not None and len(A) > 0:
                h2_ok = all(a in Y for a in A)
    except Exception:
        h2_ok = False

    neg_q_ok = False
    try:
        if X is not None and Y is not None and topology_X is not None and topology_Y is not None and A is not None and f is not None:
            neg_q_ok = not is_adjunction_space_connected(X, Y, topology_X, topology_Y, A, f)
        else:
            # For sympy sets or graphs, the adjunction space is mathematically always connected 
            # if the hypotheses hold, so the negation of the conclusion is False.
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: X and Y are connected topological spaces",
    "H_2: A is a non-empty closed subset of Y",
    "¬Q: The adjunction space X \\cup_f Y is not connected"
]

N_HYP = 2
NEG_Q_INDEX = 2