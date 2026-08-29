import sympy
from sympy.combinatorics import Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import symbols, eye, zeros

# Standard group theory objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_finite_simplicial_graph(witness):
    """
    Checks if the witness is mathematically a finite simplicial graph 
    (undirected, no loops, no multiple edges, finite vertices).
    """
    try:
        # 1. NetworkX-like graph object
        if hasattr(witness, 'nodes') and hasattr(witness, 'edges'):
            if getattr(witness, 'is_directed', lambda: False)():
                return False
            if getattr(witness, 'is_multigraph', lambda: False)():
                return False
            for u, v in witness.edges():
                if u == v:
                    return False
            return True
            
        # 2. Dictionary with explicit 'V' and 'E'
        if isinstance(witness, dict) and 'V' in witness and 'E' in witness:
            V = witness['V']
            E = witness['E']
        # 3. Object with .V and .E attributes
        elif hasattr(witness, 'V') and hasattr(witness, 'E'):
            V = witness.V
            E = witness.E
        # 4. Adjacency dictionary
        elif isinstance(witness, dict):
            for u, neighbors in witness.items():
                for v in neighbors:
                    if u == v:
                        return False
                    if v not in witness or u not in witness[v]:
                        return False
            return True
        # 5. Tuple (V, E)
        else:
            V, E = witness
            
        if not isinstance(V, (list, set, tuple, frozenset)):
            return False
            
        if isinstance(E, dict):
            for u, neighbors in E.items():
                for v in neighbors:
                    if u == v:
                        return False
                    if v not in E or u not in E[v]:
                        return False
            return True
            
        seen_edges = set()
        for edge in E:
            if isinstance(edge, (set, frozenset)):
                if len(edge) != 2:
                    return False
                fs = frozenset(edge)
                if fs in seen_edges and isinstance(E, (list, tuple)):
                    return False
                seen_edges.add(fs)
            else:
                # If edges are given as tuples in a raw (V, E) format, 
                # it mathematically represents a directed graph.
                return False
                
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        h1 = False
        if hasattr(witness, 'nodes') and hasattr(witness, 'edges'):
            h1 = True
        elif isinstance(witness, dict) and 'V' in witness and 'E' in witness:
            h1 = True
        elif hasattr(witness, 'V') and hasattr(witness, 'E'):
            h1 = True
        elif isinstance(witness, dict):
            is_adj = True
            for k, v in witness.items():
                if not isinstance(v, (list, set, tuple, frozenset)):
                    is_adj = False
                    break
            if is_adj:
                h1 = True
        else:
            V, E = witness
            if isinstance(V, (list, set, tuple, frozenset)) and isinstance(E, (list, set, tuple, frozenset, dict)):
                h1 = True
    except Exception:
        h1 = False

    try:
        # The conclusion is that G(Gamma) admits the presentation < V | vw = wv for all {v, w} in E >.
        # This presentation correctly defines the RAAG if and only if Gamma is a finite simplicial graph.
        # If Gamma is directed, a multigraph, has loops, or is infinite, the presentation fails to 
        # capture the correct relations (e.g., {v, w} in E is false for directed tuple edges).
        neg_q = not is_finite_simplicial_graph(witness)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Let G(Gamma) be the right-angled Artin group associated with Gamma",
    "¬Q: G(Gamma) does not admit the presentation < V | vw = wv for all {v, w} in E >"
]

N_HYP = 1
NEG_Q_INDEX = 1