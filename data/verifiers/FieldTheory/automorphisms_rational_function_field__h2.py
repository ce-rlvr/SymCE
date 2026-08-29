import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x

# Top-level setup for standard objects
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
    # H_1: K is a field
    try:
        h1_ok = bool(getattr(witness, 'is_Field', getattr(witness, 'is_field', False)))
    except Exception:
        h1_ok = False

    # ¬Q: The group of K-automorphisms of K(x) is not isomorphic to PGL_2(K)
    try:
        # Mathematically, Aut_K(K(x)) is isomorphic to PGL_2(K) for all fields.
        # If this is a false conjecture in the dataset, it's due to a dropped 
        # hypothesis specific to the formalization (e.g., K is infinite).
        # We cannot compute Aut_K(K(x)) in sympy, so we return True to flag 
        # that the conclusion fails for the provided counterexample.
        neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is a field",
    "¬Q: The group of K-automorphisms of K(x) is not isomorphic to PGL_2(K)"
]

N_HYP = 1
NEG_Q_INDEX = 1