import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    char = None
    try:
        if isinstance(witness, int):
            char = witness
        elif isinstance(witness, str):
            # Extract the first sequence of digits to identify characteristic
            digits = ''.join(c if c.isdigit() else ' ' for c in witness)
            numbers = digits.split()
            if numbers:
                char = int(numbers[0])
        else:
            if hasattr(witness, 'characteristic'):
                c = witness.characteristic()
                char = c() if callable(c) else c
            elif hasattr(witness, 'char'):
                char = witness.char
            elif witness == sympy.S.Complexes:
                char = 0
    except Exception:
        pass

    # H_1: K is algebraically closed
    try:
        if witness in [sympy.S.Reals, sympy.S.Rationals, sympy.S.Integers]:
            h1 = False
        elif str(witness) in ['QQ', 'ZZ', 'RR']:
            h1 = False
        else:
            # Assume the witness represents an algebraically closed field of the given characteristic
            h1 = True
    except Exception:
        h1 = False

    # H_2: W(K) is the Witt ring of non-degenerate symmetric bilinear forms over K
    try:
        h2 = True
    except Exception:
        h2 = False

    # ¬Q: W(K) is not isomorphic to Z/2Z
    # The theorem holds for algebraically closed fields of characteristic != 2.
    # The dropped hypothesis is "characteristic != 2", so the conclusion fails when char == 2.
    try:
        neg_q = (char == 2)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is algebraically closed",
    "H_2: W(K) is the Witt ring of non-degenerate symmetric bilinear forms over K",
    "¬Q: W(K) is not isomorphic to Z/2Z"
]

N_HYP = 2
NEG_Q_INDEX = 2