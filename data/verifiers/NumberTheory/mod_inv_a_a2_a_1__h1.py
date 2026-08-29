import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        a = witness
        m = a**2 + a + 1
        inv = sympy.mod_inverse(a, m)
        q_holds = (inv % m) == (-(a + 1) % m)
        neg_q = not q_holds
    except Exception:
        # If mod_inverse is undefined or raises an error (e.g. for non-integers),
        # the conclusion fails.
        neg_q = True
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The modular inverse of a modulo a^2+a+1 is not congruent to -(a+1) mod a^2+a+1"
]

N_HYP = 0
NEG_Q_INDEX = 0