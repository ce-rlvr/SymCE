import sympy
import math
import itertools
import functools

# Top-level setup
# (No specific named objects required for this general topology verifier)

def get_attr_or_key(obj, name):
    if isinstance(obj, dict) and name in obj:
        return obj[name]
    if hasattr(obj, name):
        return getattr(obj, name)
    raise KeyError(name)

def get_topology(X, T):
    """
    Generates the full topology (closed under unions and intersections) 
    from a given family of sets T on the space X.
    """
    T_full = set(frozenset(s) for s in T)
    T_full.add(frozenset())
    T_full.add(frozenset(X))
    
    while True:
        new_sets = set()
        for A in T_full:
            for B in T_full:
                C_union = A.union(B)
                C_inter = A.intersection(B)
                if C_union not in T_full:
                    new_sets.add(C_union)
                if C_inter not in T_full:
                    new_sets.add(C_inter)
        if not new_sets:
            break
        T_full.update(new_sets)
        
    return [set(s) for s in T_full]

def is_connected(X, T):
    """
    Checks if a finite topological space X with topology T is connected.
    Uses the property that clopens in a finite space correspond to 
    connected components in the undirected graph where edges are defined 
    by the minimal open sets containing each point.
    """
    elements = list(X)
    if not elements:
        return True
    
    min_open = {}
    for p in elements:
        containing = [U for U in T if p in U]
        if containing:
            min_open[p] = set.intersection(*[set(U) for U in containing])
        else:
            min_open[p] = set()
            
    adj = {p: set() for p in elements}
    for p in elements:
        for q in min_open[p]:
            if q in adj:
                adj[p].add(q)
                adj[q].add(p)
                
    start = elements[0]
    visited = set([start])
    queue = [start]
    
    while queue:
        curr = queue.pop(0)
        for neighbor in adj[curr]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                
    return len(visited) == len(elements)

def is_continuous(X, Y, T_X, T_Y, f):
    """
    Checks if f is a continuous function from (X, T_X) to (Y, T_Y).
    """
    for x in X:
        if x not in f or f[x] not in Y:
            return False
    for V in T_Y:
        V_set = set(V)
        preimage = {x for x in X if f.get(x) in V_set}
        if not any(set(U) == preimage for U in T_X):
            return False
    return True

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness should represent finite topological spaces X and Y, and a function f.
    """
    try:
        X = get_attr_or_key(witness, 'X')
        T_X_raw = get_attr_or_key(witness, 'topology_X')
        Y = get_attr_or_key(witness, 'Y')
        T_Y_raw = get_attr_or_key(witness, 'topology_Y')
        f_raw = get_attr_or_key(witness, 'f')
        
        if callable(f_raw):
            f = {x: f_raw(x) for x in X}
        else:
            f = f_raw
            
        T_X = get_topology(X, T_X_raw)
        T_Y = get_topology(Y, T_Y_raw)
        
    except Exception:
        return [False, False, False]
        
    # H_1: X is a connected space
    try:
        h1 = is_connected(X, T_X)
    except Exception:
        h1 = False
        
    # H_2: f: X -> Y is a continuous function
    try:
        h2 = is_continuous(X, Y, T_X, T_Y, f)
    except Exception:
        h2 = False
        
    # ¬Q: The graph G is not a connected subset of X x Y
    try:
        try:
            # Allow the witness to provide a custom topology on X x Y
            T_XY_raw = get_attr_or_key(witness, 'topology_XY')
            T_XY = get_topology([(x, y) for x in X for y in Y], T_XY_raw)
        except Exception:
            T_XY = None
            
        G = {(x, f[x]) for x in X}
        if not G:
            neg_q = False
        else:
            if T_XY is not None:
                basic_open_sets_in_G = []
                for W in T_XY:
                    inter = {p for p in G if p in W}
                    basic_open_sets_in_G.append(inter)
            else:
                # Default to the product topology
                basic_open_sets_in_G = []
                for U in T_X:
                    for V in T_Y:
                        inter = {(x, y) for (x, y) in G if x in U and y in V}
                        basic_open_sets_in_G.append(inter)
                        
            is_G_connected = is_connected(G, basic_open_sets_in_G)
            neg_q = not is_G_connected
            
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: X is a connected space",
    "H_2: f: X -> Y is a continuous function",
    "¬Q: The graph G is not a connected subset of X x Y"
]

N_HYP = 2
NEG_Q_INDEX = 2