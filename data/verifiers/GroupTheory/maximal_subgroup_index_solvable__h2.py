import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.ntheory import factorint

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, M = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]

    try:
        h1 = getattr(G, 'is_solvable', False)
        if h1 is None:
            h1 = False
        h1 = bool(h1)
    except Exception:
        h1 = False

    try:
        if not isinstance(G, PermutationGroup) or not isinstance(M, PermutationGroup):
            neg_q = False
        else:
            is_sub = all(G.contains(g) for g in M.generators)
            if not is_sub:
                neg_q = False
            else:
                idx = G.order() // M.order()
                factors = factorint(idx)
                is_prime_power = (len(factors) == 1)
                neg_q = not is_prime_power
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite solvable group",
    "not Q: The index of M in G is not a power of a prime number"
]

N_HYP = 1
NEG_Q_INDEX = 1