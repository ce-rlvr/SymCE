import math
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
        H1 = isinstance(witness, PermutationGroup)
    except Exception:
        H1 = False

    try:
        if H1:
            p = witness.degree
            if callable(p):
                p = p()
            H2 = bool(isprime(p))
        else:
            H2 = False
    except Exception:
        H2 = False

    try:
        H3 = False
        if H1:
            for g in witness.generate():
                cycles = g.cyclic_form
                if callable(cycles):
                    cycles = cycles()
                if len(cycles) == 1 and len(cycles[0]) == 2:
                    H3 = True
                    break
    except Exception:
        H3 = False

    try:
        if H1 and H2:
            p = witness.degree
            if callable(p):
                p = p()
            order = witness.order
            if callable(order):
                order = order()
            neg_Q = bool(order != math.factorial(p))
        else:
            neg_Q = False
    except Exception:
        neg_Q = False

    return [H1, H2, H3, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a permutation group",
    "H_2: The degree p of G is a prime number",
    "H_3: G contains at least one transposition",
    "¬Q: G is not equal to the symmetric group S_p"
]

N_HYP = 3
NEG_Q_INDEX = 3