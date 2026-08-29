import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import divisors

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

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
    except Exception:
        return [False, False]

    # H_1: N is a normal subgroup of G
    try:
        h1 = True
        # Check if N is a subgroup of G
        for gen in N.generators:
            if gen not in G:
                h1 = False
                break
        # Check normality condition: g * n * g^-1 in N
        if h1:
            for g in G.generators:
                for n in N.generators:
                    if (g * n * ~g) not in N:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # ¬Q: G/N is not locally cyclic
    # For finite groups, locally cyclic is equivalent to cyclic.
    try:
        if G.order() % N.order() != 0:
            neg_q = False
        else:
            target_order = G.order() // N.order()
            if target_order == 1:
                neg_q = False
            else:
                prop_divs = divisors(target_order)[:-1]
                is_cyclic = False
                for g in G.elements:
                    is_gen = True
                    for k in prop_divs:
                        if (g**k) in N:
                            is_gen = False
                            break
                    if is_gen:
                        is_cyclic = True
                        break
                neg_q = not is_cyclic
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "¬Q: G/N is not locally cyclic"
]

N_HYP = 1
NEG_Q_INDEX = 1