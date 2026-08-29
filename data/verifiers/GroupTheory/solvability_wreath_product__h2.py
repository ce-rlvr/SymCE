import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
)

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def wreath_product(A, B):
    """
    Constructs the standard wreath product A wr B of two permutation groups.
    A acts on m points, B acts on n points.
    The wreath product acts on m * n points.
    """
    if not hasattr(A, 'degree') or not hasattr(B, 'degree'):
        raise ValueError("A and B must be permutation groups")
    
    m = A.degree
    n = B.degree
    if m == 0: m = 1
    if n == 0: n = 1
    gens = []
    
    # Generators for the base group A^n
    for g in A.generators:
        for k in range(n):
            perm = list(range(m * n))
            for i in range(m):
                perm[i + k * m] = int(g(i)) + k * m
            gens.append(Permutation(perm))
            
    # Generators for the top group B
    for h in B.generators:
        perm = list(range(m * n))
        for j in range(n):
            hj = int(h(j))
            for i in range(m):
                perm[i + j * m] = i + hj * m
        gens.append(Permutation(perm))
        
    if not gens:
        return PermutationGroup([Permutation(list(range(m * n)))])
    return PermutationGroup(gens)

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                A, B, G = witness
                G_provided = True
            elif len(witness) == 2:
                A, B = witness
                G_provided = False
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: A is a finite solvable group
    try:
        h1_val = A.is_solvable
        if callable(h1_val):
            h1_val = h1_val()
        h1 = bool(h1_val)
    except Exception:
        h1 = False

    # H_2: G is the wreath product of A and B
    try:
        W = wreath_product(A, B)
        if G_provided:
            if G == W:
                h2 = True
            else:
                g_order = G.order
                if callable(g_order):
                    g_order = g_order()
                w_order = W.order
                if callable(w_order):
                    w_order = w_order()
                
                if g_order != w_order:
                    h2 = False
                else:
                    h2 = G.is_isomorphic(W)
        else:
            G = W
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: G is not a solvable group
    try:
        neg_q_val = G.is_solvable
        if callable(neg_q_val):
            neg_q_val = neg_q_val()
        neg_q = not bool(neg_q_val)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is a finite solvable group",
    "H_2: G is the wreath product of A and B",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2