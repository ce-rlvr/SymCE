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
    # The witness is the parameter n for the affine Coxeter group \tilde{A}_n.
    try:
        n = int(witness)
        # \tilde{A}_n is defined for n >= 1
        h1 = (n >= 1)
    except Exception:
        h1 = False

    try:
        n = int(witness)
        # The conclusion claims the given presentation defines \tilde{A}_n.
        # For n >= 2, the presentation is exactly the standard presentation of \tilde{A}_n.
        # For n = 1, the presentation includes the relation (s_0 s_1)^3 = 1, 
        # which yields the finite group S_3. However, \tilde{A}_1 is the infinite dihedral group,
        # which has no such relation. Thus, the conclusion fails (neg_q is True) iff n == 1.
        neg_q = (n == 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer >= 1 (defining the affine Coxeter group A-tilde_n)",
    "¬Q: The given presentation does not define A-tilde_n"
]

N_HYP = 1
NEG_Q_INDEX = 1