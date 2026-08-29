import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, A, B = witness
        elif isinstance(witness, tuple) and len(witness) == 1:
            G = witness[0]
            if isinstance(G, PermutationGroup):
                if G.generators:
                    g = G.generators[0]
                    id_perm = g ** g.order()
                else:
                    id_perm = Permutation()
                A = PermutationGroup([id_perm])
                B = PermutationGroup([id_perm])
            else:
                A = B = None
        else:
            G = witness
            if isinstance(G, PermutationGroup):
                if G.generators:
                    g = G.generators[0]
                    id_perm = g ** g.order()
                else:
                    id_perm = Permutation()
                A = PermutationGroup([id_perm])
                B = PermutationGroup([id_perm])
            else:
                A = B = None
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: A is an abelian subgroup of G
    try:
        h2 = False
        if isinstance(A, PermutationGroup) and isinstance(G, PermutationGroup):
            is_sub = all(g in G for g in A.generators)
            a_ab = A.is_abelian
            if callable(a_ab):
                a_ab = a_ab()
            h2 = bool(is_sub and a_ab)
    except Exception:
        h2 = False

    # H_3: B is an abelian subgroup of G
    try:
        h3 = False
        if isinstance(B, PermutationGroup) and isinstance(G, PermutationGroup):
            is_sub = all(g in G for g in B.generators)
            b_ab = B.is_abelian
            if callable(b_ab):
                b_ab = b_ab()
            h3 = bool(is_sub and b_ab)
    except Exception:
        h3 = False

    # ¬Q: G is not metabelian or not solvable
    try:
        neg_q = False
        if isinstance(G, PermutationGroup):
            derived = G.derived_subgroup()
            der_ab = derived.is_abelian
            if callable(der_ab):
                der_ab = der_ab()
            
            solv = G.is_solvable
            if callable(solv):
                solv = solv()
                
            neg_q = not (bool(der_ab) and bool(solv))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: A is an abelian subgroup of G",
    "H_3: B is an abelian subgroup of G",
    "¬Q: G is not metabelian or not solvable"
]

N_HYP = 3
NEG_Q_INDEX = 3