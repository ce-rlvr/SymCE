import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis is n >= 2. For n = 1, the Artin presentation is ill-defined
    (generators \sigma_1, \dots, \sigma_0) and thus the conclusion fails.
    """
    # H_1: B_n is the braid group on n strands
    try:
        n = int(witness)
        # The witness must be an integer representing the number of strands (n >= 1)
        h1_ok = isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool) and n >= 1
    except Exception:
        h1_ok = False

    # ¬Q: The conclusion FAILS at the witness
    try:
        n = int(witness)
        # The Artin presentation is valid and isomorphic to B_n for n >= 2.
        # For n < 2 (specifically n = 1), the presentation notation is invalid/empty,
        # making the literal conclusion false.
        neg_q_ok = (n < 2)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: B_n is the braid group on n strands",
    "¬Q: The Artin presentation is invalid or not isomorphic to B_n"
]

N_HYP = 1
NEG_Q_INDEX = 1