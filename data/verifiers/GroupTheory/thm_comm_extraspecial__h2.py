import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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
        G, p = witness
    except Exception:
        return [False, False]

    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    try:
        comm = G.derived_subgroup()
        neg_q = bool(comm.order() != p)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: p is a prime number", "¬Q: The commutator subgroup does not have order exactly p"]
N_HYP = 1
NEG_Q_INDEX = 1