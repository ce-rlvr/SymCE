import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
)

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False]
        G, N = witness
    except Exception:
        return [False, False]

    # H_1: N is a normal subgroup of G
    try:
        h1_ok = True
        # Check if N is a subgroup of G
        for n in N.generators:
            if n not in G:
                h1_ok = False
                break
        # Check normality: g * n * g^-1 in N for all generators
        if h1_ok:
            for g in G.generators:
                for n in N.generators:
                    if (g * n * (g**-1)) not in N:
                        h1_ok = False
                        break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False

    # ¬Q: G/N is NOT a solvable group
    # G/N is solvable iff the derived series of G eventually falls into N.
    try:
        curr = G
        is_solv = False
        while True:
            # Check if curr is a subgroup of N
            sub_ok = True
            for g in curr.generators:
                if g not in N:
                    sub_ok = False
                    break
            if sub_ok:
                is_solv = True
                break
            
            nxt = curr.derived_subgroup()
            # If the derived series stabilizes before reaching N, it's not solvable
            if curr.order() == nxt.order():
                is_solv = False
                break
            curr = nxt
        neg_q_ok = not is_solv
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "¬Q: G/N is not a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1