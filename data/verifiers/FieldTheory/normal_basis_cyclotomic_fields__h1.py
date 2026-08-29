import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup
from sympy.combinatorics.named_groups import CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

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

def conditions(witness):
    try:
        if isinstance(witness, bool):
            h1 = False
        else:
            n = int(witness)
            if n == witness:
                h1 = (n >= 1)
            else:
                h1 = False
    except Exception:
        h1 = False

    try:
        if h1:
            n = int(witness)
            factors = factorint(n)
            is_sqf = all(v == 1 for v in factors.values())
            # By the Normal Basis Theorem, the field extension K/Q always possesses a normal basis.
            # Thus, the statement "K/Q possesses a normal basis" is unconditionally True.
            # The conclusion claims this is True IF AND ONLY IF n is square-free.
            # Therefore, the conclusion holds iff n is square-free.
            # The negated conclusion holds iff n is NOT square-free.
            neg_q = not is_sqf
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K = Q(zeta_n) is the n-th cyclotomic field (n >= 1)",
    "¬Q: The equivalence (K/Q possesses a normal basis iff n is square-free) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1