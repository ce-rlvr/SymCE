import math
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.ntheory import factorint

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

def divides_factorial(index, n):
    if index == 1:
        return True
    if n >= index:
        return True
    factors = factorint(index)
    for p, k in factors.items():
        count = 0
        power = p
        while power <= n:
            count += n // power
            power *= p
        if count < k:
            return False
    return True

def conditions(witness):
    try:
        if len(witness) == 3:
            G, H, n = witness
        elif len(witness) == 2:
            G, H = witness
            n = G.order() // H.order()
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: H is a subgroup of G
    try:
        if isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup):
            h2 = all(g in G for g in H.generators)
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: NOT (There exists a normal subgroup N of G such that N <= H and [G:N] divides n!)
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            try:
                n_val = int(n)
            except Exception:
                n_val = -1
                
            if n_val < 0:
                neg_q = False
            else:
                core = H
                while True:
                    new_core = core
                    for g in G.generators:
                        conj_gens = []
                        for h in core.generators:
                            conj_gens.append(g * h * ~g)
                        if not conj_gens:
                            conj_gens = [g**0]
                        conj_H = PermutationGroup(conj_gens)
                        new_core = new_core.intersect(conj_H)
                    if new_core.order() == core.order():
                        break
                    core = new_core
                
                index = G.order() // core.order()
                neg_q = not divides_factorial(index, n_val)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: G is a group", "H_2: H is a subgroup of G", "¬Q: no normal subgroup N of G in H has index dividing n factorial"]
N_HYP = 2
NEG_Q_INDEX = 2