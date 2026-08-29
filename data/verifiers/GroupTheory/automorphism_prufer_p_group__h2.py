import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup

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

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            p, G = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]

    try:
        h1_ok = bool(sympy.isprime(p))
    except Exception:
        h1_ok = False

    try:
        # The group of p-adic units Z_p^x is uncountably infinite for any prime p.
        # If G is a finite permutation group, its automorphism group Aut(G) is finite.
        # Therefore, Aut(G) cannot be isomorphic to Z_p^x.
        if isinstance(G, PermutationGroup):
            neg_q_ok = True
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: Aut(G) is not isomorphic to Z_p^x"
]

N_HYP = 1
NEG_Q_INDEX = 1