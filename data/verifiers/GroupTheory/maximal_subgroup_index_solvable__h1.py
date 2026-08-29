import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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
        G, M = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = False
        if M.is_subgroup(G) and M.order() < G.order():
            h1 = True
            for g in list(G.generate()):
                if g not in M:
                    H = PermutationGroup(list(M.generators) + [g])
                    if H.order() != G.order():
                        h1 = False
                        break
    except Exception:
        h1 = False

    try:
        neg_q = False
        if G.order() % M.order() == 0:
            idx = G.order() // M.order()
            if idx > 1:
                factors = factorint(idx)
                if len(factors) > 1:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: M is a maximal subgroup of G",
    "not Q: The index of M in G is not a power of a prime number"
]

N_HYP = 1
NEG_Q_INDEX = 1
