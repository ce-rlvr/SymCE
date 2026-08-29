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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, SymmetricGroup):
            n = witness.degree
        else:
            n = int(witness)
        h1_ok = (n >= 1)
    except Exception:
        h1_ok = False

    try:
        if isinstance(witness, SymmetricGroup):
            n = witness.degree
        else:
            n = int(witness)
        
        if n >= 1:
            # For n = 1, S_1 is the trivial group. Any homomorphism to {1, -1} 
            # must map the identity to 1, so the image is {1}. 
            # Thus, no surjective homomorphism exists.
            # For n >= 2, the sign homomorphism is surjective with kernel A_n.
            neg_q_ok = (n == 1)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: S_n is the symmetric group of degree n (n >= 1)",
    "¬Q: There does NOT exist a unique surjective group homomorphism sgn: S_n -> {1, -1} with kernel A_n"
]

N_HYP = 1
NEG_Q_INDEX = 1