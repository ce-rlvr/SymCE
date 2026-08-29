import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            n = witness.get('n')
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, n = witness
        else:
            G = witness
            n = getattr(G, 'degree', None)
    except Exception:
        return [False, False]

    # H_1: n is an integer such that n <= 4
    try:
        h1_ok = (int(n) == n) and (n <= 4)
    except Exception:
        h1_ok = False

    # ¬Q: G is not a solvable group
    try:
        neg_q_ok = not bool(G.is_solvable)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is an integer such that n <= 4",
    "¬Q: G is not a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1