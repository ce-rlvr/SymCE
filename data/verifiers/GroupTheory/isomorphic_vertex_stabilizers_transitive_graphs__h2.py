import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from itertools import permutations

# Top-level setup for potential witness references
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (n, E, u, v) where:
      - n is the number of vertices (vertices are 0, 1, ..., n-1)
      - E is a list of edges (each edge is a 2-element iterable of vertices)
      - u and v are vertices in the graph
    """
    try:
        n, E, u, v = witness
        E = list(E)
    except Exception:
        return [False, False, False]
        
    # H_1: Γ is a graph (simple graph on n vertices)
    try:
        h1 = isinstance(n, int) and n > 0
        if h1:
            for e in E:
                if not isinstance(e, (list, tuple, set, frozenset)) or len(e) != 2:
                    h1 = False
                    break
                e_list = list(e)
                u_e, v_e = e_list[0], e_list[1]
                if not (isinstance(u_e, int) and isinstance(v_e, int) and 0 <= u_e < n and 0 <= v_e < n):
                    h1 = False
                    break
                if u_e == v_e:
                    h1 = False # must be a simple graph (no self-loops)
                    break
    except Exception:
        h1 = False

    # H_2: u and v are vertices in V(Γ)
    try:
        h2 = isinstance(u, int) and isinstance(v, int) and 0 <= u < n and 0 <= v < n
    except Exception:
        h2 = False

    # ¬Q: The point stabilizer of u in Aut(Γ) is NOT isomorphic to the point stabilizer of v in Aut(Γ)
    neg_q = False
    if h1 and h2:
        try:
            edges = set(frozenset(e) for e in E)
            aut_perms = []
            
            # Compute the automorphism group of the graph
            for p in permutations(range(n)):
                preserves = True
                for e in edges:
                    e_list = list(e)
                    mapped_e = frozenset([p[e_list[0]], p[e_list[1]]])
                    if mapped_e not in edges:
                        preserves = False
                        break
                if preserves:
                    # Convert to list to ensure array form permutation (degree n)
                    aut_perms.append(Permutation(list(p)))
            
            aut = PermutationGroup(aut_perms)
            
            # Compute point stabilizers
            stab_u = aut.stabilizer(u)
            stab_v = aut.stabilizer(v)
            
            order_u = stab_u.order()
            order_v = stab_v.order()
            
            if order_u != order_v:
                neg_q = True
            else:
                if order_u == 1:
                    neg_q = False
                elif order_u > 6:
                    # For larger groups, attempt to use SymPy's built-in isomorphism check
                    try:
                        neg_q = not stab_u.is_isomorphic(stab_v)
                    except Exception:
                        neg_q = False
                else:
                    # For small groups, use a brute-force isomorphism check
                    try:
                        elems_u = list(stab_u.elements)
                    except AttributeError:
                        elems_u = list(stab_u.generate())
                    try:
                        elems_v = list(stab_v.elements)
                    except AttributeError:
                        elems_v = list(stab_v.generate())
                        
                    table_u = []
                    for a in elems_u:
                        row = []
                        for b in elems_u:
                            row.append(elems_u.index(a * b))
                        table_u.append(row)
                        
                    table_v = []
                    for a in elems_v:
                        row = []
                        for b in elems_v:
                            row.append(elems_v.index(a * b))
                        table_v.append(row)
                        
                    is_iso = False
                    for p in permutations(range(order_u)):
                        mapping_valid = True
                        for i in range(order_u):
                            for j in range(order_u):
                                if p[table_u[i][j]] != table_v[p[i]][p[j]]:
                                    mapping_valid = False
                                    break
                            if not mapping_valid:
                                break
                        if mapping_valid:
                            is_iso = True
                            break
                    neg_q = not is_iso
        except Exception:
            neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Γ is a graph",
    "H_2: u and v are vertices in V(Γ)",
    "¬Q: The point stabilizer of u in Aut(Γ) is not isomorphic to the point stabilizer of v in Aut(Γ)"
]

N_HYP = 2
NEG_Q_INDEX = 2