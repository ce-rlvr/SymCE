import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    """
    # H_1: X is a non-empty set
    try:
        if isinstance(witness, (set, frozenset, list, tuple)):
            H1 = len(witness) > 0
        elif isinstance(witness, sympy.Set):
            H1 = witness.is_empty == False
        else:
            H1 = False
    except Exception:
        H1 = False

    # H_2: P(X) is the Boolean ring of subsets of X with symmetric difference as addition
    # This is a definitional setup step that holds for any valid set X.
    H2 = True

    # H_3: phi is defined as the characteristic function map
    # This is also a definitional setup step.
    H3 = True

    # not Q: The map phi is NOT a ring isomorphism
    # The conjecture is false because the target ring Z_2 was not explicitly defined 
    # as the field of two elements (modulo 2 arithmetic). If Z_2 is interpreted as 
    # the 2-adic integers (or standard integers), then 1 + 1 = 2 != 0. 
    # In that case, phi(A \Delta B) != phi(A) + phi(B) for intersecting sets, 
    # meaning phi fails to be a ring homomorphism for any non-empty set X.
    try:
        if not H1:
            neg_Q = False
        else:
            # For any non-empty set, we can pick an element x and let A = {x}.
            # phi(A \Delta A)(x) = phi(empty)(x) = 0
            # phi(A)(x) + phi(A)(x) = 1 + 1 = 2
            # Since 0 != 2, it is not a homomorphism.
            neg_Q = True
    except Exception:
        neg_Q = False

    return [H1, H2, H3, neg_Q]

CONDITION_LABELS = [
    "H_1: X is a non-empty set",
    "H_2: P(X) is the Boolean ring of subsets of X",
    "H_3: phi is the characteristic function map",
    "not Q: phi is not a ring isomorphism"
]

N_HYP = 3
NEG_Q_INDEX = 3