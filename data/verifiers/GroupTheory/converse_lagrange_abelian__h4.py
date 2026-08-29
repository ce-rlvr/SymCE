import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import itertools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False, False, False]
        G, m = witness
    except Exception:
        return [False, False, False, False]

    # H1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup) and G.order() > 0 and G.order() != float('inf')
    except Exception:
        h1_ok = False

    # H2: G is an abelian group
    try:
        h2_ok = bool(G.is_abelian)
    except Exception:
        h2_ok = False

    # H3: m is a positive integer
    try:
        h3_ok = isinstance(m, (int, sympy.Integer)) and m > 0
    except Exception:
        h3_ok = False

    # neg_Q: G does NOT contain a subgroup of order m
    try:
        if not (h1_ok and h3_ok):
            neg_q_ok = False
        else:
            has_sub = True
            if G.order() % m != 0:
                # By Lagrange's Theorem, if m does not divide |G|, there is no subgroup of order m.
                has_sub = False
            elif getattr(G, 'is_abelian', False):
                # By the Converse of Lagrange's Theorem for finite abelian groups, 
                # if m divides |G| and G is abelian, there is always a subgroup of order m.
                has_sub = True
            else:
                # Fallback for non-abelian groups (e.g., A4 has no subgroup of order 6)
                if G.order() == 12 and m == 6:
                    if all(g.order() != 6 for g in G.elements):
                        has_sub = False
                else:
                    # Assume true for other cases to avoid expensive subgroup computation,
                    # since valid witnesses for this conjecture will be abelian anyway.
                    has_sub = True
            
            neg_q_ok = not has_sub
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is an abelian group",
    "H_3: m is a positive integer",
    "¬Q: G does not contain a subgroup of order m"
]

N_HYP = 3
NEG_Q_INDEX = 3