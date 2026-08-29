import sympy
import sympy.combinatorics
import sympy.matrices
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: L is an algebraic field extension of K
    try:
        h1 = False
        if hasattr(witness, 'L_is_algebraic_extension_of_K'):
            attr = witness.L_is_algebraic_extension_of_K
            h1 = bool(attr() if callable(attr) else attr)
        elif hasattr(witness, 'is_algebraic_extension'):
            attr = witness.is_algebraic_extension
            h1 = bool(attr() if callable(attr) else attr)
        elif isinstance(witness, dict) and 'L_is_algebraic_extension_of_K' in witness:
            h1 = bool(witness['L_is_algebraic_extension_of_K'])
        elif isinstance(witness, dict) and 'is_algebraic_extension' in witness:
            h1 = bool(witness['is_algebraic_extension'])
        elif isinstance(witness, tuple) and len(witness) >= 2 and isinstance(witness[0], (bool, int)):
            h1 = bool(witness[0])
    except Exception:
        h1 = False

    # ¬Q: S is not a subfield of L
    try:
        q = True
        if hasattr(witness, 'S_is_subfield_of_L'):
            attr = witness.S_is_subfield_of_L
            q = bool(attr() if callable(attr) else attr)
        elif hasattr(witness, 'is_subfield'):
            attr = witness.is_subfield
            q = bool(attr() if callable(attr) else attr)
        elif isinstance(witness, dict) and 'S_is_subfield_of_L' in witness:
            q = bool(witness['S_is_subfield_of_L'])
        elif isinstance(witness, dict) and 'is_subfield' in witness:
            q = bool(witness['is_subfield'])
        elif isinstance(witness, tuple) and len(witness) >= 2 and isinstance(witness[1], (bool, int)):
            q = bool(witness[1])
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: L is an algebraic field extension of K",
    "¬Q: S is not a subfield of L"
]

N_HYP = 1
NEG_Q_INDEX = 1