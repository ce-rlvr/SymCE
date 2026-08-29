import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
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
        if isinstance(witness, dict):
            A = witness.get('A')
            p = witness.get('p')
        elif isinstance(witness, tuple) and len(witness) == 2:
            A, p = witness
        else:
            A, p = None, None
    except Exception:
        A, p = None, None

    try:
        h1_ok = bool(getattr(A, "is_abelian", False))
    except Exception:
        h1_ok = False

    try:
        h2_ok = isinstance(p, int)
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = not isprime(p)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is an abelian group",
    "H_2: pA is the subgroup of A defined by {pa | a in A} (p is an integer)",
    "¬Q: A/pA is not a vector space over F_p (p is not prime)"
]

N_HYP = 2
NEG_Q_INDEX = 2