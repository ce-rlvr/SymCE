import sympy
from sympy.combinatorics import Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, S = witness
        else:
            G = witness.G
            S = witness.S
    except Exception:
        return [False, False]

    try:
        n = G.order()
        h1 = bool(G.is_cyclic and n >= 3)
    except Exception:
        h1 = False

    try:
        elements = list(G.elements)
        n_elements = len(elements)
        elem_to_idx = {e: i for i, e in enumerate(elements)}
        
        if not all(s in elements for s in S):
            neg_q = False
        else:
            adj = {i: set() for i in range(n_elements)}
            has_self_loops = False
            
            for e in elements:
                u = elem_to_idx[e]
                for s in S:
                    v_elem = e * s
                    if v_elem in elem_to_idx:
                        v = elem_to_idx[v_elem]
                        if u == v:
                            has_self_loops = True
                        else:
                            adj[u].add(v)
                            adj[v].add(u)
            
            if has_self_loops:
                is_Cn = False
            else:
                degrees_ok = all(len(neighbors) == 2 for neighbors in adj.values())
                if not degrees_ok:
                    is_Cn = False
                else:
                    visited = set()
                    queue = [0]
                    visited.add(0)
                    while queue:
                        curr = queue.pop(0)
                        for neighbor in adj[curr]:
                            if neighbor not in visited:
                                visited.add(neighbor)
                                queue.append(neighbor)
                    is_Cn = (len(visited) == n_elements)
                    
            neg_q = not is_Cn
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group of order n >= 3",
    "¬Q: The Cayley graph Gamma(G, S) is not isomorphic to the cycle graph C_n"
]

N_HYP = 1
NEG_Q_INDEX = 1