import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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
            G, p = witness
        else:
            G = witness
            p = G.degree
    except Exception:
        return [False, False]

    try:
        h1 = bool(isprime(p)) and (G.degree == p)
    except Exception:
        h1 = False

    try:
        neg_q = not bool(G.is_primitive())
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p (degree of G) is a prime number",
    "¬Q: G does not act primitively on the set"
]

N_HYP = 1
NEG_Q_INDEX = 1