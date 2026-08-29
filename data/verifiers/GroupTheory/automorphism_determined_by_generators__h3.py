import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        G, S, phi, psi = witness
    except Exception:
        return [False, False, False, False]

    def evaluate(f, x):
        if isinstance(f, dict):
            return f[x]
        return f(x)

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: S is a generating set for G
    try:
        if not h1:
            h2 = False
        else:
            S_list = list(S)
            if not all(s in G for s in S_list):
                h2 = False
            elif not S_list:
                h2 = (G.order() == 1)
            else:
                H = PermutationGroup(S_list)
                h2 = (H.order() == G.order())
    except Exception:
        h2 = False

    # H3: phi(s) == psi(s) for all s in S
    try:
        if not h1:
            h3 = False
        else:
            h3 = True
            for s in S:
                if evaluate(phi, s) != evaluate(psi, s):
                    h3 = False
                    break
    except Exception:
        h3 = False

    # neg_Q: phi(x) != psi(x) for some x in G
    try:
        if not h1:
            neg_q = False
        else:
            # First verify they are defined on all of G
            for x in G.elements:
                evaluate(phi, x)
                evaluate(psi, x)
            
            neg_q = False
            for x in G.elements:
                if evaluate(phi, x) != evaluate(psi, x):
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: S is a generating set for G",
    "H_3: phi(s) == psi(s) for all s in S",
    "¬Q: phi(x) != psi(x) for some x in G"
]

N_HYP = 3
NEG_Q_INDEX = 3