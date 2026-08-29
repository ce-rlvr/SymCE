import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, R = witness
        else:
            G = witness
            res = G
            while True:
                nxt = res.derived_subgroup()
                if nxt.order() == res.order():
                    break
                res = nxt
            R = res
    except Exception:
        return [False, False]

    # H1: R is the solvable residual of G
    try:
        if not (hasattr(G, 'generators') and hasattr(R, 'generators')):
            h1 = False
        else:
            res = G
            while True:
                nxt = res.derived_subgroup()
                if nxt.order() == res.order():
                    break
                res = nxt
            
            h1 = True
            if R.order() != res.order():
                h1 = False
            else:
                for g in R.generators:
                    if not res.contains(g):
                        h1 = False
                        break
    except Exception:
        h1 = False

    # neg_Q: R is not equal to G
    try:
        if not (hasattr(G, 'generators') and hasattr(R, 'generators')):
            neg_q = False
        else:
            eq = True
            if R.order() != G.order():
                eq = False
            else:
                for g in R.generators:
                    if not G.contains(g):
                        eq = False
                        break
            neg_q = not eq
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is the solvable residual of G",
    "¬Q: R is not equal to G"
]

N_HYP = 1
NEG_Q_INDEX = 1