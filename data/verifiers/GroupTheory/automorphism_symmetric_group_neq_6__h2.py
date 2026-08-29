import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    n = None
    if isinstance(witness, int):
        n = witness
    elif hasattr(witness, 'degree'):
        n = witness.degree
    elif isinstance(witness, (tuple, list)) and len(witness) > 0:
        if isinstance(witness[0], int):
            n = witness[0]
        elif hasattr(witness[0], 'degree'):
            n = witness[0].degree

    try:
        h1_ok = isinstance(n, int) and n >= 3
    except Exception:
        h1_ok = False

    try:
        # The conclusion states that Aut(S_n) is isomorphic to S_n.
        # It is a known theorem that for n >= 3, Aut(S_n) is isomorphic to S_n 
        # if and only if n != 6. For n = 6, Aut(S_6) has order 1440 while S_6 has order 720.
        # Thus, the conclusion fails (neg_Q is True) exactly when n == 6.
        neg_q_ok = False
        if h1_ok:
            neg_q_ok = (n == 6)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is an integer >= 3",
    "¬Q: Aut(S_n) is not isomorphic to S_n (fails for n=6)"
]

N_HYP = 1
NEG_Q_INDEX = 1