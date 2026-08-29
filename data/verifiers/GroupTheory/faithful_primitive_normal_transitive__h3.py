import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a group acting on a set X
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: The action of G on X is faithful
    try:
        # In SymPy, a PermutationGroup acts faithfully on its domain by definition
        h2 = h1
    except Exception:
        h2 = False
        
    # H3: N is a non-trivial normal subgroup of G
    try:
        if not h1:
            h3 = False
        else:
            is_sub = all(gen in G for gen in N.generators)
            is_non_trivial = N.order() > 1
            if is_sub and is_non_trivial:
                is_norm = True
                for g in G.generators:
                    g_inv = ~g
                    for n in N.generators:
                        if (g * n * g_inv) not in N:
                            is_norm = False
                            break
                        if (g_inv * n * g) not in N:
                            is_norm = False
                            break
                    if not is_norm:
                        break
                h3 = is_norm
            else:
                h3 = False
    except Exception:
        h3 = False
        
    # neg_Q: The normal subgroup N does NOT act transitively on X
    try:
        if not h1:
            neg_q = False
        else:
            degree = G.degree
            if degree == 0:
                neg_q = True
            else:
                # Compute the orbit of 0 under the action of N
                orbit = {0}
                queue = [0]
                while queue:
                    curr = queue.pop(0)
                    for gen in N.generators:
                        # Apply generator to the current point
                        nxt = gen(curr) if curr < gen.size else curr
                        if nxt not in orbit:
                            orbit.add(nxt)
                            queue.append(nxt)
                # N is transitive on X iff the orbit of 0 covers the entire domain of G
                neg_q = orbit != set(range(degree))
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: The action of G on X is faithful",
    "H_3: N is a non-trivial normal subgroup of G",
    "¬Q: The normal subgroup N does NOT act transitively on X"
]

N_HYP = 3
NEG_Q_INDEX = 3