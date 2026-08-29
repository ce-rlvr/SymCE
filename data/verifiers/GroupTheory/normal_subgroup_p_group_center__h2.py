import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, Permutation
from sympy.ntheory import factorint

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
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False]

    try:
        if not isinstance(G, PermutationGroup):
            h1_ok = False
        else:
            order = G.order()
            factors = factorint(order)
            h1_ok = (len(factors) == 1) or (order == 1)
    except Exception:
        h1_ok = False

    try:
        if not isinstance(N, PermutationGroup) or not isinstance(G, PermutationGroup):
            h2_ok = False
        else:
            is_subgroup = all(g in G for g in N.generators)
            h2_ok = is_subgroup and N.order() > 1
    except Exception:
        h2_ok = False

    try:
        if not isinstance(N, PermutationGroup) or not isinstance(G, PermutationGroup):
            neg_q_ok = False
        else:
            Z = G.center()
            int_order = 0
            for g in N.generate():
                if g in Z:
                    int_order += 1
                    if int_order > 1:
                        break
            neg_q_ok = (int_order == 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite p-group",
    "H_2: N is a non-trivial subgroup of G",
    "¬Q: The intersection of N and Z(G) is trivial"
]

N_HYP = 2
NEG_Q_INDEX = 2