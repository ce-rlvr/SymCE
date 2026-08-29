import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, p = witness
        else:
            G = witness
            p = None
    except Exception:
        G = None
        p = None

    # H_1: p is a prime number
    try:
        h1_ok = bool(sympy.isprime(p))
    except Exception:
        h1_ok = False

    # neg_Q: G is not an abelian group
    try:
        neg_q_ok = (G.is_abelian is False)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: G is not an abelian group"
]

N_HYP = 1
NEG_Q_INDEX = 1