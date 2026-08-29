import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
            G = witness.get('G')
            p = witness.get('p', 2)
        elif isinstance(witness, tuple) and len(witness) == 2:
            G, p = witness
        else:
            G = witness
            p = 2
    except Exception:
        G = None
        p = None

    try:
        h1_ok = bool(isprime(p))
    except Exception:
        h1_ok = False

    try:
        neg_q_ok = bool(G.center().order() == 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: The center of G, Z(G), does not contain more than one element"
]

N_HYP = 1
NEG_Q_INDEX = 1