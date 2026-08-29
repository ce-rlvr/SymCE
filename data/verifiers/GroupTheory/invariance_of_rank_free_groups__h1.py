import sympy
from sympy.combinatorics import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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

def get_cardinality(S):
    """Helper to safely get the cardinality of a set, list, or SymPy Set."""
    if hasattr(S, 'cardinality'):
        return S.cardinality()
    if isinstance(S, (list, tuple)):
        return len(set(S))
    return len(S)

def conditions(witness) -> list[bool]:
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    Expected witness format: a tuple (F1, S1, F2, S2) or a dict with these keys.
    """
    try:
        if isinstance(witness, dict):
            F1 = witness['F1']
            S1 = witness['S1']
            F2 = witness['F2']
            S2 = witness['S2']
        else:
            F1, S1, F2, S2 = witness
    except Exception:
        return [False, False, False]

    # H_1: F2 is a free group on a set S2
    try:
        h1_ok = type(F2).__name__ == 'FreeGroup' and get_cardinality(S2) == F2.rank
    except Exception:
        h1_ok = False

    # H_2: F1 is isomorphic to F2
    try:
        if type(F1).__name__ == 'FreeGroup' and type(F2).__name__ == 'FreeGroup':
            h2_ok = (F1.rank == F2.rank)
        else:
            h2_ok = (F1 == F2)
    except Exception:
        h2_ok = False

    # neg_Q: The sets S1 and S2 do NOT have the same cardinality
    try:
        neg_q_ok = get_cardinality(S1) != get_cardinality(S2)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F2 is a free group on a set S2",
    "H_2: F1 is isomorphic to F2",
    "¬Q: The sets S1 and S2 do not have the same cardinality"
]

N_HYP = 2
NEG_Q_INDEX = 2