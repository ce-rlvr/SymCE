import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
    """
    Check if the witness is a counterexample to the conjecture.
    The conjecture states that G is isomorphic to the binary tetrahedral group of order 24.
    Since there are no remaining hypotheses, any witness that is NOT isomorphic to the 
    binary tetrahedral group is a valid counterexample.
    
    The binary tetrahedral group is uniquely identified among groups of order 24 
    by having a derived subgroup of order 8 (which is isomorphic to the quaternion group Q8).
    """
    try:
        is_btg = False
        if hasattr(witness, 'order'):
            order = witness.order() if callable(witness.order) else witness.order
            if order == 24:
                if hasattr(witness, 'derived_subgroup'):
                    H = witness.derived_subgroup()
                    h_order = H.order() if callable(H.order) else H.order
                    if h_order == 8:
                        is_btg = True
    except Exception:
        is_btg = False

    # neg_Q is True when the conclusion FAILS (i.e., witness is NOT the binary tetrahedral group)
    neg_q = not is_btg
    
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: G is not isomorphic to the binary tetrahedral group of order 24"
]

N_HYP = 0
NEG_Q_INDEX = 0